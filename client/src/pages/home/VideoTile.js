import * as React from "react";
import Card from '@mui/material/Card';
import Box from '@mui/material/Box';
import Chip from '@mui/material/Chip';
import Stack from '@mui/material/Stack';
import Divider from '@mui/material/Divider';
import Typography from '@mui/material/Typography';

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
  const [title, setTitle] = React.useState("test title");
  const [userIcon, setUserIcon] = React.useState("test userIcon");
  const [totalViews, setTotalViews] = React.useState("test total views");
  const [uploadDate, setUploadDate] = React.useState("test upload date");
  return (
    <Card variant="outlined" sx={{ maxWidth: 360 }}>
      <Box
        sx={{ p: 2 }}
      >
        <video controls width="100%" height="100%">
          <source src="/media/cc0-videos/flower.webm" type="video/webm" />
          <source
            src={`${process.env.PUBLIC_URL}/videos/${fileDir}/${fileName}`}
            type="video/mp4"
          />
        </video>
      </Box>
      <Divider />
      <Box sx={{ p: 2 }}>
        <VideoInfo title={title} userName={userName} userIcon={userIcon} totalViews={totalViews} uploadDate={uploadDate} />
      </Box>

    </Card>
  );
}