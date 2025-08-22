import * as React from "react";
import { useParams } from "react-router-dom";

import { VideoContext } from "..";

import { useServerCall } from "../../customHooks/useServerCall";

export default function Video() {
  const { videoID } = useParams();
  const { id, setID } = React.useContext(VideoContext);
  const { setFileDir, setFileName, fileDir, fileName } =
    React.useContext(VideoContext);
  const fetchData = useServerCall();

  const handleServer = React.useCallback(
    (json) => {
      setFileDir(json?.video_data?.file_dir);
      setFileName(json?.video_data?.file_name);
    },
    [setFileDir, setFileName],
  );
  React.useEffect(() => {
    setID(videoID);
  }, [videoID, setID]); //pretty sure this will cause inf loop

  React.useEffect(() => {
    if (id !== "none")  {
      fetchData("video", handleServer);
    }
  }, [fetchData, handleServer, id]);

  //const { width: windowWidth, height: windowHeight } = useWindowDimensions();
  return (
    <video controls width="70%" height="50%">
      <source src="/media/cc0-videos/flower.webm" type="video/webm" />
      <source
        src={`${process.env.PUBLIC_URL}/videos/${fileDir}/${fileName}`}
        type="video/mp4"
      />
    </video>
  );
}

/*

      <source
        src="https://chess-react.s3.us-west-1.amazonaws.com/WIN_20240826_10_03_57_Pro.mp4"
        type="video/mp4"
      />
*/
