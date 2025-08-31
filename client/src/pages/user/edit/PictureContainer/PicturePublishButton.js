// PicturePublishButton.js
import React from "react";
import ButtonVS from "../../../components/TextButton";
import { useUserPictureEdit } from "../../../contexts/UserPictureEditContext";
import { useServerCall } from "../../../customHooks/useServerCall";

export default function PicturePublishButton() {
  const { fileBytes, fileName, remove } = useUserPictureEdit();
  const fetchData = useServerCall();

  const onPublish = () => {
    if (remove) {
      fetchData("remove-profile-pic", console.log);
    } else {
      fetchData(
        "upload-profile-pic",
        console.log,
        { file_name: fileName, byte_stream: fileBytes }
      );
    }
  };

  return <ButtonVS text="Publish" handleClick={onPublish} />;
}
