import falcon
import subprocess
import os

from src.config import TEMP_FOLDER


def make_response(response, data, status=falcon.HTTP_OK, **kwargs):
    if type(data) not in [dict, list]:
        response.text   = str(data)
    else:
        response.media  = data

    response.status     = status


def run_bash(cmd):
    sp  = subprocess.run(cmd.split(' '), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    r   = sp.stdout.decode('utf-8')
    err = sp.returncode
    return r, err


def halt_if_runbash_failed(run_bash_result):
    output_text, error_code = run_bash_result
    if error_code != 0 :
        raise Exception(f'Failed run_bash()\nError:\n{output_text}')


def run_bash_complex(target_cmd, custom_name=None):
    """
    :complex means some bash commands have piping |, redirect >, etc. that cannot run via run_bash()
    we will right the :target_cmd, i.e the complex bash command, to a bash file and run it
    """
    if custom_name is None:
        custom_name = hash(target_cmd)

    # prepare :sh_file to store :target_cmd
    sh_file_dir = f'{TEMP_FOLDER}/run_bash_complex'
    sh_file     = f'{sh_file_dir}/{custom_name}.sh'  # sh file stored here

    os.makedirs(sh_file_dir, exist_ok=True)  # prepare folder path

    # write :target_cmd to .sh file
    with open(sh_file, 'w') as f:
        f.write(
            f'#!/bin/bash\n'
            f'{target_cmd}'
        )

    # add +x permission to it
    _ = run_bash(f'chmod +x {sh_file}'); halt_if_runbash_failed(_)

    # run the created .sh file
    assert os.path.isfile(sh_file)
    _ = run_bash(sh_file)
    halt_if_runbash_failed(_)
    return _
