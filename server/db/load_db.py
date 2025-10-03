import argparse
import db.Schema as Schema
import db.Seed.Seed as Seed
from db.Seed.datasets import (
    TESTING_STATE_FULL,
    TESTING_STATE_SMALL,
    TESTING_STATE_USERS_ONLY,
)

# --- 1. Configuration States ---
# Define the different data load configurations


# Map argument strings to the actual configuration objects
STATE_MAP = {
    "full": TESTING_STATE_FULL,
    "small": TESTING_STATE_SMALL,
    "users": TESTING_STATE_USERS_ONLY,
}


# --- 2. Main Orchestration Logic ---
def get_seeder_instance():
    """Initializes and returns the DatabaseSeeder instance."""
    # Assuming the class has been renamed/refactored to handle the complexity
    # We maintain the structure defined in the original script:
    return Seed.Seed(Schema.admin_specs, Schema.database_specs, Schema)


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

    # Assumes seeder.export_data_to_file is the new method returning (filename, load_cmd)
    try:
        file_name, load_cmd = seeder.export_data_to_file(file_name_base)
        print("--- EXPORT SUCCESSFUL ---")
        print(f"File created: {file_name}")
        print(f"Load Command: {load_cmd}")
        print("-------------------------")
    except Exception as e:
        print(f"❌ Export failed: {e}")
        # Add cleanup logic here if needed


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
        help="The action to perform: \n  'seed' - Generates and inserts data into the local database. \n  'export' - Dumps the data from the database into a versioned SQL file.",
    )

    # State argument (only relevant for 'seed' action)
    parser.add_argument(
        "-s",
        "--state",
        choices=list(STATE_MAP.keys()),
        default="small",
        help=f"The configuration to use for seeding. Default is 'small'. Choices: {list(STATE_MAP.keys())}",
    )

    # File name argument (only relevant for 'export' action)
    parser.add_argument(
        "-f",
        "--file_base",
        default="test_seed",
        help="Base name for the exported SQL file (e.g., 'regression_seed'). Default is 'test_seed'.",
    )

    args = parser.parse_args()

    seeder = get_seeder_instance()

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
