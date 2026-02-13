import React from "react";
import "./ScheduleView.css";
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Frame from "../components/Frame";
import TotalRecordingDuration from "../playlist/components/TotalRecordingDuration/TotalRecordingDuration";
import { useHistory } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { schedulePlaylistReset } from "../playlist/playlistSlice";
import { useAudioRecorderContext } from "../../utils/AudioRecorderContext";
import Playlist from "../playlist/components/Playlist/Playlist";
import RecorderStatusView from "./RecorderStatusView/RecorderStatusView";
import { selectIsTermsAndConditionAccepted } from "../user/userSlice";
import TermsAndConditionsView from "./TermsAndConditionsView/TermsAndConditionsView";

import "./ScheduleView.css";

type ScheduleViewProps = {
    onRecorderResetRequested: () => void,
    lang: string
};

interface Langstrings { [key: string]: string; }
interface Langs { [key: string]: Langstrings; }

const fi_strings: Langstrings = {
    "donation-tally": "Olet lahjoittanut:",
    "exit": "Poistu"
}

const en_strings: Langstrings = {
    "donation-tally": "You have donated:",
    "exit": "Exit"
}

const sv_strings: Langstrings = {
    "donation-tally": "Du har donerat:",
    "exit": "Avsluta"
}

const langs: Langs = {
    "fi": fi_strings,
    "en": en_strings,
    "sv": sv_strings,
}

const ScheduleView: React.FC<ScheduleViewProps> = ({
    onRecorderResetRequested, lang,
}) => {
    var s = langs[lang];
  const recorder = useAudioRecorderContext();
  const history = useHistory();
  const isTermsAndConditionAccepted = useSelector(
    selectIsTermsAndConditionAccepted
  );
  const dispatch = useDispatch();

  if (!recorder) return null;

  const handleQuit = () => {
    dispatch(schedulePlaylistReset());
    history.push("/");
  };

  const showPlaylist = isTermsAndConditionAccepted && recorder.isInitialized;

  const renderContent = () => {
    if (showPlaylist) {
      return (
        <Col className="mx-auto h-100">
          <Playlist
            onQuit={handleQuit}
          onRecorderResetRequested={onRecorderResetRequested}
	  lang={lang}
          />
        </Col>
      );
    }

    if (!isTermsAndConditionAccepted) {
      return (
        <Col>
              <TermsAndConditionsView lang={lang}/>
        </Col>
      );
    }

    return (
      <Col>
            <RecorderStatusView onQuit={handleQuit} lang={lang}/>
      </Col>
    );
  };

  const schedulePlaylistClass = showPlaylist ? "schedule-view--playlist" : "";

  return (
    <Container fluid>
      <Row className={`schedule-view ${schedulePlaylistClass}`}>
        <Col className="schdule-view-col h-100 d-flex flex-column" xs={12}>
          <Frame className="schedule-view-frame">
            <Row className="schedule-view-header align-items-start">
              <Col>
                <Row className="align-items-center">
                  <Col xs={4}>
                    <button tabIndex={0}
                      className="schedule-view-header--quit float-left"
                      onClick={handleQuit}
      aria-label={s["exit"]}
                    >
                      <b>X</b>
          <span> {s["exit"]}</span>
                    </button>
                  </Col>
                  <Col>
                    <div className="float-right">
          <TotalRecordingDuration label={s["donation-tally"]} />
                    </div>
                  </Col>
                </Row>
              </Col>
            </Row>
            <Row className="schedule-view-content align-items-center">
              {renderContent()}
            </Row>
          </Frame>
        </Col>
      </Row>
    </Container>
  );
};

export default ScheduleView;
