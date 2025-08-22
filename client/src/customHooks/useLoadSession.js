import { useEffect } from "react";

import { serverURL } from "../pages/index"

export function useLoadSession() {
  useEffect(() => {
    async function initSession() {
      try {
        const res = await fetch(`${serverURL}/api/load-session`);
        if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);

        const data = await res.json();
        const tempToken = data.session_token; // use token from response body

        if (tempToken) {
          sessionStorage.setItem("tempSessionToken", tempToken);
        }
      } catch (err) {
        console.error("Failed to load session", err);
      }
    }

    initSession();
  }, []);
}
