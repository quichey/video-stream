import * as React from "react";
import List from "@mui/material/List";

import { HTTPContext } from "..";

import useWindowScroll from "../../../customHooks/useWindowScroll";
import Comment from "./Comment";

const addComment = (commentArray) => {
  commentArray.push(
    <Comment
      comment={`Comment number ${commentArray.length}`}
      user={`User number ${commentArray.length}`}
    ></Comment>,
  );
};
export default function Comments() {
  const httpContext = React.useContext(HTTPContext);

  const [comments, setComments] = React.useState([]);
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
    fetch(
      `${httpContext.serverURL}/getcomments`,
      {
        method: "POST",
        // may need to use POST later for adding params
        // i think don't have to, could use query string
        // POST is probably more secure cause body is probably encrypted
        //method: "POST",
        // body: JSON.stringify({ limit: 30 }),
        // mode: "no-cors",
      body: httpContext.postRequestPayload
      },
    )
      .then((response) => response.json())
      .then((json) => {
        console.log(json);
        const tmpComments = json.comment_data.map((comment) => {
          return <Comment comment={comment.comment} user={comment.user_name} />;
        });
        setComments(tmpComments);
        httpContext.refreshSessionToken(json);
      })
      .catch((error) => {
        console.log(error);
      });
  }, [httpContext]);

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
        /*
          Do Server Call with sessionToken
          maybe make some kinda func for re-used api info?
          also set up build of client javascript/html to
          load server host/domain Addr dynamically i think (process.env?)
        */
       /*
        console.log("end of scroll");
        let tempComments = [];
        for (var i = 0; i < comments.length + 10; i++) {
          addComment(tempComments);
        }
        setComments(tempComments);
        setLoading(true);
        */
        console.log("blah")

        
        fetch(
          `${httpContext.serverURL}/getcomments`,
          {
            method: "POST",
            // may need to use POST later for adding params
            // i think don't have to, could use query string
            // POST is probably more secure cause body is probably encrypted
            //method: "POST",
            // body: JSON.stringify({ limit: 30 }),
            // mode: "no-cors",
            body: httpContext.postRequestPayload
          },
        )
          .then((response) => response.json())
          .then((json) => {
            console.log(json);
            const tmpComments = json.comment_data.map((comment) => {
              return <Comment comment={comment.comment} user={comment.user_name} />;
            });
            
            setComments((prevComments) => {
              const newComments = [...prevComments, ...tmpComments]
              return newComments
            });
          })
          .catch((error) => {
            console.log(error);
          });
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
  }, [scrollPosition, comments, loading, httpContext]);
  return (
    <List sx={{ width: "100%", maxWidth: 360, bgcolor: "background.paper" }}>
      {comments}
    </List>
  );
}