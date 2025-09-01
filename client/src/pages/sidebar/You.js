import React from "react";
import { ListItemButton, ListItemIcon, ListItemText } from "@mui/material";
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import { NavLink } from "react-router-dom";

export default function You({ collapsed }) {
  return (
    <ListItemButton component={NavLink} to="/you">
      <ListItemIcon>
        <AccountCircleIcon />
      </ListItemIcon>
      {!collapsed && <ListItemText primary="You" />}
    </ListItemButton>
  );
}
