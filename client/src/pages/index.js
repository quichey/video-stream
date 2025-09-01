import * as React from "react";
import { BrowserRouter, Routes, Route } from "react-router";
import { Box } from "@mui/material";

import Home from "./home";
import Watch from "./watch";
import User from "./user";
import CustomizeChannel from "./user/edit/CustomizeChannel";
import VideoUpload from "./video_upload";
import Navbar from "./Navbar";

import { useLoadSession } from "../customHooks/useLoadSession";
import Loading from "../components/Loading";
import Sidebar from "./sidebar";

export const drawerWidth = 240;
export const collapsedWidth = 72;
export const navbarHeight = 64;

export default function Pages() {
  const [collapsed, setCollapsed] = React.useState(true);

  const toggleCollapsed = () => setCollapsed((prev) => !prev);
  

  React.useEffect(() => {
    // Cleanup function: remove temp-session token from sessionStorage on unmount
    return () => {
      sessionStorage.removeItem("tempSessionToken");
    };
  }, []); // empty dependency array → cleanup on unmount

  // This will handle fetching session from the server and saving temp-session from cookie
  const sessionLoaded = useLoadSession();
  if (!sessionLoaded) return <Loading />;
  return (
    <BrowserRouter>
      <Navbar handleSidbarClick={toggleCollapsed} />
      <Sidebar collapsed={collapsed}/>
      <Box
        component="main"
        sx={{
          mt: `${navbarHeight}px`,
          ml: collapsed ? `${collapsedWidth}px` : `${drawerWidth}px`,
          p: 2,
        }}
      >
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="watch">
            <Route path=":videoID" element={<Watch />} />
          </Route>
          <Route path="channel">
            <Route path=":userID">
              <Route index element={<User />} />
              <Route path="editing">
                <Route path="profile" element={<CustomizeChannel />} />
              </Route>
            </Route>
          </Route>
          <Route
            index
            path="upload"
            element={<VideoUpload />}
          />
        </Routes>
      </Box>
    </BrowserRouter>
  );
}
