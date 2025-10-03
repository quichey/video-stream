# Database Seeding and Local Testing

The files in this directory (`Seed.py`, `Data_Records.py`, `Data_Base_Structure.py`) are responsible for managing the Data Definition Language (DDL) and Data Manipulation Language (DML). They are used to create the database schema and populate it with test data for local development and integration testing.

The primary execution script is `load_db.py` in the parent directory (`db/`), which is now executed via **Poetry** to ensure the correct environment and dependencies are used.

## 🔑 How to Test the Seed Module Locally

Testing the Seed module locally verifies:

1. Connection logic using the local `DataBaseSpec` (i.e., `localhost`).

2. DDL execution (table creation).

3. DML execution (random data, foreign key lookups, secure token generation).

### Prerequisites

Before running any seed commands, ensure the following steps are complete:

1. **Local MySQL Server:** A local MySQL instance must be running (e.g., via Docker or a local install).

2. **Environment Variables:** Your local `.env` files must be loaded, as the seed module pulls database credentials from them.

### Execution (Command Line Interface)

The `load_db.py` script now uses a Command Line Interface (CLI) to select actions (`seed` or `export`) and testing states (`-s`). All commands must be run from the **Poetry root directory** (`server/`).

| Action | Command | Scenario | Primary Goal |
| :--- | :--- | :--- | :--- |
| **Seed** | `seed -s full` | **Full Load** | Core functional testing and high-volume data performance. |
| **Seed** | `seed -s small` | **Small Load** | Rapid, low-volume integration testing (default). |
| **Seed** | `seed -s users` | **Users Only** | Testing authentication/session stability. |
| **Export** | `export -f regression` | **Export Data** | Saves the current database state to a timestamped `regression_...sql` file. |

#### Examples:

**1. To seed the database with the minimal data set (`small`):**

```bash
poetry run python3 -m db.load_db seed -s small