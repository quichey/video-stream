from dataclasses import dataclass
from typing import Optional

from state.state_module import StateModule


COMMENTS_FIRST_PAGE_SIZE = 15
COMMENTS_NEXT_PAGE_SIZE = 10


class Comments(StateModule):
    offset: int = 0
    limit: int = COMMENTS_FIRST_PAGE_SIZE
    next_page: bool = False
    video_id: int = None

    def __init__(self, video_id):
        #self.on_event("load_first_page_of_comments", self.load_first_page)
        self.video_id = video_id


    """
    * From google search -- Performance optimization for later
    Performance Considerations:
        While the order of LIMIT and OFFSET doesn't directly impact performance in most cases,
        using large OFFSET values can lead to slower queries, especially on large tables,
        as the database needs to scan through a large number of rows before applying the LIMIT. 
    """
    def get_comments(self, session_info, page_number=0, page_size=50):
        limit = page_size
        offset = page_size * page_number # need to change this later to make up for initial page w/different size

        if session_info is not None:
            current_state_of_comments = self.session_manager.get_state(session_info, "video", "comments")
            offset = current_state_of_comments.offset
            limit = current_state_of_comments.limit
            #print(f"\n\n offset: {offset} \n\n")
            #print(f"\n\n limit: {limit} \n\n")

        data = []
        with self.engine.connect() as conn:
            comments_table = self.metadata_obj.tables["comments"]
            users_table = self.metadata_obj.tables["users"]

            current_video_state = self.session_manager.get_state(session_info, "video")
            subquery_select_cols = [comments_table.c.comment, comments_table.c.user_id]
            subquery = select(
                *subquery_select_cols
            ).select_from(
                comments_table
            ).where(
                comments_table.c.video_id == current_video_state.id
            ).cte("comments_one_video")

            select_cols = [subquery.c.comment, users_table.c.name]
            stmt = select(
                *select_cols
            ).select_from(
                subquery
            ).join(
                    users_table,
                    subquery.c.user_id == users_table.c.id
            ).limit(
                limit
            ).offset(
                offset
            )

            records = conn.execute(stmt)
            new_offset = offset
            for row in records:
                new_offset = new_offset + 1

                comment_data_point = {
                    "comment": row[0],
                    "user_name": row[1]
                }
                data.append(comment_data_point)

            self.session_manager.update_state(session_info, "video", "offset", new_offset, "comments")

        return data
    
    def load_next_page(self):
        pass

        # regression test
    def load_first_page(self):

        # TODO: fetch comments?
        # update self.offset
        self.limit = COMMENTS_NEXT_PAGE_SIZE
        self.next_page = True
        return {
            "next_page"
        }