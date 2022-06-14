import toml


def get_config() -> dict:
    """Get config (dict)"""
    return toml.load("./config.toml")
