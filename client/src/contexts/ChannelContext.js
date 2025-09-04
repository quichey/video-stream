import React, { createContext, useState } from "react";

// 1. Create the context
export const ChannelContext = createContext({
  id: undefined,
  setID: () => {},
  name: undefined,
  setName: () => {},
});

// 2. Create the provider component
export const ChannelProvider = ({ children }) => {
  const [channelID, setChannelID] = useState(0);
  const [channelName, setChannelName] = useState("users_name_0");

  return (
    <ChannelContext.Provider
      value={{
        id: channelID,
        setID: setChannelID,
        name: channelName,
        setName: setChannelName,
      }}
    >
      {children}
    </ChannelContext.Provider>
  );
};
