from flask import json



    
def extract_user_info(request):
    form_data = json.loads(request.data)
    # TODO: change later to something like request.form['username']
    user_info = {
        "id": form_data['user_id'],
        "name": form_data['user_name']
    }
    return user_info
    
def extract_video_info(request):
    form_data = json.loads(request.data)
    video_info = {}
    if "video_id" in form_data:
        video_info["id"] = form_data['video_id']
    return video_info