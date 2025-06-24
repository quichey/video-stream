from dataclasses import dataclass

import paramiko


@dataclass
class Credentials():
    hostname: str = 'YOUR_VM_EXTERNAL_IP'
    username: str = 'YOUR_USERNAME' # This is typically your Google Cloud username or the username associated with your SSH key

    # Path to your private SSH key
    private_key_path: str = '~/.ssh/google_cloud_key'

class Connection():
    def __init__(self, cred: Credentials):
        self.cred = cred
        return

    def connect(self):
        private_key_path = self.cred.private_key_path
        hostname = self.cred.hostname
        username = self.cred.username
        try:
            # Create an SSH client
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) # Be cautious with AutoAddPolicy in production

            # Load the private key
            private_key = paramiko.RSAKey.from_private_key_file(private_key_path)

            # Connect to the VM
            client.connect(hostname=hostname, username=username, pkey=private_key)

            # Execute a command
            stdin, stdout, stderr = client.exec_command('ls -l /')

            # Print the output
            print("STDOUT:")
            print(stdout.read().decode())
            print("STDERR:")
            print(stderr.read().decode())

        except paramiko.AuthenticationException:
            print("Authentication failed. Check your username, private key, and VM's SSH key configuration.")
        except paramiko.SSHException as e:
            print(f"SSH connection error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            if client:
                client.close()