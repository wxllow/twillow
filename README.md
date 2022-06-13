# Twillow

A ***work in progress*** modular SMS bot using the Twilio API, written in Python (with modules written in Python or Lua). The name is a combination of Twilio and the creator's name, Willow.

## Features

- Easily extendable/customizable
  - *"Everything is a module"*
  - Modules can be written in Lua or Python
  - Voice handlers can also be written to handle calls
  - Configuration file to make Twillow perfect for you without changing any source code

## Requirements

- [Python 3.9 or later](https://www.python.org/downloads/)
- [Poetry](https://pypi.org/project/poetry/)
- [Lua](https://www.lua.org/download.html)
- [Twilio](https://www.twilio.com/) account with a phone number
- Public-facing webserver or port forwarding (to make webserver accessible to Twilio)

## Installation

- Clone the repo

```sh
git clone https://github.com/wxllow/twillow
cd twillow
```

- Install dependencies
  
```sh
python -m pip install poetry # If you don't already have poetry installed
poetry install
```

- Copy and edit the config file

```sh
cp resources/config.toml config.toml
```

- Run the bot

```sh
poetry run python main.py
```

## Useful Resources

- [Setting up Google CSE](docs/tutorials/google-cse.md) (for search module)
- [Twillow Documentation](https://twillow.wxllow.dev)
- [TwiML™ for Programmable SMS](https://www.twilio.com/docs/messaging/twiml)
- [TwiML™ for Programmable Voice](https://www.google.com/search?q=TwiML&ie=UTF-8)
