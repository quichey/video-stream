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
      component="form"
      sx={{
        "& > :not(style)": { m: 1, width: "100%" },
      }}
      noValidate
      display="flex"
      flexDirection="row"
      autoComplete="off"
      style={{
        border: "1px solid grey",
        borderRadius: 5,
        marginTop: 10,
        marginBottom: 10,
        paddingBottom: 10,
        width: "100%",
      }}
    >
      <SidebarButton handleClick={handleSidbarClick} />
      <Search />
      <NavLink to={"/upload"} end>
        <IconButton aria-label="create" size="small" style={{ width: 50 }}>
          <VideocamIcon fontSize="inherit" />
          {/*
          TODO: I think add navlink to /upload route here
          */}
        </IconButton>
      </NavLink>
      <IconButton aria-label="notifications" size="small" style={{ width: 50 }}>
        <NotificationsIcon fontSize="inherit" />
      </IconButton>
      <SessionButton />
    </Box>
  );
}
