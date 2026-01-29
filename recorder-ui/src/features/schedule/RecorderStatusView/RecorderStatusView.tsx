import React, { useEffect } from "react";
import "./RecorderStatusView.css";
import { RecorderStatus } from "../../../utils/AudioRecorder";
import { useAudioRecorderContext } from "../../../utils/AudioRecorderContext";
import AppIcons from "../../components/AppIcons/AppIcons";
import PlaylistButton from "../../playlist/components/PlaylistButton/PlaylistButton";

type RecorderStatusViewProps = {
  onQuit: () => void;
};

const getTitle = (status: RecorderStatus) => {
  switch (status) {
    case "NotInitialized":
    case "WaitingForAccess":
      return "Allow your browser to use the microphone";
    case "AccessDenied":
      return "Microphone permission was not granted";
    case "NotSupported":
      return "The service does not work in your browser";
    default:
      return "";
  }
};

const getBodys = (status: RecorderStatus) => {
  switch (status) {
    case "NotInitialized":
    case "WaitingForAccess":
    case "AccessDenied":
      return [
        "To donate speech, you need to allow your browser to use the microphone during recording. The service does not use the camera. Only audio is recorded.",
        "Donated speech is handled confidentially, and the universities' Language Bank is responsible for its secure storage.",
      ];
    case "NotSupported":
      return [
        "Donating speech in the browser works best with the latest version of Chrome or Firefox.",
        "You can also download the Project name app:",
      ];
    default:
      return [];
  }
};

const RecorderStatusView: React.FC<RecorderStatusViewProps> = ({ onQuit }) => {
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
              text="Back to home"
              onClick={onQuit}
            />
          </>
        );
      default:
        return null;
    }
  };

  const bodys = getBodys(status);
  return (
    <div className="recorder-status-view">
      <h3>{getTitle(status)}</h3>
      {bodys.map(b => (
        <p key={b}>{b}</p>
      ))}
      <div>{getFooter()}</div>
    </div>
  );
};

export default RecorderStatusView;
