from dataclasses import dataclass

@dataclass
class Image:
    registry: str
    repository: str
    tag: str

    @property
    def path(self):
        return f"{self.registry}/{self.repository}"

    @property
    def full_name(self):
        return f"{self.path}:{self.tag}"
