import React, { useRef } from "react";
import { Button } from "@mui/material";

export default function FileUploadButton({ text, onChange }) {
  const fileInputRef = useRef(null);

  const handleButtonClick = () => {
    fileInputRef.current.click();
  };

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      onChange(file);
    }
  };

  return (
    <>
      <input
        type="file"
        ref={fileInputRef}
        style={{ display: "none" }}
        onChange={handleFileChange}
      />
      <Button variant="contained" onClick={handleButtonClick}>
        {text}
      </Button>
    </>
  );
}
