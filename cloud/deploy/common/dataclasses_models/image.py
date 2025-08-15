from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Image:
    image_name: str
    image_base_tag: str
    image_full_tag: str = field(init=False)

    def __post_init__(self):
        # Automatically compute the full tag on creation
        timestamp = datetime.utcnow().strftime("%Y-%m-%d--%H-%M-%S")
        self.image_full_tag = f"{self.image_base_tag}-dev-{timestamp}"

    def bump_version(self, new_base_tag: str):
        """Update base tag and refresh full tag with new timestamp."""
        self.image_base_tag = new_base_tag
        timestamp = datetime.utcnow().strftime("%Y-%m-%d--%H-%M-%S")
        self.image_full_tag = f"{self.image_base_tag}-dev-{timestamp}"
