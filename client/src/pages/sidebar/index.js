import React, { useState } from "react";
import { Drawer, List, Divider, IconButton, Box } from "@mui/material";
import MenuIcon from "@mui/icons-material/Menu";

import Home from "./Home";
import Shorts from "./Shorts";
import Subscriptions from "./Subscriptions";
import Music from "./Music";
import You from "./You";
import Downloads from "./Downloads";

const drawerWidth = 240;
const collapsedWidth = 72;

export default function Sidebar() {
  const [collapsed, setCollapsed] = useState(false);

  const toggleCollapsed = () => setCollapsed((prev) => !prev);

  const renderItem = (Component) => (
    <Component collapsed={collapsed} />
  );

  return (
    <Drawer
      variant="permanent"
      sx={{
        width: collapsed ? collapsedWidth : drawerWidth,
        flexShrink: 0,
        "& .MuiDrawer-paper": {
          width: collapsed ? collapsedWidth : drawerWidth,
          boxSizing: "border-box",
        },
      }}
    >
      <Box
        display="flex"
        alignItems="center"
        justifyContent={collapsed ? "center" : "flex-end"}
        px={1}
        py={1}
      >
        <IconButton onClick={toggleCollapsed}>
          <MenuIcon />
        </IconButton>
      </Box>

      <Divider />

      <List>
        {renderItem(Home)}
        {renderItem(Shorts)}
        {renderItem(Subscriptions)}
        {renderItem(Music)}
        {renderItem(You)}
        {renderItem(Downloads)}
      </List>
    </Drawer>
  );
}
