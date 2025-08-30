import React from "react";
import { MenuItem, Typography } from "@mui/material";
import { NavLink } from "react-router";

import { UserContext } from "../../../contexts/UserContext";

export default function ViewChannel() {
    const { id } = React.useContext(UserContext);

    const handleClick = React.useCallback((event) => {
        console.log("do navlink to user's channel page " + id)
    }, [id]);


    return (
        <div>
            <MenuItem>
                <NavLink to={`/channel/${id}`} end>
                    <Typography onClick={handleClick}>View Channel</Typography>
                </NavLink>
            </MenuItem>
        </div>
    );
}
