import * as React from "react";
import AccountCircleIcon from "@mui/icons-material/AccountCircle";
import DehazeIcon from "@mui/icons-material/Dehaze";
import NotificationsIcon from "@mui/icons-material/Notifications";
import VideocamIcon from "@mui/icons-material/Videocam";
import {
  Box,
  Container,
  IconButton,
  FormControl,
  Select,
  MenuItem,
  InputLabel,
  TextField,
  Typography,
} from "@mui/material";

import Search from "./Search";

export default function Navbar() {
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
      <IconButton aria-label="drawer" size="small" style={{ width: 50 }}>
        <DehazeIcon fontSize="inherit" />
      </IconButton>
      <Search />
      <IconButton aria-label="create" size="small" style={{ width: 50 }}>
        <VideocamIcon fontSize="inherit" />
      </IconButton>
      <IconButton aria-label="notifications" size="small" style={{ width: 50 }}>
        <NotificationsIcon fontSize="inherit" />
      </IconButton>
      <IconButton aria-label="profile" size="small" style={{ width: 50 }}>
        <AccountCircleIcon fontSize="inherit" />
      </IconButton>
    </Box>
  );
}
