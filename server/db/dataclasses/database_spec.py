from dataclasses import dataclass
from typing import Optional


@dataclass
class DataBaseSpec:
    """Class for keeping track of sql-alchemy engine creation info."""

    dialect: str
    db_api: str
    user: str
    pw: str
    hostname: str
    dbname: Optional[str] = ""
