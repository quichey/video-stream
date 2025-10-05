import subprocess
import time
import platform
from typing import Optional


def run_cmds(cmd_array, **kwargs):
    if type(cmd_array[0]) == str:
        return subprocess.run(cmd_array, **kwargs)
    else:
        for cmd in cmd_array:
            # TODO: what do return for this case?
            subprocess.run(cmd, **kwargs)


def run_cmd_with_retries(cmd, retries=5, delay=5, check=True):
    """
    Run a command with retries.

    Args:
        cmd (list): Command list for subprocess.run.
        retries (int): Number of retries before failing.
        delay (int): Seconds to wait between retries.
        check (bool): Whether to raise on non-zero exit.

    Returns:
        CompletedProcess object if successful.

    Raises:
        subprocess.CalledProcessError after all retries fail.
    """
    last_exception = None
    for attempt in range(1, retries + 1):
        try:
            print(f"Attempt {attempt}: Running command: {' '.join(cmd)}")
            result = subprocess.run(cmd, check=check, capture_output=True, text=True)
            print(result.stdout)
            return result
        except subprocess.CalledProcessError as e:
            print(f"Attempt {attempt} failed with error: {e.stderr or e}")
            last_exception = e
            if attempt < retries:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                print("All retries failed.")
                raise last_exception


def run_shell_command(
    command: str, check: bool = True, shell: bool = False
) -> Optional[str]:
    """
    Runs a shell command and returns the output or None on failure.

    Args:
        command: The shell command string.
        check: If True, raises a CalledProcessError on non-zero exit code.
        shell: If True, the command is executed through the shell.
    """
    try:
        # Using subprocess.run for simplicity and reliability
        print(f"-> Executing command: {command}")
        result = subprocess.run(
            command, check=check, shell=shell, capture_output=True, text=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {command}")
        print(f"Stderr: {e.stderr}")
        if check:
            raise
        return None
    except FileNotFoundError:
        return None


def get_os_type() -> str:
    """Returns the main OS type (e.g., 'Darwin' for macOS, 'Linux', 'Windows')."""
    return platform.system()
