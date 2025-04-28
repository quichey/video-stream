class MyClass:
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        """Getter method for the 'value' attribute."""
        return self._value

    @value.setter
    def value(self, new_value):
        """Setter method for the 'value' attribute."""
        if new_value < 0:
            raise ValueError("Value cannot be negative")
        self._value = new_value

    @value.deleter
    def value(self):
        """Deleter method for the 'value' attribute."""
        del self._value

"""
or dataclasses?
"""

from dataclasses import dataclass

@dataclass
class InventoryItem:
    """Class for keeping track of an item in inventory."""
    name: str
    unit_price: float
    quantity_on_hand: int = 0

    def total_cost(self) -> float:
        return self.unit_price * self.quantity_on_hand


@dataclass
class Point:
     x: int
     y: int

@dataclass
class C:
     mylist: list[Point]

p = Point(10, 20)
assert asdict(p) == {'x': 10, 'y': 20}

c = C([Point(0, 0), Point(10, 4)])
assert asdict(c) == {'mylist': [{'x': 0, 'y': 0}, {'x': 10, 'y': 4}]}



"""
ForeignKeyDataStore needs to have a PrimaryKeyDataStore attribute
to be able to do get_random_foreign_key

PrimaryKeyDataStore does not need to have a ForeignKeyDataStore attribute

Both DataStore need the metadata_tables and ways to get info based off of
table_name passed in

so maybe make dataclasses for each table_name to store pk/fk information
and then @property decorator on FK/PKDataStore classes to...
... retrieve table_name pk/fk dataclasses? no, no @property dec i think.
needs table_name as param

why bother with dataclasses? i suppose it is good for
syntax highlighting the attributes as opposed to tracking down
random dictionary keys/names
"""

@dataclass
class PrimaryKey:
    """Class for keeping track of an item in inventory."""
    table_name: str
    column_name: str
    existing_values: list # TODO: change to List from typing or sumthing

    def update_existing_values(self):
        pass

@dataclass
class ForeignKey:
    """Class for keeping track of an item in inventory."""
    # the FK Column is housed in a table
    home_table_name: str
    home_column_name: str
    # the FK Column references another table
    referenced_table_name: str
    referenced_column_name: str # usually the ref table's PK


# prob don't need this, prob just use python dict now
class DataStore():
    def get_item():
        pass