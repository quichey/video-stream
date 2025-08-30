import * as React from "react";
import { Box } from "@mui/material";

import { UserContext } from "../../../contexts/UserContext";

import { useServerCall } from "../../../customHooks/useServerCall";

import FileUploadButton from "../../../components/FileUploadButton";
import UserIconImg from "../../../components/UserIconImg";

export default function Picture() {
  const { id: loggedInUserID, iconFileName, iconSASURL } = React.useContext(UserContext);
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
        <UserIconImg
            id={loggedInUserID}
            userIcon={iconFileName}
            userIconURL={iconSASURL}
            length="50px"
        />
        <FileUploadButton text="Change" onChange={onFileChange} />
        <p>
            Remove
        </p>
    </Box>
  );
}
