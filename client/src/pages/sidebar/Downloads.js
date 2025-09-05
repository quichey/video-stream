import React from "react";
import { ListItemButton, ListItemIcon, ListItemText } from "@mui/material";
import DownloadIcon from "@mui/icons-material/Download";
import { NavLink } from "react-router-dom";

export default function Downloads({ collapsed }) {
  return (
    <ListItemButton component={NavLink} to="/downloads">
      <ListItemIcon>
        <DownloadIcon />
      </ListItemIcon>
      {!collapsed && <ListItemText primary="Downloads" />}
    </ListItemButton>
  );
}
