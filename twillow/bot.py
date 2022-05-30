
import os
import logging
import inspect
from functools import wraps

from lupa import lua_type
from rich.logging import RichHandler
from flask import Flask, abort, request, redirect
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from twilio.request_validator import RequestValidator

from .config import get_config
from .mod import load_module, load_voice_handler
from . import listutils

logging.basicConfig(level=logging.DEBUG, format="%(message)s",
                    datefmt="[%X]", handlers=[RichHandler()])
log = logging.getLogger("rich")

config = get_config()
modules = {}  # Contains modules

client = Client(config['account_sid'], config['auth_token'])  # Twilio client
app = Flask(__name__)

voice_handler = None


def send_message(body, to=config['to_number'], from_=config['from_number']):
    """Sends a message"""
    message = client.messages.create(
        body=body,
        from_=from_,
        to=to
    )

    return message


def validate_twilio_request(f):
    """Validates that incoming requests genuinely originated from Twilio"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Create an instance of the RequestValidator class
        validator = RequestValidator(config['auth_token'])

        # Validate the request using its URL, POST data,
        # and X-TWILIO-SIGNATURE header
        request_valid = validator.validate(
            request.url,
            request.form,
            request.headers.get('X-TWILIO-SIGNATURE', ''))

        # Continue processing the request if it's valid, return a 403 error if it's not
        if request_valid:
            return f(*args, **kwargs)
        else:
            return abort(403)

    return decorated_function


def help_command():
    """Help command"""
    help = MessagingResponse()

    msg = f"-- {config.get('name', 'Twillow')} Help --\n"

    for module in modules:
        msg += f'{module}:\n'

        # Get argument
        if lua_type(modules[module]) == 'table':
            d = [item[0] for item in list(modules[module].items())]
        else:
            d = dir(modules[module])

        for i in d:
            # Skip init/special methods
            if i.startswith('_') or i == 'init':
                continue

            # See if method is a function/callable
            f = getattr(modules[module], i)

            if not callable(f):
                continue

            if lua_type(f):
                if lua_type(f) != 'function':
                    continue

            # Add command to help message
            msg += f'    {module} {i} '

            try:
                for arg in inspect.getargspec(f):
                    if arg == ['self'] or not arg:
                        continue

                    msg += f"<{arg.upper()}> "
            except:
                # need to add argument support for lua somehow
                pass

            msg += '\n'

    split_msg = [msg[index: index + 1600]
                 for index in range(0, len(msg), 1600)]

    for p in split_msg:
        help.message(p)

    return str(help)


def error_message():
    """Error message"""
    help = MessagingResponse()

    help.message("⛔️ Oops! An error has occured!")

    return str(help)


@app.route('/voice', methods=['GET', 'POST'])
@validate_twilio_request
def call_reply():
    """Replies to incoming calls"""
    if voice_handler:
        return voice_handler.call_reply(request)

    return ""


@app.route("/sms", methods=['GET', 'POST'])
@validate_twilio_request
def sms_reply():
    """Respond to incoming messages."""
    command = request.values.get('Body', '').strip().split()

    help = help_command()

    if not command:
        return help

    # Try getting command from modules
    if command[0] in modules:
        # Try running subcommand, or run main command, if it exists.
        try:
            # If command length is less than 2, it can't be a subcommand
            if len(command) < 2:
                raise AttributeError

            f = getattr(modules[command[0]], command[1])
            off = 2

            if f is None:
                raise AttributeError
        except AttributeError:
            try:
                log.debug('Command not found, running _all')

                f = modules[command[0]]._all()
                off = 1

                if f is None:
                    raise AttributeError
            except AttributeError:
                return help
        except Exception as e:
            logging.exception(e)
            return error_message()

        args = listutils.get_rem(command, off)

        # Add blank arg to fix first arg not working with lua
        if lua_type(f) == 'function':
            args.insert(0, None)

        return str(f(*args))

    return help


def load_modules():
    """Load modules (unloads previously loaded onces if keep is not true"""

    # Load modules
    for loc in config.get('modules', {}):
        log.info(f'[green]Loading module from {loc}', extra={
                 "markup": True})

        loc = os.path.abspath(loc)

        try:
            name, module = load_module(loc)
        except Exception as e:
            log.exception(e)
            log.error(
                f'[red]An error occured while loading module {os.path.split(loc)[-1]}', extra={
                    "markup": True})

        modules[name] = module

        log.info(f'[green]Loaded module: {module} as "{name}"\n', extra={
                 "markup": True})


def load_voice_handlers():
    loc = config.get('voice_handler', None)

    if not loc:
        return

    log.info(f'[green]Loading voice handler from {loc}', extra={
        "markup": True})

    loc = os.path.abspath(loc)

    try:
        name, v = load_voice_handler(loc)
    except Exception as e:
        log.exception(e)
        log.error(f'[red]An error occured while loading voice handler {os.path.split(loc)[-1]}', extra={
            "markup": True})

    global voice_handler
    voice_handler = v

    log.info(f'[green]Loaded voice handler: {voice_handler} as "{name}"\n', extra={
        "markup": True})


def start():
    load_modules()

    load_voice_handlers()

    app.run(debug=False)


if __name__ == '__main__':
    start()
