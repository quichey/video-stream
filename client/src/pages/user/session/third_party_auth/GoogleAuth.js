import React from "react";
import GoogleIcon from "@mui/icons-material/Google";

import IconButtonVS from "../../../../components/IconButton";

export default function GoogleAuth() {
  const handleClick = React.useCallback((event) => {
    window.location.href = "http://localhost:5000/google/login";
  }, []);

  return (
    <IconButtonVS handleClick={handleClick}>
      <GoogleIcon />
    </IconButtonVS>
  );
}
