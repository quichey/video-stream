import React from "react";
import { ListItemButton, ListItemIcon, ListItemText } from "@mui/material";
import SubscriptionsIcon from "@mui/icons-material/Subscriptions";
import { NavLink } from "react-router-dom";

export default function Subscriptions({ collapsed }) {
  return (
    <ListItemButton component={NavLink} to="/subscriptions">
      <ListItemIcon>
        <SubscriptionsIcon />
      </ListItemIcon>
      {!collapsed && <ListItemText primary="Subscriptions" />}
    </ListItemButton>
  );
}
