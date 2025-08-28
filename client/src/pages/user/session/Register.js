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

export default function Register() {
    const [open, setOpen] = useState(false);
    const [name, setName] = useState(false);
    const [email, setEmail] = useState(false);
    const [password, setPassword] = useState(false);
    const fetchData = useServerCall();
    const { setName: setUserName } = React.useContext(UserContext);

  const handleClick = React.useCallback((event) => {
    setOpen(true)
  }, []);

  const handleRegister = React.useCallback(() => {
    // handle register logic here
    // Do Server api
    fetchData("register", (json) => {
        const tempToken = json.session_token
        sessionStorage.setItem("tempSessionToken", tempToken);
        setUserName(name)
        setOpen(false);
    }, { user_name: name, email: email, password: password });
  }, [fetchData, name, email, password, setUserName]);

  const handleNameChange = React.useCallback((e) => {
    if (e.target?.value !== undefined) {
        setName(e.target.value)
    }
  }, [])

  const handleEmailChange = React.useCallback((e) => {
    if (e.target?.value !== undefined) {
        setEmail(e.target.value)
    }
  }, [])

  const handlePasswordChange = React.useCallback((e) => {
    if (e.target?.value !== undefined) {
        setPassword(e.target.value)
    }
  }, [])

  return (
    <div>
        <MenuItem onClick={handleClick}>Register</MenuItem>
        <Dialog open={open} onClose={() => setOpen(false)}>
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
          <TextField
            margin="dense"
            label="Password"
            type="password"
            fullWidth
            value={password}
            onChange={handlePasswordChange}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpen(false)}>Cancel</Button>
          <Button variant="contained" onClick={handleRegister}>
            Register
          </Button>
        </DialogActions>
      </Dialog>
    </div>
  );
}
