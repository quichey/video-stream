import argparse
import copy
import db.Schema as Schema
import db.Seed.Seed as Seed
from db.Seed.datasets import (
    TESTING_STATE_FULL,
    TESTING_STATE_SMALL,
    TESTING_STATE_USERS_ONLY,
    TESTING_STATE_SERVER_RESTART,
)

# --- 1. Configuration States & Dialect Mapping ---
# Map argument strings to the actual configuration objects
STATE_MAP = {
    "full": TESTING_STATE_FULL,
    "small": TESTING_STATE_SMALL,
    "users": TESTING_STATE_USERS_ONLY,
    "restart": TESTING_STATE_SERVER_RESTART,
}

# Map simple dialect names to SQLAlchemy dialect/driver pairs
DIALECT_MAP = {
    # Default MySQL configuration
    "mysql": {"dialect": "mysql", "db_api": "pymysql"},
    # Default PostgreSQL configuration
    "postgres": {"dialect": "postgresql", "db_api": "psycopg2"},
    # Add other mappings as needed
}


# --- 2. Main Orchestration Logic ---
def get_seeder_instance(dialect_override: str = None):
    """
    Initializes and returns the DatabaseSeeder instance, applying
    dynamic dialect overrides if specified by the command line.
    """
    # 1. Copy the default specs from Schema to avoid mutating the imported module's state
    admin_specs = copy.deepcopy(Schema.admin_specs)
    database_specs = copy.deepcopy(Schema.database_specs)

    # 2. Apply dialect override if provided
    if dialect_override:
        if dialect_override not in DIALECT_MAP:
            print(f"ERROR: Unknown dialect '{dialect_override}'. Using default specs.")
        else:
            dialect_config = DIALECT_MAP[dialect_override]

            # Update both the main database specs and the admin specs
            database_specs["dialect"] = dialect_config["dialect"]
            database_specs["db_api"] = dialect_config["db_api"]

            admin_specs["dialect"] = dialect_config["dialect"]
            admin_specs["db_api"] = dialect_config["db_api"]

            print(
                f"Using dialect override: {dialect_config['dialect']}+{dialect_config['db_api']}"
            )

    # 3. Instantiate the Seed class with the potentially updated specs
    # The Seed.__init__ will use these dictionaries to create DataBaseSpec dataclass instances.
    return Seed.Seed(admin_specs, database_specs, Schema)


def execute_seeding(seeder: Seed.Seed, state_key: str):
    """Initiates the data generation and insertion process."""
    if state_key not in STATE_MAP:
        print(
            f"ERROR: Unknown state '{state_key}'. Choose from {list(STATE_MAP.keys())}"
        )
        return

    config = STATE_MAP[state_key]
    print(f"Attempting to seed database with '{state_key}' configuration...")

    # This is where your topological sort and insertion logic runs
    seeder.initiate_test_environment(config)
    print(f"✅ Seeding completed for state: {state_key}")


def execute_export(seeder: Seed.Seed, file_name_base: str):
    """Exports the current database state (assumed to be seeded) to a SQL file."""
    print("Attempting to export current database state to SQL file...")

    try:
        file_name = seeder.export_data_to_file(file_name_base)
        print("--- EXPORT SUCCESSFUL ---")
        print(f"File created: {file_name}")
        print("-------------------------")
    except Exception as e:
        print(f"❌ Export failed: {e}")


def main():
    """Parses command-line arguments and executes the requested database operation."""
    parser = argparse.ArgumentParser(
        description="Utility for seeding and exporting the video-stream test database.",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    # Main action argument
    parser.add_argument(
        "action",
        choices=["seed", "export"],
        help="The action to perform: \n 'seed' - Generates and inserts data into the local database. \n 'export' - Dumps the data from the database into a versioned SQL file.",
    )

    # State argument (only relevant for 'seed' action)
    parser.add_argument(
        "-s",
        "--state",
        choices=list(STATE_MAP.keys()),
        default="small",
        help=f"The configuration to use for seeding. Default is 'small'. Choices: {list(STATE_MAP.keys())}",
    )

    # NEW DIALECT ARGUMENT: Allows user to specify the database type at runtime
    parser.add_argument(
        "-d",
        "--dialect",
        choices=list(DIALECT_MAP.keys()),
        default=None,
        help=f"Optional: Override the default database dialect. Choices: {list(DIALECT_MAP.keys())}. If omitted, the default dialect from db.Schema is used.",
    )

    # File name argument (only relevant for 'export' action)
    parser.add_argument(
        "-f",
        "--file_base",
        default="test_seed",
        help="Base name for the exported SQL file (e.g., 'regression_seed'). Default is 'test_seed'.",
    )

    args = parser.parse_args()

    # Pass the dialect override from the arguments to the seeder instance factory
    seeder = get_seeder_instance(args.dialect)

    if args.action == "seed":
        execute_seeding(seeder, args.state)

    elif args.action == "export":
        # NOTE: For export to be useful, you should typically run 'seed' first.
        # Ensure the database is initialized before exporting.
        execute_export(seeder, args.file_base)

    else:
        # Should be caught by argparse choices, but good for defense
        parser.print_help()


if __name__ == "__main__":
    main()
