from typing import override
from Deploy import Deploy

class Server(Deploy):
    
    @override
    def build_packages(self):
        return super().build_packages()
    @override
    def start_daemon(self):
        return super().start_daemon()