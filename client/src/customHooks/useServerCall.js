import * as React from "react";

import { HTTPContext } from "../pages";

export const useServerCall = () => {
  const { serverURL, postRequestPayload, refreshSessionToken } =
    React.useContext(HTTPContext);
  const generate_params = React.useCallback(
    (postRequestPayload, extraParams) => {
      let method = "POST";
      if (extraParams.method !== undefined) {
        method = extraParams.method;
      }

      // TODO: add extraParams to postRequestPayload
      let finalPayload = JSON.parse(postRequestPayload);
      if (extraParams.body !== undefined) {
        finalPayload.assign(extraParams.body);
      }
      const finalPayloadStr = JSON.stringify(finalPayload);

      const fetchParams = {
        method: method,
        // may need to use POST later for adding params
        // i think don't have to, could use query string
        // POST is probably more secure cause body is probably encrypted
        //method: "POST",
        // body: JSON.stringify({ limit: 30 }),
        // mode: "no-cors",
        body: finalPayloadStr,
      };

      if (extraParams.headers !== undefined) {
        fetchParams.headers = extraParams.headers;
      }

      return fetchParams;
    },
    [],
  );
  const fetchServer = React.useCallback(
    (route, onResponse, extraParams = {}, extraOnResponseParams = []) => {
      const fetchParams = generate_params(postRequestPayload, extraParams);
      fetch(`${serverURL}/${route}`, fetchParams)
        .then((response) => response.json())
        .then((json) => {
          console.log(json);
          if (extraOnResponseParams) {
            onResponse(
              json,
              extraOnResponseParams[0],
              extraOnResponseParams[1],
            );
          } else {
            onResponse(json);
          }
          refreshSessionToken(json);
        })
        .catch((error) => {
          console.log(error);
        });
    },
    [serverURL, postRequestPayload, refreshSessionToken, generate_params],
  );

  return fetchServer;
};
