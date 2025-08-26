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

export default function Login() {
    const [open, setOpen] = useState(false);

  const handleLogin = () => {
    // handle login logic here
    setOpen(false);
  };

  const handleRegister = () => {
    // open registration dialog or redirect
    console.log("Navigate to Register");
  };

  const handleClick = (event) => {
  };


  return (
    <div>
        <MenuItem onClick={handleClick}>Login</MenuItem>
        <Dialog open={open} onClose={() => setOpen(false)}>
        <DialogTitle>Login</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            label="Email"
            type="email"
            fullWidth
          />
          <TextField
            margin="dense"
            label="Password"
            type="password"
            fullWidth
          />
          <Typography variant="body2" mt={2}>
            Don't have an account?{" "}
            <Link component="button" onClick={handleRegister}>
              Register
            </Link>
          </Typography>
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
