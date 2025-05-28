import * as React from "react";
import List from "@mui/material/List";

import useWindowScroll from "../../../customHooks/useWindowScroll";
import { useServerCall } from "../../../customHooks/useServerCall";

import Comment from "./Comment";


export default function Comments() {
  const fetchServer = useServerCall();

  const [comments, setComments] = React.useState([]);
  const [loading, setLoading] = React.useState(false);
  const scrollPosition = useWindowScroll();

  const handleFirstPageResponse = React.useCallback((json) => {
    const tmpComments = json.comment_data.map((comment) => {
      return (
        <Comment
          comment={comment.comment}
          user={comment.user_name}
        />
      );
    });
    setComments(tmpComments);
  }, []);
  const route = "/getcomments"
  React.useEffect(() => {
    fetchServer(route, handleFirstPageResponse)
  }, [
    fetchServer,
    route,
    handleFirstPageResponse,
  ]);


  const handleNextPageResponse = React.useCallback((json) => {
    const tmpComments = json.comment_data.map((comment) => {
      return (
        <Comment
          comment={comment.comment}
          user={comment.user_name}
        />
      );
    });
    
    setComments((prevComments) => {
      const newComments = [...prevComments, ...tmpComments]
      return newComments
    });
  }, []);

  React.useEffect(() => {
    if (scrollPosition.yPercent > 98) {
      if (loading) {
        setLoading(false);
      } else {
        fetchServer(route, handleNextPageResponse);
      }
    }
  }, [
    scrollPosition,
    comments,
    loading,
    fetchServer,
    route,
    handleNextPageResponse,
  ]);

  return (
    <List
      sx={{ width: "100%", maxWidth: 360, bgcolor: "background.paper" }}
    >
      {comments}
    </List>
  );
}