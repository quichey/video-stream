from db.dataclasses.database_spec import DataBaseSpec


def translate_to_object(database_specs):
    return DataBaseSpec(**database_specs)


def get_db_conn_str(database_specs):
    dialect = database_specs.dialect
    db_api = database_specs.db_api

    user = database_specs.user
    pw = database_specs.pw
    hostname = database_specs.hostname
    dbname = database_specs.dbname
    url = f"{dialect}+{db_api}://{user}:{pw}@{hostname}"
    if dbname != "":
        url += f"/{dbname}"
    return url


def construct_conn_str_any(database_specs, deployment):
    if deployment == "local":
        dialect = database_specs["dialect"]
        db_api = database_specs["db_api"]

        user = database_specs["user"]
        pw = database_specs["pw"]
        hostname = database_specs["hostname"]
        dbname = database_specs["dbname"]
        url = f"{dialect}+{db_api}://{user}:{pw}@{hostname}/{dbname}"
        DATABASE_URI = url
    elif database_specs["provider"] == "azure":
        dialect = database_specs["dialect"]
        db_api = database_specs["db_api"]

        user = database_specs["user"]
        pw = database_specs["pw"]
        hostname = database_specs["hostname"]
        dbname = database_specs["dbname"]
        url = f"{user}:{pw}@{hostname}/{dbname}"

        DATABASE_URI = f"{dialect}+{db_api}://{url}"

    # Google cloud run deployment
    else:
        DB_USER = database_specs["user"]
        DB_PASS = database_specs["pw"]
        DB_NAME = database_specs["dbname"]
        CLOUD_SQL_CONNECTION_NAME = database_specs["CLOUD_SQL_CONNECTION_NAME"]

        # Unix socket path (Cloud Run mounts /cloudsql)
        unix_socket_path = f"/cloudsql/{CLOUD_SQL_CONNECTION_NAME}"

        # SQLAlchemy connection URL (note: use pymysql)
        DATABASE_URI = (
            f"mysql+pymysql://{DB_USER}:{DB_PASS}@/{DB_NAME}"
            f"?unix_socket={unix_socket_path}"
        )

    return DATABASE_URI
