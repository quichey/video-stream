import React from "react";
import GoogleIcon from "@mui/icons-material/Google";

import IconButtonVS from "../../../../components/IconButton";
import { UserContext } from "../../../../contexts/UserContext";
import { HTTPContext } from "../../../../contexts/HTTPContext";
import { useServerCall } from "../../../../customHooks/useServerCall";

export default function GoogleAuth() {
  const { setName, setID, setIconFileName, setIconSASURL } =
    React.useContext(UserContext);
  const { serverURL } = React.useContext(HTTPContext);
  const fetchData = useServerCall();
  const handleClick = React.useCallback(
    (event) => {
      const width = 500;
      const height = 600;
      const left = (window.innerWidth - width) / 2;
      const top = (window.innerHeight - height) / 2;
      const tempSessionToken = sessionStorage.getItem("tempSessionToken");
      const popup = window.open(
        `${serverURL}/google/login?session_token=${encodeURIComponent(tempSessionToken)}`,
        "google-login",
        `width=${width},height=${height},top=${top},left=${left}`,
      );

      // Listen for the message from popup
      window.addEventListener("message", function handleMessage(event) {
        if (event.origin !== serverURL) return; // validate origin
        const { payload } = event.data;
        if (payload) {
          const tempToken = payload.session_token;
          sessionStorage.setItem("tempSessionToken", tempToken);
          const oneTimeToken = payload.one_time_token;
          fetchData(
            "auth/set_cookie",
            (json) => {
              const tempToken = json.session_token;
              sessionStorage.setItem("tempSessionToken", tempToken);
              setName(json.user_data.name);
              setID(json.user_data.id);
              setIconFileName(json.user_data.profile_icon);
              setIconSASURL(json.user_data.profile_icon_sas_url);
            },
            { one_time_token: oneTimeToken },
          );
          window.removeEventListener("message", handleMessage);
          popup.close();
        }
      });
    },
    [setID, setIconFileName, setIconSASURL, setName, serverURL, fetchData],
  );

  return (
    <IconButtonVS handleClick={handleClick}>
      <GoogleIcon />
    </IconButtonVS>
  );
}
