// UserPictureEditContext.js
import React, { createContext, useContext, useState } from "react";

const UserPictureEditContext = createContext();
export const useUserPictureEdit = () => useContext(UserPictureEditContext);

export const UserPictureEditProvider = ({ children }) => {
  const [fileBytes, setFileBytes] = useState(new Uint8Array(0));
  const [fileName, setFileName] = useState("");
  const [preview, setPreview] = useState(null);
  const [remove, setRemove] = useState(false);

  const reset = () => {
    setFileBytes(new Uint8Array(0));
    setFileName("");
    setPreview(null);
    setRemove(false);
  };

  return (
    <UserPictureEditContext.Provider
      value={{
        fileBytes,
        setFileBytes,
        fileName,
        setFileName,
        preview,
        setPreview,
        remove,
        setRemove,
        reset,
      }}
    >
      {children}
    </UserPictureEditContext.Provider>
  );
};
