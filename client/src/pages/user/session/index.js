import React, { useState } from "react";
import AccountCircleIcon from "@mui/icons-material/AccountCircle";

import IconButtonVS from "../../../components/IconButton";
import SessionMenu from "./SessionMenu";

import { UserContext } from "../../../contexts/UserContext";
import { get_storage_url } from "../../../util/urls";

function SessionButton() {
  const [anchorEl, setAnchorEl] = useState(null);
  const { id, iconFileName, iconSASURL } = React.useContext(UserContext)

  const handleClick = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };
  // TODO: use profiles ICON image as icon
  const img_url = get_storage_url("images", id, iconFileName, iconSASURL)
  const has_profile_pic = id !== undefined && iconFileName !== undefined;

  return (
    <div>
      <IconButtonVS handleClick={handleClick} >
        {
            has_profile_pic ? <img 
                src={img_url} 
                alt="icon" 
                style={{ width: 24, height: 24 }} // size to match MUI icons
            /> : <AccountCircleIcon />
        }
        
      </IconButtonVS>
      <SessionMenu handleClose={handleClose} anchorEl={anchorEl}/>
    </ div>
  );
}

export default SessionButton;
