import React from "react";
import { NavLink } from "react-router";

import ButtonVS from "../../../components/TextButton";

import { UserContext } from "../../../contexts/UserContext";

function CustomizeChannelButton() {
  const { id } = React.useContext(UserContext)

  return (
    <div>
        <NavLink to={`/channel/${id}/editing/profile`} end>
            <ButtonVS>
                Customize channel
            </ButtonVS>
        </NavLink>
    </ div>
  );
}

export default CustomizeChannelButton;
