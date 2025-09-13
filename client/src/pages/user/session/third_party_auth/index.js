import React from "react";
import { MenuItem } from "@mui/material";

import GoogleAuth from "./GoogleAuth";

export default function ThirdPartyAuths() {
  return (
    <div>
      <MenuItem>
        <GoogleAuth />
      </MenuItem>
    </div>
  );
}
