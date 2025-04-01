import os

from flask import Flask

from api.Cache import Cache
from api.Router import Router

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
    

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    # Base configs that should hold true no matter what
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    # different optional start-up configs
    # to alter the genetic inheritance if the
    # specific instance
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

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
    cache = Cache()
    router = Router(cache=cache)
    app.router = router
    def construct_routes():
        # Routes.get_route_signatures ?
        routes = router.get_route_signatures()

        counter = 0
        for python_func, name, http_methods in routes:
            # i think need to use getattr/setattr
            # to dynamically add functions to this app object
            # while decorating it with @app.route
            # iirc, python decorators are functions
            # that wrap the func below within it
            # the inner_func is one of the params
            # and the following params are the accepted arguments?
            """
            @app.route(name, http_methods)
            route_func = python_func
            """

            """
            @app.route(name, http_methods)(python_func)
            """
            #temp_func_name = f"route_func_{counter}"
            app.temp_func_name = app.route(name, http_methods)(python_func)
            counter = counter + 1
            """
            possibly for sys-admin stuff,
            store a hashmap from python func name to cached app.func_name
            in case you run into something odd and need
            to take down just a few routes or something
            """
        
        return app
    #construct_routes()
    @app.route("/getcomments", methods=["POST"])
    def read_comments():
        return router.read_comments()

    return app