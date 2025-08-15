from dataclasses import dataclass, field

@dataclass
class Container:
    name: str
    id: str = field(init="")
