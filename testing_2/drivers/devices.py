# TODO: handle cloud services/devices

# extract env vars from cloud/providers/azure etc.

# call cloud/deploy/deploy_machines --env test in here?

# should the python module to start/stop cloud services be in here?
# prob not, prob better in cloud/ somewhere, probably deploy?

import subprocess


def run_cmds(cmd_array, **kwargs):
    if type(cmd_array[0]) == str:
        return subprocess.run(cmd_array, **kwargs)
    else:
        for cmd in cmd_array:
            # TODO: what do return for this case?
            subprocess.run(cmd, **kwargs)


SERVICE_LIFECYCLE_SCRIPT_DIR = "cloud/deploy"
SERVICE_LIFECYCLE_SCRIPT_NAME = "service_lifecycle.py"
SERVICE_LIFECYCLE_SCRIPT_LOCATION = (
    f"{SERVICE_LIFECYCLE_SCRIPT_DIR}/{SERVICE_LIFECYCLE_SCRIPT_NAME}"
)
DEPLOY_SCRIPT_NAME = "deploy_machines.py"


class TestInfraManager:
    def deploy(self):
        self._run_deploy_script()

    def start(self):
        self._run_lifecycle_script("start")

    def stop(self):
        self._run_lifecycle_script("stop")

    def restart(self):
        self._run_lifecycle_script("restart", machines=["server"])

    def _run_lifecycle_script(self, action, machines=None):
        run_cmd = [
            "poetry",
            "run",
            "python3",
            SERVICE_LIFECYCLE_SCRIPT_NAME,
            "--env",
            "test",
            "--action",
            action,
        ]
        if machines:
            if "client" in machines:
                run_cmd.append("--client")
            if "server" in machines:
                run_cmd.append("--server")

        run_cmds(run_cmd, cwd=f"../../{SERVICE_LIFECYCLE_SCRIPT_DIR}")

    def _run_deploy_script(self):
        run_cmd = [
            "poetry",
            "run",
            "python3",
            DEPLOY_SCRIPT_NAME,
            "--env",
            "test",
        ]
        run_cmds(run_cmd, cwd=f"../../{SERVICE_LIFECYCLE_SCRIPT_DIR}")
