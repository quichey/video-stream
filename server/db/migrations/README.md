# 💾 Database Migrations (Alembic)

This project uses **Alembic** to manage database schema changes. The configuration is set up to read the critical database URL from the **`DB_URL`** environment variable.

---

## ⚙️ Setup & Configuration

### 1. Configure the DB URL

The connection string is read from the `DB_URL` environment variable, which is loaded from `server/db/migrations/.env`.

* **Action:** Copy the example file and update the `DB_URL` for your environment.

    ```bash
    cp server/db/migrations/.env.example server/db/migrations/.env
    # Edit server/db/migrations/.env with your DB connection string
    ```

### 2. Run Commands

All Alembic commands must be run from the **`server` directory** (where `alembic.ini` is located).

---

## 🚀 Alembic Command Line Usage

| Command | Purpose | Example |
| :--- | :--- | :--- |
| **Generate** | Creates a new migration script based on model changes in `db/Schema/Models.py`. | `alembic revision --autogenerate -m "add user role"` |
| **Upgrade** | Applies pending migration scripts to the database. | `alembic upgrade head` |
| **Downgrade** | Reverts the last applied migration. | `alembic downgrade -1` |
| **Current** | Shows the revision ID of the latest migration applied to the database. | `alembic current` |
| **History** | Shows the entire revision history. | `alembic history` |

---

## 🛠️ Handling Existing Databases (Stamping)

If a database already has the required schema, running `alembic upgrade head` will cause errors.

Use the **`stamp`** command to manually update the database's version tracker **without running any migrations.**

* **Initial Schema Stamping:**
    ```bash
    # Stamp the DB as being at the initial commit (6954f76c47c2)
    alembic stamp 6954f76c47c2
    ```
* **Up-to-Date Stamping:**
    ```bash
    # Stamp the DB as being fully up-to-date with the latest revision
    alembic stamp head
    ```

## commands
video-stream/server/# poetry run alembic ...