import * as React from "react";
import { Box } from "@mui/material";

import Home from "./home";
import Watch from "./watch";
import Navbar from "./Navbar";

export default function Pages() {
  const [userID, setUserID] = React.useState(0)
  const [sessionToken, setSessionToken] = React.useState()
  const [page, setPage] = React.useState("home")
    const [pageComponent, setPageComponent] = React.useState()
    const [videoID, setVideoID] = React.useState(0)

    React.useEffect(() => {
        switch(page) {
            case "home":
                setPageComponent(
                    <Home userID={userID} sessionToken={sessionToken} setSessionToken={setSessionToken} />
                )
                break;
            case "watch":
                setPageComponent(
                    <Watch userID={userID} sessionToken={sessionToken} setSessionToken={setSessionToken} videoID={videoID}/>
                )
                break;
        }
    }, [page])
  return (
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
      {
        pageComponent
      }
    </Box>
  );
}
