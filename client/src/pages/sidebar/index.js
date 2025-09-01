import React from "react";
import { Box, List } from "@mui/material";

import Home from "./Home";
import Shorts from "./Shorts";
import Subscriptions from "./Subscriptions";
import Music from "./Music";
import You from "./You";
import Downloads from "./Downloads";

const drawerWidth = 240;
const collapsedWidth = 72;

export default function Sidebar({ collapsed }) {
  const renderItem = (Component) => <Component collapsed={collapsed} />;

  return (
    <Box
      sx={{
        width: collapsed ? collapsedWidth : drawerWidth,
        flexShrink: 0,
        bgcolor: "background.paper",
        height: "100%",      // full height of parent container
        display: "flex",
        flexDirection: "column",
        overflowY: "auto",   // scroll if content is too tall
        borderRight: 1,
        borderColor: "divider",
        transition: "width 0.3s", // smooth expand/collapse
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
