import logo from "./logo.svg";
import "./App.css";

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
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
    </div>
  );
}

export default App;
