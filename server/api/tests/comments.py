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




with app.test_request_context('/getcomments', method='POST'):
    # now you can do something with the request until the
    # end of the with block, such as basic assertions:
    assert request.path == '/getcomments'
    assert request.method == 'POST'