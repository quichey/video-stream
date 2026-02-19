# 📄 Deployment Developer Notes

## 🏗️ Architecture Overview
The deployment system uses a **Mixin-Provider-Deployer** pattern to maintain clean separation of concerns:

* **Deployers (e.g., `ClientDeployer`, `BaseDBDeployer`):** Orchestrate high-level steps (verify environment, build, launch).
* **Mixins (e.g., `CloudDBMixin`):** Bridges the deployer to the cloud provider, handling conditional logic like "is this the first deploy?".
* **Providers (e.g., `AzureMySQLDBProvider`):** Contains the raw platform-specific CLI command lists.

---

## 🚀 Database Deployment Lifecycle (`BaseDBDeployer`)
The database provisioning follows a strict sequence to ensure idempotent deploys:

1.  **Engine Check (`is_first_deploy`):** Runs `az mysql flexible-server show`.
    * **Success (0) + Valid JSON:** Server exists; proceed to update/migrations.
    * **Exit Code 3 (ResourceNotFound):** Server missing; trigger "First Deploy" provisioning.
    * **Other Exit Code:** Auth error or API failure—**Fast Fail** (Crashes script to prevent duplicate resources).
2.  **Provision Engine:** Creates the physical MySQL instance in Azure.
3.  **Create Schema:** Creates the specific database within that engine.
4.  **Seed & Stamp:**
    * **Seeding:** Pipes `seeded_db.sql` into the host using `mysql` CLI redirection (`<`).
    * **Alembic Stamp:** Critical! Marks the cloud DB at revision `6954f76c47c2` so Alembic knows the schema is already initialized.

---

## 🐚 Execution Rules (`subprocess_helper.py`)
Selection of the `shell` argument depends on whether we need OS-level features like pipes or redirections.

| Command Type | `shell` Mode | Reason |
| :--- | :--- | :--- |
| **Azure CLI (`az`)** | `False` | Passed as a `list`. Safer and avoids shell injection. |
| **SQL Seeding (`<`)** | `True` | Required for the `<` file redirection symbol. |
| **Migrations (`&&`)** | `True` | Required to chain directory changes (`cd`) with commands. |

---

## ⚠️ Robust Resource Checking
We do not rely solely on Azure CLI exit codes because of known inconsistencies (e.g., `az` returning 0 for empty lists). Our `check_resource_exists` helper validates:
1.  **Exit Code:** Must be `0`.
2.  **Output Content:** Output must not be empty, `[]`, or `null`.
*If these fail but the exit code isn't 3, the script raises a `CalledProcessError` to stop the deploy.*

---

## 🛠️ Common Manual Sanity Checks (WSL)
If automation fails, use these commands in WSL to verify the cloud state:

```bash
# Verify if the MySQL Engine exists
az mysql flexible-server show -g <resource-group> -n <server-name>

# Verify if the specific Database Schema exists
az mysql flexible-server db show -g <resource-group> -s <server-name> -d <db-name>

# Check connectivity (Requires Public Access 0.0.0.0 or Firewall rule)
mysql -h <host> -u <admin> -p