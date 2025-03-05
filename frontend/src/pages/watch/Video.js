export default function Video() {
  //const { width: windowWidth, height: windowHeight } = useWindowDimensions();
  return (
    <video controls width="70%" height="50%">
      <source src="/media/cc0-videos/flower.webm" type="video/webm" />
      <source
        src="https://chess-react.s3.us-west-1.amazonaws.com/WIN_20240826_10_03_57_Pro.mp4"
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
