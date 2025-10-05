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
