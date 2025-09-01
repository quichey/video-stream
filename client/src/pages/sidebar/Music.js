import React from "react";
import { ListItemButton, ListItemIcon, ListItemText } from "@mui/material";
import LibraryMusicIcon from '@mui/icons-material/LibraryMusic';
import { NavLink } from "react-router-dom";

export default function Music({ collapsed }) {
  return (
    <ListItemButton component={NavLink} to="/music">
      <ListItemIcon>
        <LibraryMusicIcon />
      </ListItemIcon>
      {!collapsed && <ListItemText primary="Music" />}
    </ListItemButton>
  );
}
