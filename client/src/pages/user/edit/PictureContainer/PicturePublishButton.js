// PicturePublishButton.js
import React from "react";

import { UserContext } from "../../../../contexts/UserContext";
import ButtonVS from "../../../../components/TextButton";
import { useUserPictureEdit } from "./UserPictureEditContext";
import { useServerCall } from "../../../../customHooks/useServerCall";

export default function PicturePublishButton() {
  const { fileBytes, fileName, remove } = useUserPictureEdit();
  const { setIconFileName, setIconSASURL } = React.useContext(UserContext)
  const fetchData = useServerCall();

  const onPublish = () => {
    if (remove) {
      fetchData("remove-profile-pic", console.log);
    } else {
      fetchData(
        "upload-profile-pic",
        (json) => {
            setIconFileName(json?.pic_data?.profile_icon)
            setIconSASURL(json?.pic_data?.profile_icon_sas_url)
        },
        { file_name: fileName, byte_stream: fileBytes }
      );
    }
  };

  return <ButtonVS text="Publish" handleClick={onPublish} />;
}
