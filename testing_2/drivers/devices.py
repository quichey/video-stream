# TODO: handle cloud services/devices

# extract env vars from cloud/providers/azure etc.

# call cloud/deploy/deploy_machines --env test in here?

# should the python module to start/stop cloud services be in here?
# prob not, prob better in cloud/ somewhere, probably deploy?

SERVICE_LIFECYCLE_SCRIPT_DIR = "cloud/deploy"
SERVICE_LIFECYCLE_SCRIPT_NAME = "service_lifecycle.py"
SERVICE_LIFECYCLE_SCRIPT_LOCATION = (
    f"{SERVICE_LIFECYCLE_SCRIPT_DIR}/{SERVICE_LIFECYCLE_SCRIPT_NAME}"
)


class TestInfraManager:
    def start(self):
        self._run_lifecycle_script("start")

    def stop(self):
        self._run_lifecycle_script("stop")

    def _run_lifecycle_script(self, action):
        cd_cmd = f"cd {SERVICE_LIFECYCLE_SCRIPT_DIR}"

        run_cmd = f"poetry run python3 {SERVICE_LIFECYCLE_SCRIPT_NAME} --env test --action {action}"
