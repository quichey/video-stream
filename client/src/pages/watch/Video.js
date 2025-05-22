import * as React from "react";

export default function Video({ userID, sessionToken, setSessionToken }) {
  const id = 1;
  const [fileName, setFileName] = React.useState("");
  const [fileDir, setFileDir] = React.useState("");
  const [userName, setUserName] = React.useState("");


  var temp_user = {
    "user_id": userID,
    "user_name": "blah",
    //"token": sessionToken,
    "video_id": 1
  };
  var post_req_data = JSON.stringify(temp_user)
  fetch(
    "http://127.0.0.1:5000/video",
    {
      method: "POST",
      // may need to use POST later for adding params
      // i think don't have to, could use query string
      // POST is probably more secure cause body is probably encrypted
      //method: "POST",
      // body: JSON.stringify({ limit: 30 }),
      // mode: "no-cors",
      body: post_req_data
    },
  )
  .then((response) => response.json())
  .then((json) => {
    console.log(json);
    setFileDir(json.video_data.file_dir);
    setFileName(json.video_data.file_name);
    setUserName(json.video_data.user_name);
    setSessionToken(json.session_info);
  })
  .catch((error) => {
    console.log(error);
  });
  
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