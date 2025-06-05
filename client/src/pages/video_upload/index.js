import React from "react";
//import axios from "axios";

//try to useServerCall
import { useServerCall } from "../../customHooks/useServerCall";

const UPLOAD_ENDPOINT = "blah";

export default function VideoUpload() {
  const fetchData = useServerCall();
  const [file, setFile] = React.useState(new Uint8Array());
  const [name, setName] = React.useState("");

  const fetchFileStreamer = React.useCallback(
    (readFileStream, pageNum) => {
      //const pageSize = 64000;
      const pageSize = 6400000;
      const firstIdx = pageNum * pageSize;
      const lastIdx = pageNum + pageSize;
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

      baseFetch(readFileStream, pageNum);
    },
    [name, baseFetch],
  );

  const handleServer = React.useCallback(
    (json, readFileStream, pageNum) => {
      console.log(`reached video-upload-handle-server: ${json}`);
      fetchFileStreamer(readFileStream, pageNum + 1);
    },
    [fetchFileStreamer],
  );

  const baseFetch = React.useCallback(
    (readFileStream, pageNum) => {
      if (file !== undefined) {
        const extraParams = {
          body: { file: file },
        };
        const extraOnResponseParams = [readFileStream, pageNum];
        fetchData(
          "video-upload",
          handleServer,
          extraParams,
          extraOnResponseParams,
        );
      }
    },
    [fetchData, handleServer, file],
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
        function joinByteArrays(array1, array2) {
          const mergedArray = new Uint8Array(array1.length + array2.length);
          mergedArray.set(array1, 0);
          mergedArray.set(array2, array1.length);
          return mergedArray;
        }
        //const valueAsArray = value;
        //return prevFileArray.concat(valueAsArray);
        return joinByteArrays(prevFileArray, value);
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
