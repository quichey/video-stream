from dataclasses import dataclass
from typing import Optional
from datetime import datetime
import subprocess


from .Data_Base_Structure import Data_Base_Structure
from .Data_Records import Data_Records

# Sketching out blueprint/concepts of Seed class vs Cache class
"""
I want the Seed class to be a wrapper around the sqlalchemy library, to be able to quickly create test data-sets for a given schema.

I want the Cache class to be an internal Encapsulation within the Seed class,
to store any important information of the state of database during the process of populating test data

Why am i doing this?
Auto-populating foreign keys based off the parent table's primary keys is seeming to be difficult.
And this is without handling the case of composite foreign/primary key defs.

But i am unclear of what internal state the Seed class should have as opposed to putting them in the Cache class.
I think the Seed class should have the sqlalchemy constructs/objects, but the cache seems to be using sqlalchemy queries
in order to populate data. This may be fine.
The Seed class mainly has the programs/functions to run on the command-line that actually create the data.
The user of the Seed program should not have to know sqlalchemy queries.

The Seed class can handle the different script options/configs, while the cache class can handle the sqlalchemy calls, when it needs to.
This seems like the Cache class will have a ton of functions.
Should i move it to a different file? I think so.
Pros?
- idk
Cons?
- idk
probably not important

I think what i need to do next is create update_cache_* functions within cache,
or seems just moving over any function with self.cache into cache seems to make more sense.
But I feel lazy right now
"""


@dataclass
class DataBaseSpec:
    """Class for keeping track of sql-alchemy engine creation info."""

    dialect: str
    db_api: str
    user: str
    pw: str
    hostname: str
    dbname: Optional[str] = ""


@dataclass
class TableTestingState:
    """Class for keeping track of an test dataset table generation info."""

    name: str
    num_records: int


# may expand this file to be named snapshot_db
# to draw inspiration from ISS/Clinicomp as well as the
# glorious game Pokemon Snap
# -- ideally i would make functionality to
# - Check if database named video_stream exists
# - - if not, create it with a test user
# - create/load tables with demo-able data
# - prepare indices for optimal searching/fetching for appropriate cases


class Seed:
    database_specs = None
    base = None
    metadata_obj = None

    def __init__(self, admin_specs, database_specs, schema):
        self.admin_specs = DataBaseSpec(**admin_specs)
        self.database_specs = DataBaseSpec(**database_specs)
        self.schema = schema
        self.base = schema.Base
        self.metadata_obj = schema.Base.metadata

        self.data_base_structure_factory = Data_Base_Structure(self)
        self.data_records_factory = Data_Records(self)

    @property
    def engine(self):
        return self._engine

    @engine.setter
    def engine(self, new_value):
        if new_value is None:
            raise ValueError("Value cannot be None")
        self._engine = new_value

    def get_table_metadata(self, table_name):
        return self.metadata_obj.tables[table_name]

    def parse_test_data_file(self):
        # first row is table name
        # second row is columns names
        # determine the delimiter
        # construct list of dictionary records
        pass

    def fill_table_with_test_data(self, table_name, test_file):
        pass

    # fill in tables with given test data
    # TODO: update, i think create TableTestState instances here or in load_db.py
    def initiate_test_environment(self, testing_state):
        print(f"testing_state: {testing_state}")
        list_of_table_files = testing_state.get("table_files", {})
        for file in list_of_table_files:
            table_data = self.parse_test_data_file(file)
            print(f"table_data: {table_data}")
        list_of_table_rand = testing_state["tables_random_populate"]
        test_table_states = [
            TableTestingState(**test_table_info)
            for test_table_info in list_of_table_rand
        ]

        self.data_base_structure_factory.init_ddl()
        self.data_records_factory.init_table_data(test_table_states)

    def export_data_to_file(self, file_name_base="video_stream") -> str:
        # ASSUME INITIATE_test_environment as been run alrady
        file_extension = self.determine_ext()
        version_num = datetime.now().strftime("%Y%m%d%H%M%S")
        file_name = f"{file_name_base}_{version_num}_.{file_extension}"
        db_engine_export_cmd = self._get_load_cmd(file_name)
        # Note: subprocess.run expects the command as a list of strings for security,
        # but for simple shell redirects (mysqldump > file), passing a single string
        # with shell=True is simpler and often used in this context.
        # We'll use the string format here.
        subprocess.run(db_engine_export_cmd, shell=True, check=True)
        return file_name

    def determine_ext(self) -> str:
        return "sql"

    def _get_load_cmd(self, file_name: str) -> str:
        # Get the dialect from your SQLAlchemy engine/configuration
        dialect = self.engine.dialect.name

        specs = self.database_specs

        if "postgresql" in dialect:
            # PostgreSQL dump command using the pg_dump client
            # Example: pg_dump -h <host> -U <user> -d <db_name> > <file_name>
            return f"pg_dump -h {specs.hostname} -U {specs.user} -d {specs.dbname} > {file_name}"

        elif "mysql" in dialect:
            # MySQL dump command using the mysqldump client
            # Command structure: mysqldump -u <user> -h <host> -P <port> -p<pw> <db_name> > <file_name>

            user = specs.user
            pw = specs.pw
            # Safely extract host and port
            host_parts = specs.hostname.split(":")
            host = host_parts[0]
            port = host_parts[1] if len(host_parts) > 1 else "3306"
            db_name = specs.dbname

            # Using -p<password> for non-interactive execution with subprocess.run
            # Warning is expected, but necessary for automation.
            return f"mysqldump -u {user} -h {host} -P {port} -p'{pw}' {db_name} > {file_name}"

        elif "mssql" in dialect or "azure" in dialect:
            # Azure SQL Database / MSSQL (using the sqlcmd utility for EXPORT is complex,
            # often a different utility or a script is needed). Placeholder for now.
            return "ERROR: MSSQL export not yet supported by shell command logic."

        else:
            return (
                f"ERROR: Unsupported dialect '{dialect}' for generating dump command."
            )


# ideas for testing state
# fill up users table with random data since it does not have foreign keys
# and then view contents
# and then write up test files for other tables using id's from this table
# -- possibly add in a case in create_random_data where it checks if the column
# -- is a foreign key, and then scan the parent table for a proper id
