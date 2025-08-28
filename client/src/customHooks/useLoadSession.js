import { useEffect, useState, useContext } from "react";

import { serverURL } from "../contexts/HTTPContext";
import { UserContext } from "../contexts/UserContext";

export function useLoadSession() {
  const [loaded, setLoaded] = useState(false); // initially false
  const { setName, setIconFileName, setIconSASURL, setID } = useContext(UserContext)
  useEffect(() => {
    async function initSession() {
      try {
        const res = await fetch(`${serverURL}/load-session`, {method: "POST", credentials: "include"});
        if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);

        const data = await res.json();
        const tempToken = data.session_token; // use token from response body
        const userData = data.user_data;

        if (userData) {
          setName(userData.name)
          setIconFileName(userData.profile_icon)
          setIconSASURL(userData.profile_icon_sas_url)
          setID(userData.id)
        }
        if (tempToken) {
          sessionStorage.setItem("tempSessionToken", tempToken);
          setLoaded(true); // token retrieved
        } else {
            setLoaded(false)
        }
      } catch (err) {
        console.error("Failed to load session", err);
      }
    }

    initSession();
  }, [setID, setIconFileName, setIconSASURL, setName]);
  return loaded;
}
