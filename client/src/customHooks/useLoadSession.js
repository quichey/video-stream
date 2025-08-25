import { useEffect, useState } from "react";

import { serverURL } from "../contexts/HTTPContext";

export function useLoadSession() {
  const [loaded, setLoaded] = useState(false); // initially false
  useEffect(() => {
    async function initSession() {
      try {
        const res = await fetch(`${serverURL}/load-session`, {method: "POST", credentials: "include"});
        if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);

        const data = await res.json();
        const tempToken = data.session_token; // use token from response body

        if (tempToken) {
          sessionStorage.setItem("tempSessionToken", tempToken);
          setLoaded(true); // token retrieved
        } else{
            setLoaded(false)
        }
      } catch (err) {
        console.error("Failed to load session", err);
      }
    }

    initSession();
  }, []);
  return loaded;
}
