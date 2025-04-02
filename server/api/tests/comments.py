import pytest
import time
from flask import request

from api import create_app

@pytest.fixture()
def initiate_test_user():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    # get info of test_user
    test_user = pass
    # include info in yield
    app_info = {
        "client": app,
        "test_user": test_user
    }
    yield app_info

    # clean up / reset resources here

def extract_token(response):
    pass # TODO: get token

def get_first_page(client):
    response = client.post(
        "/getcomments",
        options={
            "data": {
                "user_id": 0,
                "user_name": "test_user"
            }
        }
    )
    num_comments = len(response.data)
    assert num_comments > 0
    assert num_comments < 1000
    # assert the session token is either
    # returned here or the login
    # http request
    token = extract_token(response)
    yield token

    # when I add into Seed module
    # the code for instantiating 
    # a consistent testing database
    # ensure the num_comments == size_of_first_page


def get_next_page(client, token):
    start_time = pass # TODO: get time_delta_start
    response = client.post(
        "/getcomments",
        options={
            "data": {
                "user_id": 0,
                "user_name": "test_user",
                "token": token
            }
        }
    )
    num_comments = len(response.data)
    assert num_comments > 0
    assert num_comments < 1000
    # assert page size is less than first page

    # assert the session token is either
    # returned here or the login
    # http request
    token = extract_token(response)
    time_delta = pass # TODO: get time_delta
    results = {
        "time_delta": time_delta,
        "token": token
    }
    yield results



"""
May use this context manager
as a quick means of running through all tests
in the order in which they should be applied (imperative programming paradigm)
"""
with app.test_request_context('/getcomments', method='POST'):
    # now you can do something with the request until the
    # end of the with block, such as basic assertions:
    assert request.path == '/getcomments'
    assert request.method == 'POST'

    app_info = initiate_test_user()
    test_user = app_info["test_user"]
    token = get_first_page(client)
    num_pages_to_test = 10
    for i in range(num_pages_to_test):
        # TODO: assert latencies of each request
        results = get_next_page(client, token)
        time_delta = results["time_delta"]
        assert time_delta < 100 #TODO: determine appropriate threshold
        assert results["token"] == token
        # Possible scalability/security measure
        # switch token every request
        # WAAAY down the line
