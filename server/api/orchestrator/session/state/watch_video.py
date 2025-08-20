from sqlalchemy import select

from state.comments import Comments
from state.state_module import StateModule


class Video(StateModule):
    id: int
    timestamp: str
    comments: Comments

    def __init__(self, video_info):
        self.id=video_info["id"]
        self.timestamp=0,
        self.comments=Comments()
        return
    
    def get_video_data(self, request):
        data = {}
        with self.engine.connect() as conn:
            videos_table = self.metadata_obj.tables["videos"]
            users_table = self.metadata_obj.tables["users"]

            subquery_select_cols = [videos_table.c.file_name, videos_table.c.file_dir, videos_table.c.user_id]
            subquery = select(
                *subquery_select_cols
            ).select_from(
                videos_table
            ).where(
                videos_table.c.id == self.id
            ).cte("one_video")

            select_cols = [subquery.c.file_name, subquery.c.file_dir, users_table.c.name]
            stmt = select(
                *select_cols
            ).select_from(
                subquery
            ).join(
                    users_table,
                    subquery.c.user_id == users_table.c.id
            )

            records = conn.execute(stmt)
            #TODO: consider how to actually have
            # client show the correct video
            # maybe could just point to
            # api's address and move assets from
            # db/ to api/ 
            for row in records:
                data["file_name"] = row[0]
                data["file_dir"] = row[1]
                data["user_name"] = row[2]

        return data

    def open_video(self, request):
        results = {}
        results["video_data"] = self.get_video_data(request)
        #comments_data = self.emit("load_first_page_of_comments", {"video_id": self.id})
        #results["comments_data"] = comments_data

        return results
