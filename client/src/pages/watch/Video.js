import * as React from "react";
import { useParams } from "react-router-dom";

import { get_storage_url } from "../../util/urls";
import { VideoContext } from "../../contexts/VideoContext";

import { useServerCall } from "../../customHooks/useServerCall";
import Loading from "../../components/Loading";

export default function Video() {
  const { videoID } = useParams();
  const { setID, setFileDir, setFileName, fileDir, fileName } =
    React.useContext(VideoContext);
  const fetchData = useServerCall();
  const [sasURL, setSasURL] = React.useState(undefined)

  React.useEffect(() => {
    // Clear old video state
    setID(videoID);
    setFileDir(undefined);
    setFileName(undefined);

    // Fetch new video
    fetchData("video", (json) => {
      setFileDir(json?.video_data?.file_dir);
      setFileName(json?.video_data?.file_name);
      if (process.env.REACT_APP_DEPLOY_ENV === 'local') {
        setSasURL(undefined)
      } else{
        setSasURL(json?.video_data?.video_url)
      }
    }, { video_id: videoID });
  }, [videoID, setID, setFileDir, setFileName, fetchData]);

  const videoUrl =
    fileDir && fileName
      ? get_storage_url("videos", fileDir, fileName, sasURL)
      : null;

  if (!videoUrl) {
    return <Loading />; // or a spinner
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