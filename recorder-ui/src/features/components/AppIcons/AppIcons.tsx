import React from "react";
import appStoreIcon from "./App_Store_Badge_FI.svg";
import googlePlayIcon from "./Google_Play_Badge_FI.png";

import "./AppIcons.css";

const APP_STORE_LINK =
  "https://apps.apple.com/fi/app/lahjoita-puhetta/id1515534152?l=fi";
const GOOGLE_PLAY_LINK =
  "https://play.google.com/store/apps/details?id=fi.lahjoitapuhetta.recorder";

type AppIconsProps = {};

const AppIcons: React.FC<AppIconsProps> = () => {
  return (
    <div className="app-icons">
      <a
        className="app-store-icon"
        target="_blank"
        href={APP_STORE_LINK}
        rel="noopener noreferrer"
      >
        <img src={appStoreIcon} alt="Lataa App Storesta" />
      </a>
      <a
        className="google-play-icon"
        target="_blank"
        href={GOOGLE_PLAY_LINK}
        rel="noopener noreferrer"
      >
        <img src={googlePlayIcon} alt="Lataa Google Playsta" />
      </a>
    </div>
  );
};

export default AppIcons;
