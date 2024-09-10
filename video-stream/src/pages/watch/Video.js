export default function Video() {
  return (
    <video controls width="2500" height="1000">
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
