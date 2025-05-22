import * as React from "react";


export default function VideoTile({ id, fileName, fileDir, userName }) {
  return (
    <video controls width="15%" height="10%">
      <source src="/media/cc0-videos/flower.webm" type="video/webm" />
      <source
        src={`${process.env.PUBLIC_URL}/videos/${fileDir}/${fileName}`}
        type="video/mp4"
      />
    </video>
  );
}