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
- [Lua](https://www.lua.org/download.html)
- [Twilio](https://www.twilio.com/) account with a phone number
- Public-facing webserver or port forwarding (to make webserver accessible to Twilio)

### Optional Requirements

- [Google Custom Search Engine API Key](docs/google-cse.md) (for search module)

### Dependencies

#### From PyPi/PIP

- [Twillo API](https://pypi.org/project/twilio/)
- [Flask](https://pypi.org/project/Flask/)
- [TOML](https://pypi.org/project/toml/)
- [Rich](https://pypi.org/project/rich/)
- [google-api-python-client](https://pypi.org/project/google-api-python-client/) (for built-in search module)
- [Lupa](https://pypi.org/project/lupa/#building-with-different-lua-versions) (for lua modules)

## Installation

- Clone the repo

```sh
git clone https://github.com/wxllow/twillow
```

- Create a virtual environment
  
```sh
python3 -m venv ./venv
```

- Copy and edit the config file

```sh
cp resources/config.toml config.toml
```

- Run the bot

```sh
python3 main.py
```

## Useful Resources

- [Setting up Google CSE](docs/google-cse.md) (for search module)
- [TwiML™ for Programmable SMS](https://www.twilio.com/docs/messaging/twiml)
- [TwiML™ for Programmable Voice](https://www.google.com/search?q=TwiML&ie=UTF-8)
