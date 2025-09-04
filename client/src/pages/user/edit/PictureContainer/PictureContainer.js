import React from "react";
import { Box, Stack, Typography } from "@mui/material";
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
    <Box>
      <Stack spacing={1}>
        <Typography variant="h6">Profile Picture</Typography>
        <Typography variant="body2" color="textSecondary">
          This will be shown on your profile.
        </Typography>
      </Stack>
      <Stack direction="row" spacing={2} alignItems="center">
        <PicturePreview />
        <Stack spacing={1} flex={1}>
          <Typography variant="body1">
            Your profile picture is shown on your public profile.
          </Typography>
          <Stack direction="row" spacing={1}>
            <PictureUploadButton />
            <PictureRemoveButton />
            <PicturePublishButton />
          </Stack>
        </Stack>
      </Stack>
    </Box>
  );
}
