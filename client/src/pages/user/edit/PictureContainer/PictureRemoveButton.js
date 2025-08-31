// PictureRemoveButton.js
import React from "react";
import ButtonVS from "../../../components/TextButton";
import { useUserPictureEdit } from "../../../contexts/UserPictureEditContext";

export default function PictureRemoveButton() {
  const { setRemove } = useUserPictureEdit();
  return <ButtonVS text="Remove" handleClick={() => setRemove(true)} />;
}
