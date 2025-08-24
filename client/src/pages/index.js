import * as React from "react";
import { BrowserRouter, Routes, Route } from "react-router";
import { Box } from "@mui/material";

import Home from "./home";
import Watch from "./watch";
import User from "./user";
import VideoUpload from "./video_upload";
import Navbar from "./Navbar";


export default function Pages() {
  return (
    <BrowserRouter>
      <Box
        component="form"
        sx={{
          "& > :not(style)": { m: 1, width: "100%" },
        }}
        noValidate
        display="flex"
        flexDirection="column"
        autoComplete="off"
        style={{
          width: "100%",
        }}
      >
        <Navbar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="watch">
            <Route path=":videoID" element={<Watch />} />
          </Route>
          <Route path="channel">
            <Route path=":userID" element={<User />} />
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
