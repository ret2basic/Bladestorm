#!/usr/bin/env python3
import argparse
import importlib
from pathlib import Path
import sys

# Command-line arguments setup
parser = argparse.ArgumentParser(description="PCTF automation")
command_parser = parser.add_subparsers(dest="command", metavar="command")
command_parser.required = True

def load_modules():
    # Find all .py files in the ./modules subdirectory
    modules = [
    "./modlues/simplecalc.py",
    ]

    for module in modules:

        try:
            # Import module
            module_name = f"modules.{Path(module).stem}"
            imported_module = importlib.import_module(module_name)

            # Parse the imported module
            cmd = command_parser.add_parser(imported_module.name(), help=imported_module.help())
            cmd.set_defaults(func=imported_module.run)
            for arg in imported_module.args():
                cmd.add_argument(arg)

        except:
            # Exception handling in case module fails loading
            e = sys.exc_info()[0]
            print(f"Failed to import module {module}")
            print(f"Exception: {e}")

def main():

    load_modules()

    # Parse arguments
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
