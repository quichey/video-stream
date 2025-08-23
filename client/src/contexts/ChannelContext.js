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
  const [channelID, setChannelID] = useState(0);
  const [channelName, setChannelName] = useState("users_name_0");

  return (
    <UserContext.Provider
      value={{ id: channelID, setID: setChannelID, name: channelName, setName: setChannelName }}
    >
      {children}
    </UserContext.Provider>
  );
};
