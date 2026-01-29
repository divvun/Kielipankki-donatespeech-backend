import React from "react";
import { useDispatch } from "react-redux";
import { Link } from "react-router-dom";
import PlaylistButton from "../../playlist/components/PlaylistButton/PlaylistButton";
import { termsAndConditionAccepted } from "../../user/userSlice";

import "./TermsAndConditionsView.css";
import routes from "../../../config/routes";

const CAMPAIGN_URL = "https://example.com";
const KIELIPANKKI_URL = "https://www.kielipankki.fi";
const EMAIL_ADDRESS = "your-feedback-email-here";

const largerBodyTextStyle = {
  fontSize: "larger",
};

type TermsAndConditionsViewProps = {};

const TermsAndConditionsView: React.FC<TermsAndConditionsViewProps> = () => {
  const dispatch = useDispatch();
  return (
    <div className="terms-and-conditions-view">
      <h4>Thanks for joining us!</h4>
      <p>
        <strong style={largerBodyTextStyle}>
          This page contains basic information about the project. After reading
          it, you can start donating at the bottom of the page.
        </strong>
      </p>
      <h4>What?</h4>
      <p>
        Vestibulum lorem turpis, lacinia sed blandit nec, viverra et ligula. In
        vestibulum dui eu pretium vestibulum.
      </p>
      <p>
        Aliquam dictum egestas vehicula. Suspendisse potenti. Fusce ut tristique
        mi. Donec dictum leo at metus lobortis imperdiet. Donec pellentesque
        laoreet ultrices. Mauris tincidunt nunc pretium nunc placerat congue.
      </p>
      <p>
        More information about the campaign can be found
        {"  "}
        <Link to={routes.INFO}>here</Link>
        {". "}
      </p>
      <h4>Who?</h4>
      <p>
        Pellentesque efficitur efficitur blandit. Sed iaculis enim neque, cursus
        mollis sapien venenatis sit amet. In aliquet ligula ac nisi porttitor
        ornare. Nullam sit amet odio nec ex semper tempus quis eu erat. Donec
        nec elit nec neque feugiat convallis. Maecenas rhoncus urna nec libero
        fringilla, nec auctor nisi consectetur.
      </p>
      <h4>How is personal data handled?</h4>
      <p>
        Donated speech and other related information contain personal data about
        the speaker. We process this data in accordance with Finnish data
        protection legislation. More information about the processing of
        personal data can be found
        {"  "}
        <Link to={routes.PRIVACY}>here</Link>
        {". "}
      </p>
      <h4>Rights to the speech</h4>
      <p>You may have copyright or other rights to the speech you donate.</p>
      <p>
        You grant these rights to the University of Helsinki to the extent
        necessary and legally possible for the development and research of
        speech-understanding or speech-producing AI, linguistic research, or
        related higher education. The University of Helsinki may further
        transfer these rights.
      </p>
      <p>
        Please do not use text written by others in your speech, such as poems,
        lines from plays, or excerpts, and do not disclose private, sensitive,
        or confidential information about yourself or others.
      </p>
      <h4>More information</h4>
      <p>
        Campaign website:
        {"  "}
        <a href={CAMPAIGN_URL}>(hankkeen nimi)</a>
        <br />
        Helsingin yliopisto, Kielipankki,
        {"  "}
        <a target="_blank" rel="noopener noreferrer" href={KIELIPANKKI_URL}>
          {KIELIPANKKI_URL}
        </a>
        {", "}
        <a href={`mailto: ${EMAIL_ADDRESS}`}>{EMAIL_ADDRESS}</a>
      </p>
      <div className="terms-and-conditions-footer">
        <p>
          By clicking the I accept button below, I accept the above terms for
          donating speech. If I am under 18, my guardian accepts the terms on my
          behalf.
        </p>
        <PlaylistButton
          text="I accept"
          onClick={() => dispatch(termsAndConditionAccepted())}
        />
      </div>
    </div>
  );
};

export default TermsAndConditionsView;
