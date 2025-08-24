from flask import json
from sqlalchemy import select
from azure.identity import DefaultAzureCredential
from azure.storage.blob import (
    BlobServiceClient,
    generate_blob_sas, BlobSasPermissions
)

from api.orchestrator.session.state.comments import Comments
from api.orchestrator.session.state.state_module import StateModule
from api.util.request_data import extract_video_info


class Video(StateModule):
    id: int
    timestamp: str
    comments: Comments

    def __init__(self, request, response, deployment):
        super().__init__(request, response, deployment)
        video_info = extract_video_info(request=request)
        self.id=video_info["id"]
        self.timestamp=0,
        self.comments=Comments(request, response, deployment, self.id)
        return
    
    def get_video_data(self, request, response):
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

    def open_video(self, request, response):
        results = {}
        results["video_data"] = self.get_video_data(request, response)
        #comments_data = self.emit("load_first_page_of_comments", {"video_id": self.id})
        #results["comments_data"] = comments_data

        return results["video_data"]
