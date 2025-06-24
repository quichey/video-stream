from CloudMachine.config import CloudConfig

class Deploy():
    def __init__(self, config: CloudConfig):
        self.config = config
        return

    """
    ssh into cloud instance?
    """
    def _connect_to_cloud(self):
        pass

    def run(self):
        self._connect_to_cloud()
        self.build_packages()
        self.start_daemon()
        pass

    def build_packages(self):
        pass

    def start_daemon(self):
        pass