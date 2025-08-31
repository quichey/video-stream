// Picture.js
import React from "react";
import { Box, Stack } from "@mui/material";
import { UserPictureEditProvider } from "./UserPictureEditContext";
import PicturePreview from "./PicturePreview";
import PictureUploadButton from "./PictureUploadButton";
import PictureRemoveButton from "./PictureRemoveButton";
import PicturePublishButton from "./PicturePublishButton";

export default function PictureContainer() {
  return (
    <UserPictureEditProvider>
      <Picture />
    </UserPictureEditProvider>
  );
}

function Picture() {
  return (
    <Box
      component="form"
      sx={{ "& > :not(style)": { m: 1, width: "100%" } }}
      noValidate
      display="flex"
      flexDirection="column"
      autoComplete="off"
      style={{ width: "100%" }}
    >
      <Stack spacing={2}>
        <PicturePreview />
        <PictureUploadButton />
        <PictureRemoveButton />
        <PicturePublishButton />
      </Stack>
    </Box>
  );
}
