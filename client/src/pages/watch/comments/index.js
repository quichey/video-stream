import * as React from "react";
import List from "@mui/material/List";

import useWindowScroll from "../../../customHooks/useWindowScroll";
import Comment from "./Comment";


export default function Comments() {
  const [comments, setComments] = React.useState([]);
  const [nextPageKey, setNextPageKey] = React.useState();
  const [loading, setLoading] = React.useState(false);
  const scrollPosition = useWindowScroll();

  const addComments = React.useCallback(
    (numNewComments) => {
      setComments((prevComments) => {
        //let tempComments = JSON.parse(JSON.stringify(prevComments));
        for (var i = 0; i < numNewComments; i++) {
          //addComment(tempComments);
          addComment(prevComments);
        }
        //return tempComments;
        return prevComments;
      });
    },
    [setComments],
  );

  /*
  React.useEffect(() => {
    addComments(20);
  }, [addComments]);
  */
  React.useEffect(() => {
    /*
    TODO: add nextPageKey to list of params for post request
    */
    fetch(
      "localhost:5000",
      {
        method: "POST",
        body: JSON.stringify({ limit: 30 }),
        mode: "no-cors",
      },
    )
      .then((response) => response.json())
      .then((json) => {
        console.log(json);
        const tmpComments = json.items.map((comment) => {
          <Comment comment={comment.comment} user={comment.user_name} />;
        });
        setComments(tmpComments);
        setNextPageKey(json.last_evaluated_key);
      })
      .catch((error) => {
        console.log(error);
      });

    /*
    let tempComments = [];
    for (var i = 0; i < 40; i++) {
      addComment(tempComments);
    }
    setComments(tempComments);
    */
  }, []);

  React.useEffect(() => {
    if (scrollPosition.yPercent > 98) {
      if (loading) {
        setLoading(false);
      } else {
        console.log("end of scroll");
        let tempComments = [];
        for (var i = 0; i < comments.length + 10; i++) {
          addComment(tempComments);
        }
        setComments(tempComments);
        setLoading(true);
      }
      /*
      setComments((prevComments) => {
        let tempComments = JSON.parse(JSON.stringify(prevComments));
        for (var i = 0; i < 20; i++) {
          addComment(tempComments);
        }
        return tempComments;
      });
      */
    }
  }, [scrollPosition, comments, loading]);
  return (
    <List sx={{ width: "100%", maxWidth: 360, bgcolor: "background.paper" }}>
      {comments}
    </List>
  );
}