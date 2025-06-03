import React from "react";
//import axios from "axios";

const UPLOAD_ENDPOINT = "http://127.0.0.1:5000/video-upload";

export default function VideoUpload() {
  const [file, setFile] = React.useState(null);
  const [name, setName] = React.useState("");

  const readFile = React.useCallback((file) => {
    const reader = new FileReader();
    reader.onload = function (event) {
      const fileContent = event.target.result;
      console.log(fileContent); // Process the file content
    };
    const fileAsText = reader.readAsText(file); // Read as text

    return fileAsText; // want this to be an array
  }, []);

  const fetchFileStreamer = React.useCallback(
    (readFileStream, pageNum) => {
      const firstIdx = pageNum * 1000;
      const lastIdx = pageNum + 1000;
      const baseCaseReached = lastIdx >= readFileStream.length();
      var file_stream;
      if (baseCaseReached) {
        file_stream = "DONE";
      } else {
        file_stream = readFileStream.splice(firstIdx, lastIdx);
      }
      const body = {
        user_id: 0,
        user_name: "3",
        token: 0,
        file: file_stream,
        name: name,
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
      const file_stream = readFile(file);
      fetchFileStreamer(file_stream, 0);
    },
    [fetchFileStreamer, readFile, file],
  );

  const handleFileChange = React.useCallback((e) => {
    setFile(e.target.files[0]);
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
