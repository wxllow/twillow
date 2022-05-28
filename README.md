# Twillow

A modular SMS bot using the Twilio API, written in Python (with modules written in lua). The name is a combination of Twilio and the creator's name, Willow.

## Features

- Easily extendable/customizable
  - *"Everything is a module"*
  - Modules can be written in Lua or Python
  - Configuration file to make Twillow perfect for you

## Requirements

- Python 3.9 or later
- Twillo account with a phone number
- Public-facing webserver or port forwarding (to make webserver accessible to Twilio)
- [Google Custom Search Engine API Key](docs/google-cse.md)

### Dependencies

#### From PyPi/PIP

- [Twillo API](https://pypi.org/project/twilio/)
- [Flask](https://pypi.org/project/Flask/)
- [TOML](https://pypi.org/project/toml/)
- [Rich](https://pypi.org/project/rich/)
- [google-api-python-client](https://pypi.org/project/google-api-python-client/) (for built-in search module)
- [Lupa](https://pypi.org/project/lupa/#building-with-different-lua-versions) (for lua modules)

#### External

- [Lua](https://www.lua.org/download.html)

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
