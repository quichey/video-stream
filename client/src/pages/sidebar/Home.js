import React from "react";
import { ListItemButton, ListItemIcon, ListItemText } from "@mui/material";
import HomeIcon from "@mui/icons-material/Home";
import { NavLink } from "react-router-dom";

export default function Home({ collapsed }) {
  return (
    <ListItemButton component={NavLink} to="/">
      <ListItemIcon>
        <HomeIcon />
      </ListItemIcon>
      {!collapsed && <ListItemText primary="Home" />}
    </ListItemButton>
  );
}
