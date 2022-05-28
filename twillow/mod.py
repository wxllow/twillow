import sys
import importlib.util


def load_module(loc):
    spec = importlib.util.spec_from_file_location(
        "module.{name}", loc)

    module = importlib.util.module_from_spec(spec)

    sys.modules[f"module.{loc.split('/')[-1]}"] = module
    spec.loader.exec_module(module)

    return module
