// UserNameInput.js
import React, { useState } from "react";
import { Box, TextField } from "@mui/material";
import * as leoProfanity from "leo-profanity";

import { useServerCall } from "../customHooks/useServerCall";

leoProfanity.loadDictionary(); // load default dictionary

const UserNameInput = ({ value, onChange }) => {
  const [error, setError] = useState("");
    const fetchData = useServerCall();

  const validate = (val) => {
    if (!val) return "Username is required.";
    if (val.length < 3) return "Username must be at least 3 characters.";
    if (val.length > 20) return "Username must be less than 20 characters.";
    if (!/^[a-zA-Z0-9_]+$/.test(val))
      return "Username can only contain letters, numbers, and underscores.";
    if (leoProfanity.check(val)) return "Username contains inappropriate words.";
    return "";
  };

  const handleChange = React.useCallback((e) => {
    const val = e.target.value;
    onChange(val);
    setError(validate(val));
  }, [onChange]);

  React.useEffect(() => {
    if (error === "") {
        fetchData("verify-name", (json) => {
            if (!json.verified) {
                setError("Username already taken")
            }
        }, { user_name: value });
    }
  }, [value, fetchData, error])

  return (
    <Box sx={{ minHeight: 80 }}>
        <TextField
            label="Username"
            value={value}
            onChange={handleChange}
            error={Boolean(error)}
            helperText={error}
            fullWidth
        />
    </Box>
  );
};

export default UserNameInput;
