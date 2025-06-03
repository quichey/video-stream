import * as React from "react";
import { Typography } from "@mui/material";
import FileUploadIcon from "@mui/icons-material/FileUpload";
import Button from "@mui/material";

import { useServerCall } from "../../customHooks/useServerCall";

/*

-- Video upload ICON --

"Drag and drop video files to upload

Your videos will be private until you publish them."

-- Select files BUTTON --

*/

export default function VideoUpload() {
  const [file, setFile] = React.useState(undefined);
  // TODO: maybe don't do useServerCall as headers need to be different
  const fetchData = useServerCall();

  const handleClick = React.useCallback((e) => {
    console.log(e);
    setFile(e.target.files[0]);
  }, []);

  const handleServer = React.useCallback((json) => {
    console.log(`reached video-upload-handle-server: ${json}`);
  }, []);

  React.useEffect(() => {
    if (file !== undefined) {
      const extraParams = {
        body: { file: file },
        headers: { "content-type": "multipart/form-data" },
      };
      fetchData("video-upload", handleServer, extraParams);
    }
  }, [fetchData, handleServer, file]);
  return (
    <div>
      <FileUploadIcon />
      <Typography>Drag and drop video files to upload</Typography>
      <Typography>
        Your videos will be private until you publish them.
      </Typography>
      {
        // have to use form input type="file" or MUI file thing to open file explorer
      }
      <Button onClick={handleClick}>Select Files</Button>
    </div>
  );
}

/*

  const handleSubmit = async (event) => {
    setStatus(""); // Reset status
    event.preventDefault();
    const formData = new FormData();
    formData.append("avatar", file);
    formData.append("name", name);



    const extraParams = { file: file };
      fetchData("video-upload", handleServer, "POST", extraParams)



    setStatus(resp.status === 200 ? "Thank you!" : "Error.");
  };

  return (
    <form onSubmit={handleSubmit}>
      <h1>React File Upload</h1>
      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <input
        type="text"
        onChange={(e) => setName(e.target.value)}
        value={name}
      />
      <button type="submit" disabled={!(file && name)}>
        Upload File
      </button>
      {status ? <h1>{status}</h1> : null}
    </form>
  );
*/
