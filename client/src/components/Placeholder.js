// Placeholder.js
import React from "react";
import { Box, Typography } from "@mui/material";

export default function Placeholder({ label = "Coming Soon" }) {
  return (
    <Box
      sx={{
        border: "1px dashed gray",
        borderRadius: 2,
        p: 2,
        textAlign: "center",
        color: "gray",
        minHeight: 80,
      }}
    >
      <Typography variant="body2">{label}</Typography>
    </Box>
  );
}
