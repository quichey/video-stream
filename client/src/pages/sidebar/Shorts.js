import React from "react";
import { ListItemButton, ListItemIcon, ListItemText } from "@mui/material";
import AppShortcutIcon from '@mui/icons-material/AppShortcut';
import { NavLink } from "react-router-dom";

export default function Shorts({ collapsed }) {
  return (
    <ListItemButton component={NavLink} to="/shorts">
      <ListItemIcon>
        <AppShortcutIcon />
      </ListItemIcon>
      {!collapsed && <ListItemText primary="Shorts" />}
    </ListItemButton>
  );
}
