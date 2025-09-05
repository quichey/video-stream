import { useCallback, useContext } from "react";

import { HTTPContext } from "../contexts/HTTPContext";
import { buildRequestBody } from "../api/httpUtils";

export const useServerCall = () => {
  const { serverURL } = useContext(HTTPContext);

  const fetchData = useCallback(
    async (route, onResponse, httpParams = {}, method = "POST") => {
      try {
        const res = await fetch(`${serverURL}/${route}`, {
          method,
          credentials: "include",
          body: buildRequestBody(httpParams),
        });

        if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);

        const data = await res.json();

        if (onResponse && typeof onResponse === "function") {
          onResponse(data);
        }

        return data; // still return the data in case caller wants it
      } catch (err) {
        console.error("Server call failed", err);
        throw err; // propagate error
      }
    },
    [serverURL],
  );

  return fetchData;
};
