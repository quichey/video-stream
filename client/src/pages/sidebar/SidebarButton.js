import React from "react";
import MenuIcon from "@mui/icons-material/Menu";

import IconButtonVS from "../../components/IconButton";

function SidebarButton({ handleClick }) {
  return (
    <div>
      <IconButtonVS handleClick={handleClick}>
        <MenuIcon />
      </IconButtonVS>
    </div>
  );
}

export default SidebarButton;
