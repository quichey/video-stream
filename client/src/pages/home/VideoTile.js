import * as React from "react";
import Card from '@mui/material/Card';
import Stack from '@mui/material/Stack';
import Divider from '@mui/material/Divider';
import Typography from '@mui/material/Typography';
import { NavLink } from "react-router";

import { VideoContext } from "..";





function VideoInfo({title, userName, userIcon, totalViews, uploadDate}) {
  return (
    <Stack direction="row" spacing={1}>
      <Typography>
        {userName}
      </Typography>
      <Typography>
        {title}
      </Typography>
      <Typography>
        {userIcon}
      </Typography>
      <Typography>
        {totalViews}
      </Typography>
      <Typography>
        {uploadDate}
      </Typography>
    </Stack>
  );

}

export default function VideoTile({ id, fileName, fileDir, userName }) {
  const {setID} = React.useContext(VideoContext);

  const [title, setTitle] = React.useState("");
  const [userIcon, setUserIcon] = React.useState("");
  const [totalViews, setTotalViews] = React.useState("");
  const [uploadDate, setUploadDate] = React.useState("");

  React.useEffect(() => {
    setTitle("test title")
    setUserIcon("test userIcon")
    setTotalViews("test total views")
    setUploadDate("test upload date")
  }, [])

  const handleVideoClick = React.useCallback(() => {
    setID(id)
  }, [id, setID]) //pretty sure this will cause inf loop

  return (
    
    <Card
      variant="outlined"
      sx={{ maxWidth: 360 }}
      onClick={handleVideoClick}
      >
        <NavLink to={`/watch/${id}`} end>
          <video controls width="100%" height="100%">
            <source src="/media/cc0-videos/flower.webm" type="video/webm" />
            <source
              src={`${process.env.PUBLIC_URL}/videos/${fileDir}/${fileName}`}
              type="video/mp4"
            />
          </video>
        </NavLink>
      <Divider />
      <VideoInfo title={title} userName={userName} userIcon={userIcon} totalViews={totalViews} uploadDate={uploadDate} />
    </Card>
  );
}