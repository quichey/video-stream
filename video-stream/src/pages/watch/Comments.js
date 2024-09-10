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

  React.useEffect(() => {
    let tempComments = [];
    for (var i = 0; i < 20; i++) {
      addComment(tempComments);
    }
    setComments(tempComments);
  }, []);
  return (
    <List sx={{ width: "100%", maxWidth: 360, bgcolor: "background.paper" }}>
      {comments}
    </List>
  );
}
