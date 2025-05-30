from dataclasses import dataclass

@dataclass
class Addr():
    hostname: str
    port: int

@dataclass
class CloudConfig():
    service: str
    addr: Addr
    id: int