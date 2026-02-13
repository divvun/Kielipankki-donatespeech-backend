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
    lang: string;
};

interface Langstrings { [key: string]: string; }
interface Langs { [key: string]: Langstrings; }

const fi_strings: Langstrings = {
}

const en_strings: Langstrings = {
}

const sv_strings: Langstrings = {
     
}

const langs: Langs = {
    "fi": fi_strings,
    "en": en_strings,
    "sv": sv_strings,
}

const InviteFriend: React.FC<InviteFriendProps> = ({ className, lang }) => {
  const totalRecDurationSeconds = useSelector(selectTotalRecordingDuration);
    const minutes = Math.floor(totalRecDurationSeconds / 60);
    const this_url = lang !== "sv" ? config.WEBSITE_URL : "https://doneraprat.fi";
    const fi_startText = minutes >= 2
	? `Lahjoitin puhettani ${minutes} minuuttia.`
	: "Lahjoitin juuri puhettani.";

    const startText = lang !== "sv" ? fi_startText : "Jag har donerat mitt prat!";
    const twitterQuote = lang !== "sv" ?
	`${startText} Sen avulla saamme tekoälyn ja puheentunnistuksen, joka ymmärtää paremmin suomea. Lahjoita sinäkin ja puhu meille sujuvampi arki! #lahjoitapuhetta` :
	`${startText} Du kan också donera – tillsammans är vi med och utvecklar röststyrning på finlandssvenska! #doneraprat`;
    const fbQuote = twitterQuote + ` ${this_url}`;
  return (
    <div className={`invite-friend ${className}`}>
      <FacebookShareButton
        className="mr-4"
        url={config.WEBSITE_URL}
        quote={fbQuote}
      >
        <FacebookIcon size={48}></FacebookIcon>
      </FacebookShareButton>
      <TwitterShareButton title={twitterQuote} url={this_url}>
        <TwitterIcon size={48}></TwitterIcon>
      </TwitterShareButton>
    </div>
  );
};

export default InviteFriend;
