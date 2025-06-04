import React from "react";
//import axios from "axios";

const UPLOAD_ENDPOINT = "http://127.0.0.1:5000/video-upload";

export default function VideoUpload() {
  const [file, setFile] = React.useState([]);
  const [name, setName] = React.useState("");

  const chunkByteArray = React.useCallback((byteArray, startIdx, endIdx) => {
    const byteArray = new Uint8Array([1, 2, 3, 4, 5]);

    // Example: Remove elements at index 1 and 2, and insert 6 and 7
    const start = 1;
    const deleteCount = 2;
    const insert = new Uint8Array([6, 7]);

    const newByteArray = new Uint8Array(
      byteArray.length - deleteCount + insert.length,
    );

    newByteArray.set(byteArray.slice(0, start));
    newByteArray.set(insert, start);
    newByteArray.set(
      byteArray.slice(start + deleteCount),
      start + insert.length,
    );

    console.log(newByteArray); // Output: Uint8Array [1, 6, 7, 4, 5]
  }, []);

  const fetchFileStreamer = React.useCallback(
    (readFileStream, pageNum) => {
      const firstIdx = pageNum * 1000;
      const lastIdx = pageNum + 1000;
      readFileStream = readFileStream[0];
      // TODO: check length of readFileStream here
      console.log(`readFileStream.length: ${readFileStream.length}`);
      const baseCaseReached = firstIdx >= readFileStream.length;
      var file_stream;
      if (baseCaseReached) {
        file_stream = "DONE";
      } else {
        file_stream = readFileStream.slice(firstIdx, lastIdx);
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
      <input type="file" accept="video/mp4" onChange={handleFileChange} />
      <input type="text" onChange={handleNameChange} value={name} />
      <button disabled={!(file && name)} onClick={handleSubmit}>
        Upload File
      </button>
    </div>
  );
}
