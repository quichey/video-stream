import React from "react";
import { Box, List } from "@mui/material";

import Home from "./Home";
import Shorts from "./Shorts";
import Subscriptions from "./Subscriptions";
import Music from "./Music";
import You from "./You";
import Downloads from "./Downloads";

import { collapsedWidth, drawerWidth, navbarHeight } from "..";

export default function Sidebar({ collapsed }) {
  const renderItem = (Component) => <Component collapsed={collapsed} />;

  return (
    <Box
      sx={{
        position: "fixed",
        top: navbarHeight, // sits below Navbar
        left: 0,
        width: collapsed ? collapsedWidth : drawerWidth,
        height: `calc(100vh - ${navbarHeight}px)`,
        bgcolor: "background.paper",
        borderRight: 1,
        borderColor: "divider",
        transition: "width 0.3s ease",
        overflowY: "auto", // Sidebar can scroll independently if items overflow
        zIndex: 1100,
      }}
    >
      <List sx={{ p: 0 }}>
        {renderItem(Home)}
        {renderItem(Shorts)}
        {renderItem(Subscriptions)}
        {renderItem(Music)}
        {renderItem(You)}
        {renderItem(Downloads)}
      </List>
    </Box>
  );
}
