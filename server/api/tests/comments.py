import pytest
import time
from datetime import timedelta, date, datetime
from flask import request

from api import create_app

@pytest.fixture()
def initiate_test_user():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    # get info of test_user
    test_user = 0
    # include info in yield
    app_info = {
        "client": app,
        "test_user": test_user
    }
    yield app_info

    # clean up / reset resources here

def extract_token(response):
    pass # TODO: get token

def package_session_info(user):
    data = {
        "data": {
            "user_id": 0,
            "user_name": user
        }
    }
    return data

def get_first_page(client, user):
    response = client.post(
        "/getcomments",
        json=package_session_info(user)
    )
    data = response.json["data"]
    num_comments = len(data)
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


def get_next_page(client, token, user):
    start_time = datetime.now()
    response = client.post(
        "/getcomments",
        json=package_session_info(user)
    )
    data = response.json["data"]
    num_comments = len(data)
    assert num_comments > 0
    assert num_comments < 1000
    # assert page size is less than first page

    # assert the session token is either
    # returned here or the login
    # http request
    token = extract_token(response)
    now = datetime.now()
    time_delta = now - start_time 
    time_delta = time_delta.seconds // 1000
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
def test_infinite_scroll():

    app_info = initiate_test_user()
    test_user = app_info["test_user"]
    token = get_first_page(client, test_user)
    num_pages_to_test = 10
    for i in range(num_pages_to_test):
        # TODO: assert latencies of each request
        results = get_next_page(client, token, test_user)
        time_delta = results["time_delta"]
        assert time_delta < 1000 #TODO: determine appropriate threshold
        assert results["token"] == token
        # Possible scalability/security measure
        # switch token every request
        # WAAAY down the line
