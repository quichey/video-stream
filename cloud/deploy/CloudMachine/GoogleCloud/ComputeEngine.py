from CloudMachine import CloudConfig, Addr

class ComputeEngine():
    def __init__(self):
        self.addr = Addr(
            hostname="temp",
            port="temp"
        )
        self.config = CloudConfig(
            service="Google_compute_engine",
            addr=self.addr,
            id="temp"
        )