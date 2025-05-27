import * as React from "react";

import { VideoContext } from "..";

import { useServerCall } from "../../customHooks/useServerCall";


export default function Video() {
  const {setFileDir, setFileName, fileDir, fileName} = React.useContext(VideoContext);

  const handleServer = React.useCallback((json) => {
    setFileDir(json.video_data.file_dir);
    setFileName(json.video_data.file_name);
  }, [setFileDir, setFileName])

  useServerCall("video", handleServer)
  
  //const { width: windowWidth, height: windowHeight } = useWindowDimensions();
  return (
    <video controls width="70%" height="50%">
      <source src="/media/cc0-videos/flower.webm" type="video/webm" />
      <source
        src={`${process.env.PUBLIC_URL}/videos/${fileDir}/${fileName}`}
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