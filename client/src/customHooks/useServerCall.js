import * as React from "react";

import { HTTPContext } from "../pages";

export const useServerCall = () => {
  const httpContext = React.useContext(HTTPContext);
  const fetchServer = React.useCallback((route, onResponse, method="POST") => {
      fetch(
        `${httpContext.serverURL}/${route}`,
        {
          method: method,
          // may need to use POST later for adding params
          // i think don't have to, could use query string
          // POST is probably more secure cause body is probably encrypted
          //method: "POST",
          // body: JSON.stringify({ limit: 30 }),
          // mode: "no-cors",
          body: httpContext.postRequestPayload
        },
      )
      .then((response) => response.json())
      .then((json) => {
        console.log(json);
        onResponse(json)
        httpContext.refreshSessionToken(json);
      })
      .catch((error) => {
        console.log(error);
      });
  
    }, [httpContext])

  return fetchServer;
};
