import * as React from "react";

import { get_storage_url } from "../util/urls";

export default function UserIconImg({ id, userIcon, userIconURL, length="20px" }) {
  return (
    <img
        alt={userIcon}
        src={get_storage_url("images", id, userIcon, userIconURL)}
        width={length}
        height={length}
        style={{
            borderRadius: "50%",
            objectFit: "cover",
        }}
    />
  );
}
