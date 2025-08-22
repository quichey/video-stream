import * as React from "react";

import { HTTPContext } from "../pages";

export const useServerCall = () => {
  const {serverURL, postRequestPayload} = React.useContext(HTTPContext);
  const fetchServer = React.useCallback((route, onResponse, method="POST") => {
      fetch(
        `${serverURL}/${route}`,
        {
          method: method,
          credentials: "include",
          // may need to use POST later for adding params
          // i think don't have to, could use query string
          // POST is probably more secure cause body is probably encrypted
          //method: "POST",
          // body: JSON.stringify({ limit: 30 }),
          // mode: "no-cors",
          body: postRequestPayload
        },
      )
      .then((response) => response.json())
      .then((json) => {
        console.log(json);
        onResponse(json)
      })
      .catch((error) => {
        console.log(error);
      });
  
    }, [serverURL, postRequestPayload])

  return fetchServer;
};
