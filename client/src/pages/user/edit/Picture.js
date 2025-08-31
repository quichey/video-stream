import * as React from "react";
import AccountCircleIcon from "@mui/icons-material/AccountCircle";
import { Box } from "@mui/material";

import { UserContext } from "../../../contexts/UserContext";

import { useServerCall } from "../../../customHooks/useServerCall";

import FileUploadButton from "../../../components/FileUploadButton";
import UserIconImg from "../../../components/UserIconImg";
import { readFile } from "../../../util/fileRead";
import ButtonVS from "../../../components/TextButton";

export default function Picture() {
    const [fileBytes, setFileBytes] = React.useState(new Uint8Array(0));
    const [fileName, setFileName] = React.useState(new Uint8Array(0));
    const [preview, setPreview] = React.useState(null);
    const [remove, setRemove] = React.useState(null);
  const { id: loggedInUserID, iconFileName, iconSASURL } = React.useContext(UserContext);
  const fetchData = useServerCall()

  const onFileChange = (file) => {
    const reader = new FileReader();
      reader.onloadend = () => {
        setPreview(reader.result); // base64 string
      };
      reader.readAsDataURL(file);
    setFileName(file.name)
    readFile(file, setFileBytes)
  }

  const onPublish = () => {
    if (remove) {
        fetchData("remove-profile-pic", (json) => {
            console.log(json)
        })
    }
    else {
        fetchData("upload-profile-pic", (json) => {
            console.log(json)
        }, {
            "file_name": fileName,
            "byte_stream": fileBytes
        })
    }
  }
  let displayedPic = 
                <UserIconImg
                    id={loggedInUserID}
                    userIcon={iconFileName}
                    userIconURL={iconSASURL}
                    length="50px"
                />
    if (!!preview) {
        displayedPic = <img src={preview} alt="Preview" style={{ width: 50, height: 50}}/>
    }
    else if (remove) {
        displayedPic = <AccountCircleIcon />
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
        {displayedPic}
        <FileUploadButton text="Change" onChange={onFileChange} />
        <ButtonVS text="Remove" handleClick={() => {
            setRemove(true)
        }}/>
        <ButtonVS text="Publish" handleClick={onPublish}/>
    </Box>
  );
}
