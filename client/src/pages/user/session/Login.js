import React, { useState } from "react";
import { Button, MenuItem } from "@mui/material";
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
} from "@mui/material";

import { useServerCall } from "../../../customHooks/useServerCall";
import { UserContext } from "../../../contexts/UserContext";

export default function Login() {
  const [open, setOpen] = useState(false);
  const [name, setName] = useState("");
  const [password, setPassword] = useState("");
  const fetchData = useServerCall();
  const {
    setName: setUserName,
    setID,
    setIconFileName,
    setIconSASURL,
  } = React.useContext(UserContext);

  const handleLogin = React.useCallback(() => {
    // handle register logic here
    // Do Server api
    fetchData(
      "login",
      (json) => {
        const tempToken = json.session_token;
        sessionStorage.setItem("tempSessionToken", tempToken);
        setUserName(name);
        setID(json.user_data.id);
        setIconFileName(json.user_data.profile_icon);
        setIconSASURL(json.user_data.profile_icon_sas_url);
        setOpen(false);
      },
      { user_name: name, password: password },
    );
  }, [
    fetchData,
    name,
    password,
    setID,
    setIconFileName,
    setIconSASURL,
    setUserName,
  ]);

  const handleClick = (event) => {
    setOpen(true);
  };

  const handleNameChange = React.useCallback((e) => {
    if (e.target?.value !== undefined) {
      setName(e.target.value);
    }
  }, []);

  const handlePasswordChange = React.useCallback((e) => {
    if (e.target?.value !== undefined) {
      setPassword(e.target.value);
    }
  }, []);

  return (
    <div>
      <MenuItem onClick={handleClick} data-testid="login-menu-item">
        Login
      </MenuItem>
      <Dialog
        open={open}
        onClose={() => setOpen(false)}
        data-testid="login-dialogue"
      >
        <DialogTitle>Login</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            label="User Name"
            type="text"
            fullWidth
            value={name}
            onChange={handleNameChange}
            data-testid="login-name"
          />
          <TextField
            margin="dense"
            label="Password"
            type="password"
            fullWidth
            value={password}
            onChange={handlePasswordChange}
            data-testid="login-password"
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpen(false)}>Cancel</Button>
          <Button
            variant="contained"
            onClick={handleLogin}
            data-testid="login-submit"
          >
            Login
          </Button>
        </DialogActions>
      </Dialog>
    </div>
  );
}
