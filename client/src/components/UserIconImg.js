import * as React from "react";
import AccountCircleIcon from "@mui/icons-material/AccountCircle";

import { get_storage_url } from "../util/urls";

export default function UserIconImg({
  id,
  userIcon,
  userIconURL,
  length = "20px",
}) {
  const img_url = get_storage_url("images", id, userIcon, userIconURL);
  const has_profile_pic = !!id && !!userIcon;
  if (!has_profile_pic)
    return <AccountCircleIcon style={{ width: length, height: length }} />;
  return (
    <img
      alt={userIcon}
      src={img_url}
      width={length}
      height={length}
      style={{
        borderRadius: "50%",
        objectFit: "cover",
      }}
    />
  );
}
