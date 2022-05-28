
from functools import wraps

from rich import print
from flask import Flask, abort, request, redirect
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from twilio.request_validator import RequestValidator

from config import get_config
from mod import load_module

config = get_config()

client = Client(config['account_sid'], config['auth_token'])
app = Flask(__name__)

modules = {}


def send_message(body, to=config['to_number']):
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


@app.route('/voice', methods=['GET', 'POST'])
@validate_twilio_request
def call_reply():
    return """
<Response>
<Say voice="alice">Thank you for calling the sex hotline! Please wait while we transfer your call to a hot milf near you...</Say>
</Response>
"""


@app.route("/sms", methods=['GET', 'POST'])
@validate_twilio_request
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    body = request.values.get('Body', None)

    command = body.split()

    if command:
        if command[0] in modules:
            try:
                try:
                    f = getattr(modules[command[0]], command[1])
                    offset = 2
                except AttributeError:
                    f = modules[command[0]]._all()
                    offset = 1

                return str(f(*command[offset:]))
            except AttributeError:
                resp.message(
                    "⛔️ Command not found in {command[0]} module!")
            except IndexError:
                resp = MessagingResponse()

                # resp.message(f"⚠️ Error - I can't figure out how to do that :(")

                resp.message(
                    "⛔️ Not enough arguments")

                return str(resp)

    # Help command
    resp = MessagingResponse()

    resp.message(
        "Command list coming soon 😳\nFor now, try the search and 8ball commands!")

    return str(resp)


def start():
    modules['search'] = load_module(
        './modules/search.py').module()(client=client)

    modules['8ball'] = load_module(
        './modules/8ball.py').module()(client=client)

    # Send bot started message to default receiver
    # send_message('Bot started!')

    app.run(debug=True)


if __name__ == '__main__':
    start()
