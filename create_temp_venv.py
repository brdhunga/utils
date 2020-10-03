#!/usr/bin/env python3

import pathlib
import string
import subprocess
import tempfile
import venv
import random
import logging


SCRIPT_TEMPLATE = '''\
#!${venv_executable}

import requests
print(requests)
'''

logging.basicConfig(level=logging.INFO, format='%(asctime)s :: %(levelname)s :: %(message)s')


def get_temp_venv_dir_name() -> str:
    _random_name= "".join(random.sample('abcdefghijklmnopqrstuvwxyz123456789', 5))
    return f"venv_{_random_name}"


class EnvBuilder(venv.EnvBuilder):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.context = None

    def post_setup(self, context):
        self.context = context

def main():
    target_dir_path = get_temp_venv_dir_name()
    logging.basicConfig(" *** Created temporary directory '{target_dir_path}'.")
    #
    print(f" *** Creating virtual environment...")
    venv_builder = EnvBuilder(with_pip=True)
    venv_builder.create(str(target_dir_path))
    venv_context = venv_builder.context
    #
    requirements = [
        'requests',
    ]
    print(f" *** Installing {requirements}...")
    pip_install_command = [
        venv_context.env_exe,
        '-m',
        'pip',
        'install',
        *requirements,
    ]
    subprocess.check_call(pip_install_command)
    #
    logging.basicConfig(" *** Generating script...")
    script_substitutions = {
        'venv_executable': venv_context.env_exe,
    }
    script = (
        string.Template(SCRIPT_TEMPLATE).substitute(script_substitutions)
    )
    logging.basicConfig(" *** Generated script:")
    logging.basicConfig("'''")
    logging.basicConfig(script)
    logging.basicConfig("'''")
    #
    script_path = pathlib.Path(target_dir_path).joinpath('run.py')
    logging.basicConfig(f" *** Writing script '{script_path}'")
    script_path.write_text(script)
    #
    logging.basicConfig(" *** Executing script...")
    script_command = [
        venv_context.env_exe,
        str(script_path),
    ]
    subprocess.check_call(script_command)

if __name__ == '__main__':
    main()
