import * as React from "react";
import NotificationsIcon from "@mui/icons-material/Notifications";
import VideocamIcon from "@mui/icons-material/Videocam";
import { Box, IconButton } from "@mui/material";
import { NavLink } from "react-router";

import Search from "./Search";
import SessionButton from "./user/session";
import SidebarButton from "./sidebar/SidebarButton";

export default function Navbar({ handleSidbarClick }) {
  return (
    <Box
      display="flex"
      flexDirection="row"
      alignItems="center"
      justifyContent="space-between"
      sx={{
        position: "fixed",
        top: 0,
        left: 0,
        width: "100%",
        zIndex: 1200,
      }}
    >
      {/* Left Section */}
      <Box display="flex" alignItems="center">
        <SidebarButton handleClick={handleSidbarClick} />
      </Box>

      {/* Center Section */}
      <Box flex={1} display="flex" justifyContent="center">
        <Search />
      </Box>

      {/* Right Section */}
      <Box display="flex" alignItems="center">
        <NavLink to="/upload" end>
          <IconButton aria-label="create" size="small">
            <VideocamIcon fontSize="inherit" />
          </IconButton>
        </NavLink>
        <IconButton aria-label="notifications" size="small">
          <NotificationsIcon fontSize="inherit" />
        </IconButton>
        <SessionButton />
      </Box>
    </Box>
  );
}
