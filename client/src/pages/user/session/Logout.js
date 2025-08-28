import React, { useState } from "react";
import { Popover, Button, MenuItem, Typography } from "@mui/material";

import { useServerCall } from "../../../customHooks/useServerCall";

export default function Logout() {
    const fetchData = useServerCall();

  const handleClick = React.useCallback((event) => {
    fetchData("logout", (json) => {
        const tempToken = json.session_token
        sessionStorage.setItem("tempSessionToken", tempToken);
    });
  }, []);


  return (
    <div>
        <MenuItem onClick={handleClick}>Logout</MenuItem>
    </div>
  );
}
