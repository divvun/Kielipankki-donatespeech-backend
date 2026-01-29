import React from "react";
import {
  FacebookShareButton,
  FacebookIcon,
  TwitterShareButton,
  TwitterIcon,
} from "react-share";
import { useSelector } from "react-redux";
import { selectTotalRecordingDuration } from "../../../playlistSlice";
import config from "../../../../../config/config";

import "./InviteFriend.css";

type InviteFriendProps = {
  className?: string;
};

const InviteFriend: React.FC<InviteFriendProps> = ({ className }) => {
  const totalRecDurationSeconds = useSelector(selectTotalRecordingDuration);
  const minutes = Math.floor(totalRecDurationSeconds / 60);
  const startText =
    minutes >= 2
      ? `I donated my speech for ${minutes} minutes.`
      : "I just donated my speech.";
  const twitterQuote = `${startText} It helps us build AI and speech recognition that understand Finnish better. Donate too and help make everyday life more fluent!`;
  const fbQuote = twitterQuote + ` ${config.WEBSITE_URL}`;
  return (
    <div className={`invite-friend ${className}`}>
      <FacebookShareButton
        className="mr-4"
        url={config.WEBSITE_URL}
        quote={fbQuote}
      >
        <FacebookIcon size={48}></FacebookIcon>
      </FacebookShareButton>
      <TwitterShareButton title={twitterQuote} url={config.WEBSITE_URL}>
        <TwitterIcon size={48}></TwitterIcon>
      </TwitterShareButton>
    </div>
  );
};

export default InviteFriend;
