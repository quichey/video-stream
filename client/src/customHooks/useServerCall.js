import { useCallback } from "react";
import { useContext } from "react";

import { HTTPContext } from "../contexts/HTTPContext";
import { buildRequestBody } from "../api/httpUtils";

export const useServerCall = () => {
  const { serverURL } = useContext(HTTPContext);

  const fetchServer = useCallback(
    async (route, httpParams = {}, method = "POST") => {
      try {
        const res = await fetch(`${serverURL}/${route}`, {
          method,
          credentials: "include",
          body: buildRequestBody(httpParams),
        });

        if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
        const data = await res.json();
        return data; // caller can handle response
      } catch (err) {
        console.error("Server call failed", err);
        throw err; // propagate error to caller
      }
    },
    [serverURL]
  );

  return fetchServer;
};
