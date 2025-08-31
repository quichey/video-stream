// PicturePreview.js
import React from "react";
import { AccountCircle } from "@mui/icons-material";
import { useUserPictureEdit } from "../../../contexts/UserPictureEditContext";
import UserIconImg from "../../../components/UserIconImg";
import { UserContext } from "../../../contexts/UserContext";

export default function PicturePreview() {
  const { preview, remove } = useUserPictureEdit();
  const { id: loggedInUserID, iconFileName, iconSASURL } = React.useContext(UserContext);

  if (preview) {
    return <img src={preview} alt="Preview" style={{ width: 50, height: 50 }} />;
  }

  if (remove) {
    return <AccountCircle style={{ width: 50, height: 50 }} />;
  }

  return (
    <UserIconImg
      id={loggedInUserID}
      userIcon={iconFileName}
      userIconURL={iconSASURL}
      length="50px"
    />
  );
}
