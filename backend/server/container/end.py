import socket
import os, shutil

import util.env as env


def end_command():
    pid = env.get_env("SERVER_PID")
    cmd = f"kill -9 {pid}"
    return cmd

os.system(end_command())

# socket object is a dict?

# save metadata of socket object to bash file