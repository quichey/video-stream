from dataclasses import dataclass


@dataclass
class TableTestingState:
    """Class for keeping track of an test dataset table generation info."""

    name: str
    num_records: int
