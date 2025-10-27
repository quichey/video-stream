from sqlalchemy import create_engine

from db.Schema import database_specs, database_specs_cloud_sql, Base
from util.deployment import Deployment


def init_engine(deployment="local"):
    if deployment == "local":
        db_specs = database_specs
    elif deployment == "cloud":
        db_specs = database_specs_cloud_sql
    # temporary hotfix based off reading cloud run error logs
    else:
        db_specs = database_specs_cloud_sql
    deployment = deployment
    print(f"\n\n database_specs: {db_specs} \n\n")
    return construct_engine(db_specs, deployment)


def construct_engine(database_specs, deployment):
    if deployment == "local":
        dialect = database_specs["dialect"]
        db_api = database_specs["db_api"]

        user = database_specs["user"]
        pw = database_specs["pw"]
        hostname = database_specs["hostname"]
        dbname = database_specs["dbname"]
        url = f"{user}:{pw}@{hostname}/{dbname}"

        engine = create_engine(f"{dialect}+{db_api}://{url}", echo=True)
    elif database_specs["provider"] == "azure":
        dialect = database_specs["dialect"]
        db_api = database_specs["db_api"]

        user = database_specs["user"]
        pw = database_specs["pw"]
        hostname = database_specs["hostname"]
        dbname = database_specs["dbname"]
        url = f"{user}:{pw}@{hostname}/{dbname}"

        engine = create_engine(f"{dialect}+{db_api}://{url}", echo=True)

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

        engine = create_engine(DATABASE_URI, pool_pre_ping=True)
    return engine


class DataBaseEngine(Deployment):
    _engine = None
    _metadata_obj = Base.metadata

    @property
    def engine(self):
        if self._engine is None:
            self._engine = init_engine(self.deployment)
        return self._engine

    @property
    def metadata_obj(self):
        return self._metadata_obj
