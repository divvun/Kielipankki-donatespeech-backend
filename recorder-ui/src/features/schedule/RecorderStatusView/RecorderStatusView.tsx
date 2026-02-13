import React, { useEffect } from "react";
import "./RecorderStatusView.css";
import { RecorderStatus } from "../../../utils/AudioRecorder";
import { useAudioRecorderContext } from "../../../utils/AudioRecorderContext";
import AppIcons from "../../components/AppIcons/AppIcons";
import PlaylistButton from "../../playlist/components/PlaylistButton/PlaylistButton";

type RecorderStatusViewProps = {
    onQuit: () => void,
    lang: string
};

interface Langstrings { [key: string]: string; }
interface Langs { [key: string]: Langstrings; }

const fi_strings: Langstrings = {
    "waiting-for-access-title": "Anna selaimellesi lupa mikrofonin käyttöön",
    "access-denied-title": "Lupaa mikrofonin käyttöön ei annettu",
    "not-supported-title": "Palvelu ei toimi selaimellasi",
    "access-denied-body-1": "Jotta puheen lahjoittaminen onnistuu, sinun pitää antaa selaimellesi lupa käyttää mikrofonia äänityksen ajan. Kameraa palvelu ei käytä. Ainoastaan ääntä tallennetaan.",
    "access-denied-body-2": "Lahjoitettu puhe käsitellään luottamuksellisesti ja sen turvallisesta säilömisestä vastaa yliopistojen Kielipankki.",
    "not-supported-body-1": "Puheen lahjoittaminen selaimella onnistuu parhaiten käyttäen uusinta versiota Chromesta tai Firefoxista.",
    "not-supported-body-2": "Voit myös ladata Lahjoita Puhetta -sovelluksen:",
    "return": "Palaa etusivulle"
}

const en_strings: Langstrings = {
    "waiting-for-access-title": "Give your browser permission to use the microphone",
    "access-denied-title": "Access to use microphone denied",
    "not-supported-title": "You browser doesn't support this service",
    "access-denied-body-1": "Jotta puheen lahjoittaminen onnistuu, sinun pitää antaa selaimellesi lupa käyttää mikrofonia äänityksen ajan. Kameraa palvelu ei käytä. Ainoastaan ääntä tallennetaan.",
    "access-denied-body-2": "Lahjoitettu puhe käsitellään luottamuksellisesti ja sen turvallisesta säilömisestä vastaa yliopistojen Kielipankki.",
    "not-supported-body-1": "Puheen lahjoittaminen selaimella onnistuu parhaiten käyttäen uusinta versiota Chromesta tai Firefoxista.",
    "not-supported-body-2": "",
    "return": "Palaa etusivulle"
}

const sv_strings: Langstrings = {
    "waiting-for-access-title": "Ge din webbläsare rätt att använda mikrofonen",
    "access-denied-title": "Du lät inte webbläsaren använda din mikrofon",
    "not-supported-title": "Tjänsten fungerar inte i din webbläsare",
    "access-denied-body-1": "För att kunna donera prat måste du tillåta att din webbläsare använder mikrofonen under inbandningen. Din kamera används inte.",
    "access-denied-body-2": "Pratet du donerar hanteras med respekt för dina rättigheter och universitetens språkbank lagrar materialet på ett säkert sätt.",
    "not-supported-body-1": "Det är enklast att donera prat genom att använda den nyaste versionen av Chrome eller Firefox.",
    "not-supported-body-2": "",
    "return": "Gå tillbaka till startsidan"
}

const langs: Langs = {
    "fi": fi_strings,
    "en": en_strings,
    "sv": sv_strings,
}

const getTitle = (status: RecorderStatus, lang: string) => {
  switch (status) {
    case "NotInitialized":
    case "WaitingForAccess":
	  return langs[lang]["waiting-for-access-title"];
    case "AccessDenied":
	  return langs[lang]["access-denied-title"];
    case "NotSupported":
	  return langs[lang]["not-supported-title"];
    default:
      return "";
  }
};

const getBodys = (status: RecorderStatus, lang: string) => {
  switch (status) {
    case "NotInitialized":
    case "WaitingForAccess":
    case "AccessDenied":
	  return [langs[lang]['access-denied-body-1'], langs[lang]['access-denied-body-2']];
    case "NotSupported":
	  return [langs[lang]['not-supported-body-1'], langs[lang]['not-supported-body-2']];
    default:
      return [];
  }
};

const RecorderStatusView: React.FC<RecorderStatusViewProps> = ({ onQuit, lang }) => {
  const recorder = useAudioRecorderContext();

  useEffect(() => recorder?.initialize(), [recorder]);

  if (!recorder || recorder.status === "NotInitialized") return null;

  const status = recorder.status;
  const getFooter = () => {
    switch (status) {
      case "NotSupported":
        return (
          <>
            <AppIcons />
            <PlaylistButton
              className="my-4"
            text={langs[lang]["return"]}
              onClick={onQuit}
            />
          </>
        );
      default:
        return null;
    }
  };

    const bodys = getBodys(status, lang);
  return (
    <div className="recorder-status-view">
	  <h3>{getTitle(status, lang)}</h3>
      {bodys.map(b => (
        <p key={b}>{b}</p>
      ))}
      <div>{getFooter()}</div>
    </div>
  );
};

export default RecorderStatusView;
