from flask import json


def extract_registration_info(request):
    if not request.data:
        return None
    form_data = json.loads(request.data)
    # TODO: change later to something like request.form['username']
    registration_info = {
        "name": form_data.get('user_name'),
        "password": form_data.get('password'),
    }
    return registration_info

def extract_login_info(request):
    if not request.data:
        return None
    form_data = json.loads(request.data)
    # TODO: change later to something like request.form['username']
    login_info = {
        "name": form_data.get('user_name'),
        "password": form_data.get('password'),
    }
    return login_info
    
def extract_user_info(request):
    if not request.data:
        return None
    form_data = json.loads(request.data)
    # TODO: change later to something like request.form['username']
    user_info = {
        "id": form_data.get('user_id'),
        "name": form_data.get('user_name')
    }
    return user_info

def has_user_info(request):
    user_info = extract_user_info(request)
    if not user_info:
        return False
    return user_info and (user_info.get("id") is not None) and (user_info.get("id") >= 0)
    
def extract_video_info(request):
    form_data = json.loads(request.data)
    video_info = {}
    if "video_id" in form_data:
        video_info["id"] = form_data['video_id']
    return video_info



def extract_long_term_cookie(request):
    cookie = request.cookies.get("long_term_session")
    return cookie


def has_long_term_cookie(request):
    cookie = extract_long_term_cookie(request=request)
    return cookie is not None

def extract_session_token(request):
    if not request.data:
        return None
    form_data = json.loads(request.data)
    token = form_data.get('session_token')
    return token


def has_session_token(request):
    token = extract_session_token(request=request)
    if not token:
        return False
    return token is not None



"""
TODO: at some point
implement way to handle chunked data
"""
def extract_video_file_info(request):
    user_info = extract_user_info(request)
    #print(f"\n\n reached extract_video_file_info \n\n")
    form_data = json.loads(request.data)
    video_file_info = {}
    if "file_info" in form_data:
        file_info = form_data['file_info']
        #print(f"\n\n file_info: {file_info} \n\n")
        file_stream = dict(file_info["file_stream"])
        #print(f"\n\n len(file_stream.keys()): {len(file_stream.keys())} \n\n")
        file_name = file_info["name"]
        # file being loaded as str
        # convert to something consumable by bytes() construct
        video_file_info["bytes"] = file_stream
        video_file_info["name"] = file_name
        #video_file_info["user_id"] = user_info["id"]
        video_file_info["user_id"] = 1
        video_file_info["upload_date"] = "now"
    video_file_info["bytes"] = decode_video(video_file_info["bytes"])
    return video_file_info



def decode_video(self, file_stream):
    as_array = []
    for _, b in file_stream.items():
        #print(f"\n\n bytes(b): {bytes(b)} \n\n")
        as_array.append(b)
    #print(f"\n\n as_array: {as_array} \n\n")
    #print(f"\n\n len(as_array): {len(as_array)} \n\n")
    as_bytes = bytes(as_array)
    #print(f"\n\n as_bytes: {as_bytes} \n\n")
    #print(f"\n\n len(as_bytes): {len(as_bytes)} \n\n")
    return as_bytes
    #return as_bytes.decode('utf-8', errors='ignore')