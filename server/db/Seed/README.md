# Database Seeding and Local Testing

The files in this directory (`Seed.py`, `Data_Records.py`, `Data_Base_Structure.py`) are responsible for managing the Data Definition Language (DDL) and Data Manipulation Language (DML). They are used to create the database schema and populate it with test data for local development and integration testing.

The primary execution script is `load_db.py` in the parent directory (`db/`), which imports the `Seed` module and runs one of the curated test scenarios.

## 🔑 How to Test the Seed Module Locally

Testing the Seed module locally verifies:
1.  Connection logic using the local `DataBaseSpec` (i.e., `localhost`).
2.  DDL execution (table creation).
3.  DML execution (random data, foreign key lookups, secure token generation).

### Prerequisites

Before running any seed commands, ensure the following steps are complete:

1.  **Local MySQL Server:** A local MySQL instance must be running (e.g., via Docker or a local install).
2.  **Environment Variables:** Your local `.env` files must be loaded, as the seed module pulls database credentials from them.

### Execution

The `load_db.py` script contains predefined testing states that control how much data is populated.

| Test Script | Scenario | Tables Populated | Primary Goal |
| :--- | :--- | :--- | :--- |
| `run()` | **Full Load** | Users, Videos, Comments, etc. | Core functional testing and high-volume data performance. |
| `run_small()` | **Small Load** | Minimal Users, Videos, Comments. | Rapid, low-volume integration testing. |
| `run_users()` | **Users Only** | Users (and necessary child tables, e.g., UserCookies). | Testing authentication/session stability (your new **Session Stability** scenario). |

To run a specific scenario, execute `load_db.py` and call the corresponding function (e.g., `run_small`):

```bash
# Example: Run the small test data set
# Ensure you are executing from the project root directory
python3 db/load_db.py run_small