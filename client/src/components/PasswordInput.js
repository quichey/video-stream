// PasswordInput.js
import React, { useState } from "react";
import { TextField, LinearProgress, Typography, Box } from "@mui/material";
import zxcvbn from "zxcvbn";

const PasswordInput = ({
  value,
  onChange,
  error,
  setError,
  textFieldProps = {},
}) => {
  const [strength, setStrength] = useState(null);

  const validate = (val) => {
    if (!val) return "Password is required.";
    if (val.length < 8) return "Password must be at least 8 characters.";
    if (!/[A-Z]/.test(val))
      return "Password must include at least one uppercase letter.";
    if (!/[a-z]/.test(val))
      return "Password must include at least one lowercase letter.";
    if (!/[0-9]/.test(val)) return "Password must include at least one number.";
    if (!/[!@#$%^&*(),.?":{}|<>]/.test(val))
      return "Password must include at least one special character.";
    return "";
  };

  const handleChange = (e) => {
    const val = e.target.value;
    onChange(val);

    // run rules validation
    const rulesError = validate(val);
    setError(rulesError);

    // run zxcvbn analysis
    if (val) {
      setStrength(zxcvbn(val));
    } else {
      setStrength(null);
    }
  };

  const getStrengthColor = (score) => {
    switch (score) {
      case 0:
      case 1:
        return "error"; // red
      case 2:
        return "warning"; // orange
      case 3:
        return "info"; // blue
      case 4:
        return "success"; // green
      default:
        return "inherit";
    }
  };

  return (
    <Box sx={{ minHeight: 160 }}>
      <TextField
        label="Password"
        type="password"
        value={value}
        onChange={handleChange}
        error={Boolean(error)}
        helperText={error}
        fullWidth
        {...textFieldProps}
      />
      {strength && (
        <Box mt={1}>
          <LinearProgress
            variant="determinate"
            value={(strength.score + 1) * 20}
            color={getStrengthColor(strength.score)}
          />
          <Typography variant="body2" color="textSecondary">
            {strength.feedback.warning || " "}
          </Typography>
          {strength.feedback.suggestions.length > 0 && (
            <Typography variant="caption" color="textSecondary">
              {strength.feedback.suggestions.join(" ")}
            </Typography>
          )}
        </Box>
      )}
    </Box>
  );
};

export default PasswordInput;
