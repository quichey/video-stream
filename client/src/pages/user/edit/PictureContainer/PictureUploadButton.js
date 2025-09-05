// PictureUploadButton.js
import React from "react";
import FileUploadButton from "../../../../components/FileUploadButton";
import { useUserPictureEdit } from "./UserPictureEditContext";
import { readFile } from "../../../../util/fileRead";

export default function PictureUploadButton() {
  const { setPreview, setFileBytes, setFileName, setRemove } =
    useUserPictureEdit();

  const onFileChange = (file) => {
    setRemove(false);
    const reader = new FileReader();
    reader.onloadend = () => setPreview(reader.result);
    reader.readAsDataURL(file);

    setFileName(file.name);
    readFile(file, setFileBytes);
  };

  return <FileUploadButton text="Change" onChange={onFileChange} />;
}
