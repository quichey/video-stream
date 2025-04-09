import pytest
import time
import threading
from datetime import timedelta, date, datetime
from flask import request, json

from api import create_app
from api.Cache import COMMENTS_FIRST_PAGE_SIZE, COMMENTS_NEXT_PAGE_SIZE

@pytest.fixture()
def app_info():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    # get info of test_user
    test_user = 0
    # include info in yield
    app_info = {
        "client": app.test_client(),
        "test_user": test_user
    }
    yield app_info

    # clean up / reset resources here

def extract_token(response):
    session_info = response.json["session_info"]
    return session_info

def package_session_info(user):
    """
    data = {
        "data": {
            "user_id": 0,
            "user_name": user
        }
    }
    """
    data = {
        "user_id": 0,
        "user_name": user
    }
    return data

def get_first_page(client, user):
    response = client.post(
        "/getcomments",
        #json=package_session_info(user),
        data=json.dumps(package_session_info(user))
    )
    print(f"\n\n response.json: {response.json} \n\n")
    data = response.json["comment_data"]
    num_comments = len(data)
    #assert num_comments > 0
    assert num_comments <= COMMENTS_FIRST_PAGE_SIZE
    # assert the session token is either
    # returned here or the login
    # http request
    token = extract_token(response)
    print(f"\n\n token: {token} \n\n")
    print(f"\n\n type(token): {type(token)} \n\n")
    return token

    # when I add into Seed module
    # the code for instantiating 
    # a consistent testing database
    # ensure the num_comments == size_of_first_page


def get_next_page(client, token, user):
    start_time = datetime.now()
    request_data = package_session_info(user)
    request_data["token"] = token
    response = client.post(
        "/getcomments",
        #json=request_data
        data=json.dumps(request_data)
    )
    data = response.json["comment_data"]
    num_comments = len(data)
    #assert num_comments > 0
    assert num_comments <= COMMENTS_NEXT_PAGE_SIZE
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
    return results


"""
May use this context manager
as a quick means of running through all tests
in the order in which they should be applied (imperative programming paradigm)

curl --header "Content-Type: application/json" --request POST --data '{"user_id":"0","user_name":"users_name_0"}' http://127.0.0.1:5000/getcomments
curl --header "Content-Type: application/json" --request POST --data '{"user_id":"0","user_name":"users_name_0", "token": "0"}' http://127.0.0.1:5000/getcomments
"""
def test_infinite_scroll(app_info):
    next_page_time_standard = 100

    client = app_info["client"]
    test_user = app_info["test_user"]
    #token = get_first_page(client, test_user)
    token = {
        "value": None
    }
    def create_first_thread():
        nonlocal token
        def send_http_request():
            nonlocal token
            token_value = get_first_page(client, test_user)
            token["value"] = token_value
            return
        thread = threading.Thread(
            target=send_http_request
        )
        thread.start()
        return thread

    def create_next_thread(prev_thread):
        # TODO: read more about threading, then think CAREFULLY
        # then do the things you think are good to do

        nonlocal token
        def send_http_request():
            time.sleep(1000)
            nonlocal token
            results = get_next_page(client, token["value"], test_user)
            time_delta = results["time_delta"]
            assert time_delta < next_page_time_standard #TODO: determine appropriate threshold
            assert results["token"] == token
            return


        thread = threading.Thread(target=send_http_request)
        thread.start()
        prev_thread.run()
        prev_thread.join(thread)
        return thread


    def send_next_http_request():
        time.sleep(1000)
        nonlocal token
        results = get_next_page(client, token["value"], test_user)
        time_delta = results["time_delta"]
        assert time_delta < next_page_time_standard #TODO: determine appropriate threshold
        assert results["token"] == token
        return

    first_thread = create_first_thread()
    threads = [first_thread]
    num_pages_to_test = 10
    for i in range(num_pages_to_test):
        print(f"\n\n num next pages: {i} \n\n")
        prev_thread = threads[-1]
        thread = threading.Thread(target=send_next_http_request)
        thread.start()
        prev_thread.run()
        #prev_thread.join(thread)
        thread.join(prev_thread)
        threads.append(thread)
        # TODO: i think set next_thread = create_next_thread and curr_thread = next_thread
        # first,,, read more docs
        """
        # TODO: assert latencies of each request
        results = get_next_page(client, token, test_user)
        time_delta = results["time_delta"]
        assert time_delta < next_page_time_standard #TODO: determine appropriate threshold
        assert results["token"] == token
        # Possible scalability/security measure
        # switch token every request
        # WAAAY down the line
        print(f"\n\n num next pages: {i} \n\n")
        """



"""
May use this context manager
as a quick means of running through all tests
in the order in which they should be applied (imperative programming paradigm)

curl --header "Content-Type: application/json" --request POST --data '{"user_id":"0","user_name":"users_name_0"}' http://127.0.0.1:5000/getcomments
curl --header "Content-Type: application/json" --request POST --data '{"user_id":"0","user_name":"users_name_0", "token": "0"}' http://127.0.0.1:5000/getcomments
"""
def test_infinite_scroll_2(app_info):
    next_page_time_standard = 100

    client = app_info["client"]
    test_user = app_info["test_user"]
    #token = get_first_page(client, test_user)
    token = {
        "value": None
    }
    def create_first_thread():
        nonlocal token
        def send_http_request():
            nonlocal token
            token_value = get_first_page(client, test_user)
            token["value"] = token_value
            return
        thread = threading.Thread(
            target=send_http_request
        )
        thread.start()
        return thread

    def create_next_thread(prev_thread):
        # TODO: read more about threading, then think CAREFULLY
        # then do the things you think are good to do

        nonlocal token
        def send_http_request():
            time.sleep(1000)
            nonlocal token
            results = get_next_page(client, token["value"], test_user)
            time_delta = results["time_delta"]
            assert time_delta < next_page_time_standard #TODO: determine appropriate threshold
            assert results["token"] == token
            return


        thread = threading.Thread(target=send_http_request)
        thread.start()
        prev_thread.run()
        prev_thread.join(thread)
        return thread

    prev_thread = create_first_thread()
    num_pages_to_test = 10
    for i in range(num_pages_to_test):
        print(f"\n\n num next pages: {i} \n\n")
        next_thread = create_next_thread(prev_thread)
        prev_thread = next_thread
        # TODO: i think set next_thread = create_next_thread and curr_thread = next_thread
        # first,,, read more docs
        """
        # TODO: assert latencies of each request
        results = get_next_page(client, token, test_user)
        time_delta = results["time_delta"]
        assert time_delta < next_page_time_standard #TODO: determine appropriate threshold
        assert results["token"] == token
        # Possible scalability/security measure
        # switch token every request
        # WAAAY down the line
        print(f"\n\n num next pages: {i} \n\n")
        """
