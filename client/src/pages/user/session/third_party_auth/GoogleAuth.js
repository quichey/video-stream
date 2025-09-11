import React from "react";
import GoogleIcon from "@mui/icons-material/Google";

import IconButtonVS from "../../../../components/IconButton";
import { UserContext } from "../../../../contexts/UserContext";
import { HTTPContext } from "../../../../contexts/HTTPContext";
export default function GoogleAuth() {
  const { setName, setID, setIconFileName, setIconSASURL } =
    React.useContext(UserContext);
  const { serverURL } = React.useContext(HTTPContext);
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
          const { auth_cookie_info } = payload;
          const { name, value, path, max_age, secure, samesite } =
            auth_cookie_info;
          window.document.cookie = `${name}=${encodeURIComponent(value)}; path=${path}; max-age=${max_age}; ${secure ? "Secure;" : ""} SameSite=${samesite}`;
          setName(payload.user_data.name);
          setID(payload.user_data.id);
          setIconFileName(payload.user_data.profile_icon);
          setIconSASURL(payload.user_data.profile_icon_sas_url);
          window.removeEventListener("message", handleMessage);
          popup.close();
        }
      });
    },
    [setID, setIconFileName, setIconSASURL, setName, serverURL],
  );

  return (
    <IconButtonVS handleClick={handleClick}>
      <GoogleIcon />
    </IconButtonVS>
  );
}
