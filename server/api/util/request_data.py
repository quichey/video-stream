from flask import json



    
def extract_user_info(request):
    form_data = json.loads(request.data)
    # TODO: change later to something like request.form['username']
    user_info = {
        "id": form_data['user_id'],
        "name": form_data['user_name']
    }
    return user_info

def has_user_info(request):
    user_info = extract_user_info(request)
    return user_info and (user_info.get("id") >= 0)
    
def extract_video_info(request):
    form_data = json.loads(request.data)
    video_info = {}
    if "video_id" in form_data:
        video_info["id"] = form_data['video_id']
    return video_info