import { useEffect } from "react";

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(";").shift();
  return null;
}

export function useLoadSession() {
  useEffect(() => {
    fetch("/api/load-session")
      .then(() => {
        const tempToken = getCookie("temp_session");
        if (tempToken) sessionStorage.setItem("tempSessionToken", tempToken);
      })
      .catch(err => console.error("Failed to load session", err));
  }, []);
}
