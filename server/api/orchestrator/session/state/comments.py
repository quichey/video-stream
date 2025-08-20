
from sqlalchemy import select

from state.state_module import StateModule


COMMENTS_FIRST_PAGE_SIZE = 15
COMMENTS_NEXT_PAGE_SIZE = 10


class Comments(StateModule):
    page_number = 0
    limit: int = COMMENTS_FIRST_PAGE_SIZE
    video_id: int = None

    def __init__(self, video_id):
        #self.on_event("load_first_page_of_comments", self.load_first_page)
        self.video_id = video_id

    @property
    def offset(self):
        if self.page_number == 0:
            return 0
        else:
            return COMMENTS_FIRST_PAGE_SIZE + (self.page_number - 1) * COMMENTS_NEXT_PAGE_SIZE
    


    """
    * From google search -- Performance optimization for later
    Performance Considerations:
        While the order of LIMIT and OFFSET doesn't directly impact performance in most cases,
        using large OFFSET values can lead to slower queries, especially on large tables,
        as the database needs to scan through a large number of rows before applying the LIMIT. 
    """
    def get_comments(self, request):
        limit = self.limit
        offset = self.offset

        data = []
        with self.engine.connect() as conn:
            comments_table = self.metadata_obj.tables["comments"]
            users_table = self.metadata_obj.tables["users"]

            subquery_select_cols = [comments_table.c.comment, comments_table.c.user_id]
            subquery = select(
                *subquery_select_cols
            ).select_from(
                comments_table
            ).where(
                comments_table.c.video_id == self.video_id
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

        self.page_number += 1
        self.limit = COMMENTS_NEXT_PAGE_SIZE
        return data