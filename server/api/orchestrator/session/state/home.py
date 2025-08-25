from flask import json
from sqlalchemy import select

from api.orchestrator.session.state.comments import Comments
from api.orchestrator.session.state.state_module import StateModule
from api.util.request_data import extract_video_info


class Home(StateModule):
    id: int
    timestamp: str
    
    def get_video_list(self, request, response):
        data = []
        with self.engine.connect() as conn:
            videos_table = self.metadata_obj.tables["videos"]
            users_table = self.metadata_obj.tables["users"]

            subquery_select_cols = [
                videos_table.c.id,
                videos_table.c.file_name,
                videos_table.c.file_dir,
                videos_table.c.user_id,
                videos_table.c.date_created,
                videos_table.c.date_updated,
            ]
            subquery = select(
                *subquery_select_cols
            ).select_from(
                videos_table
            ).limit(
                10
            ).cte("one_page_videos")

            select_cols = [
                subquery.c.id,
                subquery.c.file_name,
                subquery.c.file_dir,
                users_table.c.name,
                users_table.c.profile_icon,
                users_table.c.id,
                subquery.c.date_created,
                subquery.c.date_updated,
            ]
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
                video_data_point = {
                    "id": row[0],
                    "file_name": row[1],
                    "file_dir": row[2],
                    "user_name": row[3],
                    "user_icon": row[4],
                    "user_id": row[5],
                    "date_created": row[6],
                    "date_updated": row[7],
                }
                video_url = self.STORAGE.get_video_url(
                    video_data_point["file_dir"],
                    video_data_point["file_name"]
                )
                video_data_point["video_url"] = video_url
                user_icon_url = self.STORAGE.get_image_url(
                    video_data_point["file_dir"],
                    video_data_point["file_name"]
                )
                video_data_point["user_icon_url"] = user_icon_url
                data.append(video_data_point)

        return data
