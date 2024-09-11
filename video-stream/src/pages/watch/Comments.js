import * as React from "react";
import { Typography } from "@mui/material";
import List from "@mui/material/List";
import ListItem from "@mui/material/ListItem";
import ListItemText from "@mui/material/ListItemText";
import ListItemAvatar from "@mui/material/ListItemAvatar";
import Avatar from "@mui/material/Avatar";
import ImageIcon from "@mui/icons-material/Image";
import WorkIcon from "@mui/icons-material/Work";
import BeachAccessIcon from "@mui/icons-material/BeachAccess";

import useWindowScroll from "../../customHooks/useWindowScroll";

function Comment({ comment, user }) {
  return (
    <ListItem>
      <ListItemAvatar>
        <Avatar>
          <ImageIcon />
        </Avatar>
      </ListItemAvatar>
      <ListItemText primary={`@${user}`} secondary={comment} />
    </ListItem>
  );
}
const addComment = (commentArray) => {
  commentArray.push(
    <Comment
      comment={`Comment number ${commentArray.length}`}
      user={`User number ${commentArray.length}`}
    ></Comment>,
  );
};

export default function Comments() {
  const [comments, setComments] = React.useState([]);
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
    let tempComments = [];
    for (var i = 0; i < 40; i++) {
      addComment(tempComments);
    }
    setComments(tempComments);
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
