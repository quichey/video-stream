import React, { useState } from "react";
import { Button, MenuItem } from "@mui/material";
import {
  Stack,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
} from "@mui/material";

import { useServerCall } from "../../../customHooks/useServerCall";
import { UserContext } from "../../../contexts/UserContext";

import UserNameInput from "../../../components/UserNameInput";
import PasswordInput from "../../../components/PasswordInput";

export default function Register() {
  const [open, setOpen] = useState(false);
  const [name, setName] = useState("");
  const [nameError, setNameError] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [passwordError, setPasswordError] = useState("");
  const fetchData = useServerCall();
  const { setName: setUserName, setID } = React.useContext(UserContext);

  const handleClick = React.useCallback((event) => {
    setOpen(true);
  }, []);

  const handleRegister = React.useCallback(() => {
    // handle register logic here
    // Do Server api
    fetchData(
      "register",
      (json) => {
        const tempToken = json.session_token;
        sessionStorage.setItem("tempSessionToken", tempToken);
        setUserName(name);
        setID(json?.user_data?.id);
        setOpen(false);
      },
      { user_name: name, email: email, password: password },
    );
  }, [fetchData, name, email, password, setUserName, setID]);

  const handleNameChange = React.useCallback((val) => {
    if (val !== undefined) {
      setName(val);
    }
  }, []);

  const handleEmailChange = React.useCallback((e) => {
    if (e.target?.value !== undefined) {
      setEmail(e.target.value);
    }
  }, []);

  const handlePasswordChange = React.useCallback((val) => {
    if (val !== undefined) {
      setPassword(val);
    }
  }, []);

  const disabled = !!nameError || !!passwordError || !name || !password;

  return (
    <div>
      <MenuItem onClick={handleClick} data-testid="register-menu-item">
        Register
      </MenuItem>
      <Dialog
        open={open}
        onClose={() => setOpen(false)}
        maxWidth="sm"
        fullWidth
        data-testid="register-dialogue"
      >
        <DialogTitle>Register</DialogTitle>
        <DialogContent>
          <Stack spacing={4} sx={{ pt: 2 }}>
            <UserNameInput
              value={name}
              onChange={handleNameChange}
              error={nameError}
              setError={setNameError}
              textFieldProps={{ "data-testid": "register-name" }}
            />
            <TextField
              autoFocus
              margin="dense"
              label="Email"
              type="email"
              fullWidth
              value={email}
              onChange={handleEmailChange}
            />
            <PasswordInput
              value={password}
              onChange={handlePasswordChange}
              error={passwordError}
              setError={setPasswordError}
              textFieldProps={{ "data-testid": "register-password" }}
            />
          </Stack>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpen(false)}>Cancel</Button>
          <Button
            variant="contained"
            onClick={handleRegister}
            disabled={disabled}
            data-testid="register-submit"
          >
            Register
          </Button>
        </DialogActions>
      </Dialog>
    </div>
  );
}
