import React, { createContext, useState } from "react";

// 1. Create the context
export const VideoContext = createContext({
  id: "none",
  fileName: undefined,
  fileDir: undefined,
  setID: () => {},
  setFileName: () => {},
  setFileDir: () => {},
});

// 2. Create the provider component
export const VideoProvider = ({ children }) => {
  const [id, setID] = useState("none");
  const [fileName, setFileName] = useState(undefined);
  const [fileDir, setFileDir] = useState(undefined);

  return (
    <VideoContext.Provider
      value={{ id, setID, fileName, setFileName, fileDir, setFileDir }}
    >
      {children}
    </VideoContext.Provider>
  );
};
