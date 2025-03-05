import * as React from "react";
import List from "@mui/material/List";

import useWindowScroll from "../../../customHooks/useWindowScroll";
import Comment from "./Comment";


export default function Comments() {
  const [comments, setComments] = React.useState([]);
  const [nextPageKey, setNextPageKey] = React.useState();
  const [loading, setLoading] = React.useState(false);
  const scrollPosition = useWindowScroll();

  /*
   *facilicate infinite scroll by getting more comments ? 
   *or seeems to just be appending to the comments state object after getting the data
   */
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

  /*
   * getting the data from server -- i think both from initial load and scrolling down
   * params need limit (page size) as well as some variable to indicate offset/next-page
   * 
   * right now this one is only initial load cause of empty dependencies -- either:
   * --- do 2 separate useEffects, 1 for first load, 2nd for scrolling data
   * --- put all in this useEffect
   * I think 2 separate useEffects will make state updating simpler from experience iirc
   * In that case, should i make functions for repeated parts of the useEffect? -- not necessary, but possibly beneficial
   * 
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

  /*
   * moving the actual scroll bar
   * not yet implemented getting more data from server
   * 
   */
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