import pytest
from flask import request

from api import create_app

@pytest.fixture()
def initiate_test_user():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    # get info of test_user
    # include info in yield

    yield app

    # clean up / reset resources here

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

    # when I add into Seed module
    # the code for instantiating 
    # a consistent testing database
    # ensure the num_comments == size_of_first_page


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