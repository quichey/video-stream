from dataclasses import dataclass, field

@dataclass
class Image:
    name: str
    base_tag: str = field(init="")
    full_tag: str = field(init="")

