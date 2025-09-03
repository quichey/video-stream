import React from "react";
import { Popover, MenuItem, Typography } from "@mui/material";

import Login from "./Login";
import Logout from "./Logout";
import Register from "./Register";

import { UserContext } from "../../../contexts/UserContext";
import ViewChannel from "./ViewChannel";

export default function SessionMenu({ handleClose, anchorEl }) {
    const { name, id: userID } = React.useContext(UserContext);
    const [mounted, setMounted] = React.useState(false);

    React.useEffect(() => {
      setMounted(true);
    }, []);

  const open = Boolean(anchorEl);
  const id = open ? "simple-popover" : undefined;

  return (
    <div>

      <Popover
        id={id}
        open={open}
        anchorEl={anchorEl}
        onClose={handleClose}
        anchorOrigin={{
          vertical: "bottom",
          horizontal: "left",
        }}
        transformOrigin={{
          vertical: "top",
          horizontal: "left",
        }}
      >
        {
          mounted && (
            <>
              <Typography>
                  {name}
              </Typography>
              <ViewChannel />
              {!userID && <Login />}
              <MenuItem onClick={handleClose}>Settings</MenuItem>
              {!!userID && <Logout />}
              {!userID && <Register />}
            </>
          )
        }
      </Popover>
    </div>
  );
}
