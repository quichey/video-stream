import subprocess
import time


class CloudError(Exception):
    pass


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
    for attempt in range(1, retries + 1):
        try:
            print(f"Attempt {attempt}: Running command: {' '.join(cmd)}")
            result = subprocess.run(cmd, check=check, capture_output=True, text=True)
            print(result.stdout)
            return result
        except subprocess.CalledProcessError as e:
            print(f"Attempt {attempt} failed with error: {e.stderr or e}")
            if attempt < retries:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                print("All retries failed.")
                raise CloudError
