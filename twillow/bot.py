
import logging
from functools import wraps

from lupa import lua_type
from rich.logging import RichHandler
from flask import Flask, abort, request, redirect
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from twilio.request_validator import RequestValidator

from .config import get_config
from .mod import load_module
from . import listutils

logging.basicConfig(level=logging.DEBUG, format="%(message)s",
                    datefmt="[%X]", handlers=[RichHandler()])
log = logging.getLogger("rich")

config = get_config()
modules = {}  # Contains modules

client = Client(config['account_sid'], config['auth_token'])  # Twilio client
app = Flask(__name__)


def send_message(body, to=config['to_number']):
    """Sends a message"""
    message = client.messages.create(
        body=body,
        from_=config['from_number'],
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

    help.message("""
    Help:
        search - Search for something on Google
        8ball - Ask the magic 8 ball a question
        """.strip())

    return str(help)


def error_message():
    """Error message"""
    help = MessagingResponse()

    help.message("""⛔️ Oops! An error has occured!""")

    return str(help)


@app.route('/voice', methods=['GET', 'POST'])
@validate_twilio_request
def call_reply():
    """Replies to incoming calls"""
    return """
<Response>
<Say voice="alice">Thank you for calling the sex hotline! Please wait while we transfer your call to a hot milf near you...</Say>
</Response>
"""


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
                logging.debug('Command not found, running _all')

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


def load_modules(keep=False):
    """Load modules (unloads previously loaded onces if keep is not true"""
    # if not keep:
    #     modules = {}

    # Load modules
    for loc in config.get('modules', {}):
        name, module = load_module(loc)
        modules[name] = module
        log.info(f'Loaded module: {module} as "{name}"')


def start():
    load_modules()

    app.run(debug=False)


if __name__ == '__main__':
    start()
