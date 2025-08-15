from dataclasses import dataclass, field

@dataclass
class Image:
    name: str
    repo_name: str = field(init="")
    base_tag: str = field(init="")
    full_tag: str = field(init="")

