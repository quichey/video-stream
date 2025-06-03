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

  return (
    <form onSubmit={handleSubmit}>
      <h1>React File Upload</h1>
      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <input
        type="text"
        onChange={(e) => setName(e.target.value)}
        value={name}
      />
      <button type="submit" disabled={!(file && name)} onClick={handleSubmit}>
        Upload File
      </button>
    </form>
  );
}
