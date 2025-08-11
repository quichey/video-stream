import subprocess

def run_cmds(cmd_array, check=True):
    if type(cmd_array[0]) == str:
        subprocess.run(cmd_array, check=check)
    else:
        for cmd in cmd_array:
            subprocess.run(cmd, check=check)