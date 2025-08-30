import * as React from "react";
import { Box } from "@mui/material";

import { UserContext } from "../../../contexts/UserContext";

import { useServerCall } from "../../../customHooks/useServerCall";

import FileUploadButton from "../../../components/FileUploadButton";

export default function Picture() {
  const { id: loggedInUserID } = React.useContext(UserContext);
  const fetchData = useServerCall()

  const onFileChange = (file) => {
    fetchData("upload-profile-pic", (json) => {
        console.log(json)
    }, {
        "user_id": loggedInUserID
    })
  }
  return (
    <Box
      component="form"
      sx={{
        "& > :not(style)": { m: 1, width: "100%" },
      }}
      noValidate
      display="flex"
      flexDirection="column"
      autoComplete="off"
      style={{
        width: "100%",
      }}
    >
      <p>
        Profile Icon
      </p>
      <FileUploadButton text="Change" onChange={onFileChange} />
      <p>
        Remove
      </p>
    </Box>
  );
}
