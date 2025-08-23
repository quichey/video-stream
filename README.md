# video-stream
This is a work in progess. Keep on remembering different ideas/concepts from
Work as well as Schooling.

For now, interested in minimizing dependencies on other packages.
Trying to format folders/code to lend its way to high scalability.

First large feature I intend to get up is Infinite Scroll of comments
on a "Youtube" like video.

I do not have too much creativity in terms of "creating" new things.
I am more interested in analyzing existing technologies and 
learning how to replicate them.
I use Youtube often, so I hope to be able to 
replicate much of Youtube functionality, but also reduce 
the scope enough to have a working demo for Job-Apps.

Current Architecture(?) is python for server-side and React-javascript for client-side.
Reasoning? Mainly a lot of experience at previous two companies working in these languages.
Considered doing only one language for both server/client, but python seems more 
suited to operability between different Operating Systems. And Javascript is the core
language of most Web-Apps.

Hope to get an official Publicly Available Website up, but unsure if I will get to
that point.


# Planning out Next Features/things

Big Features
- Different Videos
- User Registration
- Recommendations
- User Channels
- Playlists
- Search Videos
- Settings

Comments Feature Improvements/Missing
- Date
- Likes/Dislikes
- Replies
- User Profile Icon


# Planning out Videos-Storage branch

Purpose: create db/schemas for storing a scalable amount of videos,
            while also hopefully having links to other datapoints like users, comments,
            recommendations(?)

Questions: Should it have a unique PK? or Composite/FK/PK?
            --- probably unique PK as it is the primary product/service of this app

            Should it have FK(s) to the other tables?
            Or should the FK(s) belong in the other tables?
            Or should we have linking tables?
            --- New question, should I forego all FK(s) in data-tables and use Link-Tables instead?
            ----- ignore this for now
    
VIDEO_STREAM = Table(
    __name__ = "videos",
    Columns = [
        "id": int, # do we need ID if we have file? could hash a file_name or just use file_name? probably not good idea? can't tell right now
        "file": mp4File,
        "date_added": data,
        "user_id": int (FK), # when fetching all data for 1 video, would be easiest to 
        # not have to scan whole users table for the owner
    
        ## probably have video_id in comments table instead of list of comments in here
        ## for brevity of data storage
        ## IIRC tables get strange when records are needlessly long, IE longer than
        ## a partition on hardware
        ## considering the limitless number of comments on YouTube, best not store in here
        ## OK to store lists in a table if list is expected to be short
    ]   
    )

# BUGS in Videos-Storage branch
1) trying to populate random foreign_keys for comments table
after giving it 2 different foreign_keys: user_id and video_id

# Next steps
should do sqlalchemy Declarative Base I think instead of doing
the extra Cache structures/Classes. The Declarative Base SEEMS
to be a good way to simplify the code and HOPEFULLY help with 
debugging

# Summary of Important Findings from SqlAlchemy Research
Session and ORM/Declarative Base
seems handy with writing certain things neatly,
such as the way it handles instance equality w/in the session.
Also using the update function is not necessary for
updating a single record. Seems worth using.
No longer need the generate_random_primary_key function i think

# Jotting out Ideas from brainstorming
update records_to_insert during randomization to use Declarative Base Classes/instances w/session.add()
--need to check if sqlalchemy sessions auto_flushing handles multi-threading
--- research how to do foreign_key stuff with declarative base


# commit for first branch of video-upload feature branch
- Research/Remember from ISS how uploading files/file-streams works *** Do this first 
- Create GUI for user to upload a video
- Create an API route for client to send video data


# Planning out project/integrate-cloud-runs branch

Purpose: Integrate the client-side Cloud Run Instance with the Server-side Cloud-Run instance

# Branch: session-non-logged-in-user
Purpose: Handle sessions for non-logged-in-users better.
As of now, I have to run the AdminRouter to delete the sessionmanager token
Figure out way to where I do not have to do this

# Branch: session-non-logged-in-user--client

# Branch: session-non-logged-in-user

# Branch: readme-polish