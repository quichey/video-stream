import React from "react";
import { MenuItem } from "@mui/material";

import { useServerCall } from "../../../customHooks/useServerCall";
import { UserContext } from "../../../contexts/UserContext";

export default function Logout() {
  const fetchData = useServerCall();
  const { setName, setID, setIconFileName, setIconSASURL } =
    React.useContext(UserContext);

  const handleClick = React.useCallback(
    (event) => {
      fetchData("logout", (json) => {
        const tempToken = json.session_token;
        sessionStorage.setItem("tempSessionToken", tempToken);
        setName(undefined);
        setID(undefined);
        setIconFileName(undefined);
        setIconSASURL(undefined);
      });
    },
    [fetchData, setID, setIconFileName, setIconSASURL, setName],
  );

  return (
    <div>
      <MenuItem onClick={handleClick}>Logout</MenuItem>
    </div>
  );
}
