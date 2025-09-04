import React, { createContext } from "react";

export const serverURL =
  process.env.REACT_APP_SERVER_APP_URL || process.env.REACT_APP_API_BASE;

// 1. Create the context
export const HTTPContext = createContext({
  serverURL: undefined,
});

// 2. Create the provider component
export const HTTPProvider = ({ children }) => {
  return (
    <HTTPContext.Provider value={{ serverURL }}>
      {children}
    </HTTPContext.Provider>
  );
};
