import * as React from "react";

import { HTTPContext } from "../pages";

export const useServerCall = () => {
  const { serverURL, postRequestPayload, refreshSessionToken } =
    React.useContext(HTTPContext);
  const fetchServer = React.useCallback(
    (route, onResponse, method = "POST", extraParams = {}) => {
      // TODO: add extraParams to postRequestPayload
      var payloadJSON = JSON.parse(postRequestPayload);
      const finalPayload = { ...payloadJSON, ...extraParams };
      const finalPayloadStr = JSON.stringify(finalPayload);
      fetch(`${serverURL}/${route}`, {
        method: method,
        // may need to use POST later for adding params
        // i think don't have to, could use query string
        // POST is probably more secure cause body is probably encrypted
        //method: "POST",
        // body: JSON.stringify({ limit: 30 }),
        // mode: "no-cors",
        body: finalPayloadStr,
      })
        .then((response) => response.json())
        .then((json) => {
          console.log(json);
          onResponse(json);
          refreshSessionToken(json);
        })
        .catch((error) => {
          console.log(error);
        });
    },
    [serverURL, postRequestPayload, refreshSessionToken],
  );

  return fetchServer;
};
