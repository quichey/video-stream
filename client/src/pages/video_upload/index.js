import React from "react";
//import axios from "axios";

const UPLOAD_ENDPOINT = "http://127.0.0.1:5000/video-list";

export default function VideoUpload() {
  const [file, setFile] = React.useState(null);
  const [name, setName] = React.useState("");

  const handleSubmit = React.useCallback(
    (event) => {
      /*
      event.preventDefault();
      const formData = new FormData();
      formData.append("avatar", file);
      formData.append("name", name);
      axios.post(UPLOAD_ENDPOINT, formData, {
        headers: {
          "content-type": "multipart/form-data",
        },
      });
      */

      const body = {
        user_id: 0,
        user_name: "3",
        token: 0,
        file: file,
        name: name,
      };
      const fetchParams = {
        body: JSON.stringify(body),
        method: "POST",
      };
      fetch(UPLOAD_ENDPOINT, fetchParams)
        .then((response) => response.json())
        .then((json) => {
          console.log(json);
        })
        .catch((error) => {
          console.log(error);
        });
    },
    [file, name],
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
