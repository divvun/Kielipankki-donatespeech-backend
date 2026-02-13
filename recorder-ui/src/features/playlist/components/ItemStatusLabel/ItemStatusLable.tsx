import React from "react";
import "./ItemStatusLabel.css";
import { DisplayedElement } from "../../types";

type ItemStatusLabelProps = {
  recordingItemProgress?: {
    itemNumber: number;
    totalCount: number;
  } | null;
    displayedElement: DisplayedElement;
    lang: string;
};

interface Langstrings { [key: string]: string; }
interface Langs { [key: string]: Langstrings; }

const fi_strings: Langstrings = {
    'help-research': "Auta tutkijaa",
    'watch-or-listen': "Katso tai kuuntele"
}

const en_strings: Langstrings = {
    'help-research': "Help the developers",
    'watch-or-listen': "Watch or listen"
}

const sv_strings: Langstrings = {
    'help-research': "Hjälp forskaren",
    'watch-or-listen': "Titta eller lyssna"
}

const langs: Langs = {
    "fi": fi_strings,
    "en": en_strings,
    "sv": sv_strings,
}

const NON_BRAKING_SPACE = "\u00A0";

const ItemStatusLabel: React.FC<ItemStatusLabelProps> = ({
  recordingItemProgress,
    displayedElement,
    lang,
}) => {
  const getText = () => {
    const { item } = displayedElement;
      if (!item) return null;
      var DONATE = lang !== "sv" ? "Lahjoita": "Donera";

    const isPrompt = item.kind === "prompt";
    if (isPrompt) {
      if (item.metaTitle !== null) {
        return item.metaTitle;
      }
      else {
        return langs[lang]['help-research'];
      }
    }

    if (item.isRecording && recordingItemProgress)
      return `${DONATE} ${recordingItemProgress.itemNumber}/${recordingItemProgress.totalCount}`;

    const isMedia = item.itemType !== "text";
    if (item.metaTitle !== null) {
      return item.metaTitle;
    }
    if (isMedia) {
      return langs[lang]['watch-or-listen'];
    }

    return null;
  };
  const text = getText() || NON_BRAKING_SPACE;
  return <h6 className="item-status-label">{text}</h6>;
};

export default ItemStatusLabel;
