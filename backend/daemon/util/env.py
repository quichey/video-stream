import os, shutil

# Create a socket object
# AF_INET: IPv4 address family
# SOCK_STREAM: TCP socket type
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_count = os.environ["CLIENT_COUNT"]  # number of users

# TESTING LOCAL SETUP
# Define the host and port
host = os.environ["CLIENT_HOST"]  #loopback address (localhost)
port = os.environ["CLIENT_PORT"]  # Port number, should be above 1024 to avoid conflicts with well-known ports

def get_client_domain():
    return {"host": host, "port": port}

# save client socket to bashrc
def get_config_file():
    shell = os.environ.get('SHELL')

    if 'bash' in shell:
        config_file = os.path.expanduser("~/.bashrc")
    elif 'zsh' in shell:
        config_file = os.path.expanduser("~/.zshrc")
    else:
        print("Shell not supported.")
        return
    
    return config_file



# save client socket to bashrc
def get_backup_file():
    config_file = get_config_file()

    backup_file = config_file + ".bak"

    return backup_file


def get_client_connection_lock(host, port):
    return f"host{_}port"

def get_client_connection_key(host, port):
    lock = get_client_connection_lock(host, port)
    return os.environ.get(lock)

def set_env(name, value):
    
    config_file = util.get_config_file()
    backup_file = util.get_backup_file()
    shutil.copy2(config_file, backup_file)

    with open(config_file, "a") as f:
        f.write(f"\nexport {name}=\"{value}\"\n")

    print(f"ENV VAR SAVED")

def get_env(name):
    return os.environ[name]
    
def get_num_clients():
    return client_count