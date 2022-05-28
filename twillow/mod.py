import sys
import os
import importlib.util
import lupa
from lupa import LuaRuntime


def load_module(loc, type=None):
    """Load module, returns module class"""
    if not type:
        if loc.endswith('.py'):
            type = 'py'
        else:
            type = 'lua'

    if type == 'py':
        name = os.path.split(loc)[-1].split('.')[0]

        # Load module
        spec = importlib.util.spec_from_file_location(
            f"module.{name}", loc)

        py_module = importlib.util.module_from_spec(spec)

        spec.loader.exec_module(py_module)

        module = py_module.module()

        # Return module
        if 'name' in dir(module):
            name = str(module.name)

        return name, module()
    else:
        # Execute lau module from file
        lua = LuaRuntime(unpack_returned_tuples=True)

        with open(loc, 'r') as f:
            lua.execute(f.read())

        g = lua.globals()

        # Return module
        module = g.module()
        name = module.name or os.path.split(loc)[-1].split('.')[0]

        return name, module.new()
