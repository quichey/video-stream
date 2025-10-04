import subprocess
from datetime import datetime
from typing import List

# Renamed run_mysqldump_export to _run_mysql_export and removed the dead code
# from the old _get_load_cmd approach.


class Export:
    def __init__(self, seed):
        self.seed = seed
        self.engine = seed.engine
        self.database_specs = seed.database_specs

    def determine_ext(self) -> str:
        return "sql"

    def export_data_to_file(self, file_name_base="video_stream") -> str:
        """Determines the appropriate dump command and executes it safely."""

        file_extension = self.determine_ext()
        version_num = datetime.now().strftime("%Y%m%d%H%M%S")
        file_name = f"{file_name_base}_{version_num}.{file_extension}"

        dialect = self.engine.dialect.name
        specs = self.database_specs

        # --- LOGIC CORRECTION HERE ---
        # Instead of building a shell string, we call the specific robust function
        # that handles subprocess in list format and separates stdout/stderr.
        if "mysql" in dialect:
            # Safely extract host and port
            host_parts = specs.hostname.split(":")
            host = host_parts[0]
            # Use the port if provided, otherwise default to 3306
            port = host_parts[1] if len(host_parts) > 1 else "3306"

            success = self._run_mysql_export(
                output_file=file_name,
                user=specs.user,
                password=specs.pw,
                db_name=specs.dbname,
                host=host,
                port=port,
            )
            if not success:
                # Raise an error or return an error indicator if the export failed
                # The details are already printed by _run_mysql_export
                raise RuntimeError(
                    "MySQL database export failed. See logs for details."
                )
            return file_name

        elif "postgresql" in dialect:
            # PostgreSQL dump command using the pg_dump client (Still using shell=True for now)
            # You may want to refactor this using a list-based subprocess.run like MySQL's
            cmd = f"pg_dump -h {specs.hostname} -U {specs.user} -d {specs.dbname} > {file_name}"
            print(f"Executing PostgreSQL dump: {cmd}")
            subprocess.run(cmd, shell=True, check=True)
            return file_name

        elif "mssql" in dialect or "azure" in dialect:
            raise NotImplementedError(
                "MSSQL export not yet supported by shell command logic."
            )

        else:
            raise ValueError(
                f"Unsupported dialect '{dialect}' for generating dump command."
            )

    def _get_mysql_command_list(self, user, password, db_name, host, port) -> List[str]:
        """Constructs the command list for safe execution of mysqldump."""
        # Using -p<password> for non-interactive execution, which triggers the warning
        return [
            "mysqldump",
            f"--user={user}",
            f"--password={password}",  # This is the source of the warning
            f"--host={host}",
            f"--port={port}",
            db_name,
        ]

    def _run_mysql_export(
        self,
        output_file: str,
        user: str,
        password: str,
        db_name: str,
        host: str,
        port: str,
    ) -> bool:
        """
        Safely runs the mysqldump command using list syntax and handles I/O redirection.
        This is the robust implementation to fix the original 'too many values to unpack' error.
        """
        command_list = self._get_mysql_command_list(user, password, db_name, host, port)

        print(f"Attempting to export current database state to SQL file: {output_file}")
        print(f"Executing: {' '.join(command_list)} > {output_file}")

        try:
            # 2. Execute the command
            # Redirect stdout (the dump data) directly to the file
            with open(output_file, "w") as f:
                result = subprocess.run(
                    command_list,
                    stdout=f,  # Redirect successful output directly to the file
                    stderr=subprocess.PIPE,  # Capture error/warning messages separately
                    check=True,  # Raise CalledProcessError for non-zero exit codes
                    text=True,  # Decode stdout/stderr as text
                )

            # 3. Handle Warnings (Sent to stderr)
            if result.stderr:
                print("\n--- mysqldump STDOUT/STDERR Capture ---")
                # The password warning is often sent to stderr.
                if "warning" in result.stderr.lower():
                    print(
                        f"⚠️ Export completed with warnings (non-critical): \n{result.stderr.strip()}"
                    )
                else:
                    # If there was actual error output on stderr, print it clearly.
                    print(
                        f"❌ Export completed with Errors on stderr: \n{result.stderr.strip()}"
                    )
                print("---------------------------------------")

            print(f"✅ Database successfully exported to {output_file}.")
            return True

        except subprocess.CalledProcessError as e:
            print(f"❌ Export failed due to command error. Return code: {e.returncode}")
            # If the failure was due to the command itself, the output is in e.stderr
            print(f"Error output: {e.stderr}")
            return False
        except FileNotFoundError:
            print(
                "❌ Export failed: 'mysqldump' command not found. Is MySQL installed and in your PATH?"
            )
            return False
