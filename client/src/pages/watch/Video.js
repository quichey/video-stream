import * as React from "react";
import { useParams } from "react-router-dom";

import { get_storage_url } from "../../util/urls";
import { VideoContext, HTTPContext } from "..";

import { useServerCall } from "../../customHooks/useServerCall";

export default function Video() {
  const { videoID } = useParams();
  const { postRequestPayload } = React.useContext(HTTPContext);
  const { id, setID, setFileDir, setFileName, fileDir, fileName } =
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
    setFileDir(undefined);
    setFileName(undefined);
  }, [videoID, setID, setFileDir, setFileName]); //pretty sure this will cause inf loop

  React.useEffect(() => {
    if (id !== "none" && postRequestPayload && JSON.parse(postRequestPayload).video_id !== "none") {
      fetchData("video", handleServer);
    }
  }, [fetchData, handleServer, id, postRequestPayload]);

  const videoUrl =
    fileDir && fileName
      ? `${get_storage_url()}/videos/${fileDir}/${fileName}`
      : null;

  if (!videoUrl) {
    return <div>Loading video...</div>; // or a spinner
  }

  //const { width: windowWidth, height: windowHeight } = useWindowDimensions();
  return (
    <video controls width="100%" height="100%">
      <source
        src={videoUrl}
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
