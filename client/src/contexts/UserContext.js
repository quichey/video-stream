import React, { createContext, useState } from "react";

// 1. Create the context
export const UserContext = createContext({
  id: undefined,
  setID: () => {},
  name: undefined,
  setName: () => {},
});

// 2. Create the provider component
export const UserProvider = ({ children }) => {
  const [id, setID] = useState(undefined);
  const [name, setName] = useState(undefined);

  return (
    <UserContext.Provider
      value={{ id, setID, name, setName }}
    >
      {children}
    </UserContext.Provider>
  );
};
