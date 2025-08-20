from sqlalchemy import create_engine

from db.Schema import database_specs, database_specs_cloud_sql, Base
#from api.Cache.SessionManagement import SessionManagement

class StateModule:
    def __init__(self, request, response, deployment):
        self.listeners = {}
        self.init_engine(deployment=deployment)

    def init_engine(self, deployment="local"):
        if deployment == "local":
            self.database_specs = database_specs
        elif deployment == "cloud":
            self.database_specs = database_specs_cloud_sql
        # temporary hotfix based off reading cloud run error logs
        else:
            self.database_specs = database_specs_cloud_sql
        self.deployment = deployment
        print(f"\n\n self.database_specs: {self.database_specs} \n\n")
        self.metadata_obj = Base.metadata
        self.construct_engine(self.database_specs) 
    
    def construct_engine(self, database_specs):
        if self.deployment == "local": 
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

        #Google cloud run deployment
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
        self.engine = engine
        return engine


    def on_event(self, event_name, callback):
        if event_name not in self.listeners:
            self.listeners[event_name] = []
        self.listeners[event_name].append(callback)

    def emit(self, event_name, data):
        if event_name in self.listeners:
            for callback in self.listeners[event_name]:
                callback(data)
