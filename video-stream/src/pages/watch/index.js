import Comments from "./Comments";
import Navbar from "./Navbar";
import Recommendations from "./Recommendations";
import Video from "./Video";

export default function Watch() {
  return (
    <>
      <Navbar />
      <Video />
      <Comments />
      <Recommendations />
    </>
  );
}
