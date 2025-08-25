import * as React from "react";
import List from "@mui/material/List";

import { useInfiniteScroll } from "../../../customHooks/useInfiniteScroll";

export default function Comments() {
  const [comments, setComments] = React.useState([]);

  const { sentinelRef, loading } = useInfiniteScroll({
    route: "getcomments",
    handleData: (newComments) => setComments(prev => [...prev, ...newComments]),
  });

  return (
    <div>
      <List sx={{ width: "100%", maxWidth: 360, bgcolor: "background.paper" }}>
        {comments}
      </List>
      <div ref={sentinelRef} style={{ height: 1 }} />
      {loading && <div>Loading...</div>}
    </div>
  );
}
