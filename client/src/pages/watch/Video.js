import * as React from "react";

import { VideoContext } from "..";
import { HTTPContext } from "..";


export default function Video() {
  const videoContext = React.useContext(VideoContext);
  const httpContext = React.useContext(HTTPContext);


  fetch(
    `${httpContext.serverURL}/video`,
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
    videoContext.setFileDir(json.video_data.file_dir);
    videoContext.setFileName(json.video_data.file_name);
    httpContext.refreshSessionToken(json);
  })
  .catch((error) => {
    console.log(error);
  });
  
  //const { width: windowWidth, height: windowHeight } = useWindowDimensions();
  return (
    <video controls width="70%" height="50%">
      <source src="/media/cc0-videos/flower.webm" type="video/webm" />
      <source
        src={`${process.env.PUBLIC_URL}/videos/${videoContext.fileDir}/${videoContext.fileName}`}
        type="video/mp4"
      />
      Download the
      <a href="/media/cc0-videos/flower.webm">WEBM</a>
      or
      <a href="/media/cc0-videos/flower.mp4">MP4</a>
      video.
    </video>
  );
}

/*

      <source
        src="https://chess-react.s3.us-west-1.amazonaws.com/WIN_20240826_10_03_57_Pro.mp4"
        type="video/mp4"
      />
*/