import * as React from "react";
import { useParams } from "react-router-dom";

import { get_storage_url } from "../../util/urls";
import { VideoContext } from "../../contexts/VideoContext";

import { useServerCall } from "../../customHooks/useServerCall";

export default function Video() {
  const { videoID } = useParams();
  const { setID, setFileDir, setFileName, fileDir, fileName } =
    React.useContext(VideoContext);
  const fetchData = useServerCall();

  const handleServer = React.useCallback(
    (json) => {
      setID(videoID)
      setFileDir(json?.video_data?.file_dir);
      setFileName(json?.video_data?.file_name);
    },
    [setFileDir, setFileName, setID, videoID],
  );
  /*
  React.useEffect(() => {
    setID(videoID);
    setFileDir(undefined);
    setFileName(undefined);
  }, [videoID, setID, setFileDir, setFileName]); //pretty sure this will cause inf loop
  */

  React.useEffect(() => {
    fetchData("video", handleServer, {video_id: videoID});
  }, [fetchData, handleServer, videoID]);

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