import os
from dotenv import load_dotenv

from flask import Flask, request
from flask_cors import CORS

from api.orchestrator import Orchestrator
from api.Routers import AdminRouter
from api.Routers import ClientRouter

"""
Inject Router functions into this file
to get the functionalities into the correct namespaces
within the Flask App-Server Object.

Learn the exact structure of the Flask app object
and hopefully extend it in a beneficial way



Consider:
-- what operating systems do I want to implement supporting
-------- for now: just Linux
-- what things do I imagine a sys-admin needing to do
-------- shut-down server for cost reasons
-------- spin-up duplicate servers for reliability/speed of transit reasons/locality
-------- clean-up unnecessary logging
-- what information would client machines need
------ what is the work-flow of a client
------ what would the internal state of the gateway/db need to be for the work-flow to function as expected as well as
------------ quickly as possible
------------ and as securely as possible
Some of these responsibilities can be delegated to other sub-programs within this repo
-- sub-programs include folders, python modules, python libs, installed packages within pyproject.toml



"""

load_dotenv()
load_dotenv(dotenv_path="../cloud/providers/azure/.env")
load_dotenv(dotenv_path="env/azure/.env")


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    # Base configs that should hold true no matter what
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
    )

    # TODO: maybe need to update this host for cloud build
    client_url = os.environ.get("CLIENT_APP_URL")
    CORS(
        app,
        resources={r"/*": {"origins": ["http://localhost:3000", client_url]}},
        supports_credentials=True,
    )

    # different optional start-up configs
    # to alter the genetic inheritance if the
    # specific instance
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    print(f"app.instance_path: {app.instance_path}")
    # ensure the instance folder exists
    # setup the machine's
    # operating system
    # to house the entity that is
    # the api_gateway
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    #   Any of the following functions down below
    #   should be able to be invoked by
    #   any allowed entity
    #   such as a client machine
    #   for visiting different routes of the web-app
    #   or a sys-admin for debugging/maintenance/clean-up

    """
    Add Routes.etc to here

    change of plans after trying out python interpreter/ruff checks
    just list out like in docs, but can store all the logic in Routes,
    and keep this file as managing state of whole micro-service/gateway-process
    """
    orchestrator = Orchestrator()

    client_router = ClientRouter(app=app, orchestrator=orchestrator, request=request)
    app.client_router = client_router

    admin_router = AdminRouter(app=app, orchestrator=orchestrator, request=request)
    app.admin_router = admin_router
    """
    @app.route("/getcomments", methods=["POST"])
    def read_comments():
        return router.read_comments()
    """

    """
    Maybe should make 2 Separate Router Classes
    One for video-stream Client APIs
    a separate one for Admin util cmd APIs
    """

    return app
