import React from "react";
import GoogleIcon from "@mui/icons-material/Google";

import { useServerCall } from "../../../../customHooks/useServerCall";
import { UserContext } from "../../../../contexts/UserContext";
import IconButtonVS from "../../../../components/IconButton";

export default function GoogleAuth() {
  const fetchData = useServerCall();
  const { setName, setID, setIconFileName, setIconSASURL } =
    React.useContext(UserContext);

  const handleClick = React.useCallback(
    (event) => {
      fetchData("google/login", (json) => {
        // TODO: this data comes in on reload, right? so this setting logic  belongs in useLoadSession?
        const tempToken = json.session_token;
        sessionStorage.setItem("tempSessionToken", tempToken);
        setName(json.user_data.name);
        setID(json.user_data.id);
        setIconFileName(json.user_data.profile_icon);
        setIconSASURL(json.user_data.profile_icon_sas_url);
      });
    },
    [fetchData, setID, setIconFileName, setIconSASURL, setName],
  );

  return (
    <IconButtonVS handleClick={handleClick}>
      <GoogleIcon />
    </IconButtonVS>
  );
}
