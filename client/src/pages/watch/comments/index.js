import * as React from "react";
import List from "@mui/material/List";

import { useInfiniteScroll } from "../../../customHooks/useInfiniteScroll";

import Comment from "./Comment";

export default function Comments() {
  const [comments, setComments] = React.useState([]);

  const { sentinelRef, loading } = useInfiniteScroll({
    route: "getcomments",
    handleData: (data) => setComments(prev => [...prev, ...data.comment_data]),
  });

  return (
    <div>
      <List sx={{ width: "100%", maxWidth: 360, bgcolor: "background.paper" }}>
        {comments.map(data => {
          return <Comment comment={data.comment} user={data.user_name} />
        })}
      </List>
      <div ref={sentinelRef} style={{ height: 1 }} />
      {loading && <div>Loading...</div>}
    </div>
  );
}
