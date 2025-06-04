import React from "react";
//import axios from "axios";

const UPLOAD_ENDPOINT = "http://127.0.0.1:5000/video-upload";

export default function VideoUpload() {
  const [file, setFile] = React.useState([]);
  const [name, setName] = React.useState("");

  const fetchFileStreamer = React.useCallback(
    (readFileStream, pageNum) => {
      const firstIdx = pageNum * 1000;
      const lastIdx = pageNum + 1000;
      readFileStream = readFileStream[0];
      const baseCaseReached = firstIdx >= readFileStream.length;
      var file_stream;
      if (baseCaseReached) {
        file_stream = "DONE";
      } else {
        //file_stream = readFileStream.splice(firstIdx, lastIdx);
        file_stream = readFileStream;
      }
      const fileInfo = {
        file_stream: file_stream,
        name: name,
      };
      const body = {
        user_id: 0,
        user_name: "3",
        token: 0,
        file_info: fileInfo,
      };
      const fetchParams = {
        body: JSON.stringify(body),
        method: "POST",
      };
      if (baseCaseReached) {
        fetch(UPLOAD_ENDPOINT, fetchParams)
          .then((response) => response.json())
          .then((json) => {
            console.log(json);
          })
          .catch((error) => {
            console.log(error);
          });
      }

      fetch(UPLOAD_ENDPOINT, fetchParams)
        .then((response) => response.json())
        .then((json) => {
          fetchFileStreamer(readFileStream, pageNum + 1);
          console.log(json);
        })
        .catch((error) => {
          console.log(error);
        });
    },
    [name],
  );

  const handleSubmit = React.useCallback(
    (event) => {
      const file_stream = file;
      fetchFileStreamer(file_stream, 0);
    },
    [fetchFileStreamer, file],
  );

  const handleFileChange = React.useCallback(async (e) => {
    const fileObject = e.target.files[0];
    if (!fileObject) {
      console.log("No file selected.");
      return;
    }
    const stream = fileObject.stream();
    const reader = stream.getReader();
    while (true) {
      const { done, value } = await reader.read();
      if (done) {
        console.log("Stream reading complete.");
        return;
      }
      // Process the chunk of data
      console.log("Chunk:", value);
      setFile((prevFileArray) => {
        const valueAsArray = value;
        return prevFileArray.concat(valueAsArray);
      });
    }
  }, []);

  const handleNameChange = React.useCallback((e) => {
    setName(e.target.value);
  }, []);
  return (
    <div>
      <h1>React File Upload</h1>
      <input type="file" onChange={handleFileChange} />
      <input type="text" onChange={handleNameChange} value={name} />
      <button disabled={!(file && name)} onClick={handleSubmit}>
        Upload File
      </button>
    </div>
  );
}
