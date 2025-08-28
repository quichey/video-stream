import React, { useState } from "react";
import { Popover, Button, MenuItem, Typography } from "@mui/material";
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Link,
} from "@mui/material";

import { useServerCall } from "../../../customHooks/useServerCall";

export default function Login() {
    const [open, setOpen] = useState(false);
    const [name, setName] = useState(false);
    const [password, setPassword] = useState(false);
    const fetchData = useServerCall();

    const handleLogin = React.useCallback(() => {
        // handle register logic here
        // Do Server api
        fetchData("login", (json) => {
            const tempToken = json.session_token
            sessionStorage.setItem("tempSessionToken", tempToken);
            setOpen(false);
        }, { user_name: name, password: password });
      }, [fetchData, name, password]);

    const handleClick = (event) => {
        setOpen(true)
    };
  
    const handleNameChange = React.useCallback((e) => {
        if (e.target?.value !== undefined) {
            setName(e.target.value)
        }
    }, [])

    const handlePasswordChange = React.useCallback((e) => {
        if (e.target?.value !== undefined) {
            setPassword(e.target.value)
        }
    }, [])


    return (
    <div>
        <MenuItem onClick={handleClick}>Login</MenuItem>
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
          <Button variant="contained" onClick={handleLogin}>
            Login
          </Button>
        </DialogActions>
      </Dialog>
    </div>
    );
}
