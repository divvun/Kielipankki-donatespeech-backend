import React from "react";
import "./PrivacyPage.css";
import { useSelector, useDispatch } from "react-redux";
import { Link } from "react-router-dom";
import { selectClientId, userStateReset } from "../user/userSlice";
import PlaylistButton from "../playlist/components/PlaylistButton/PlaylistButton";
import { playlistStateReset } from "../playlist/playlistSlice";

import balanceTest from "./tasapainotesti.pdf";
import routes from "../../config/routes";

type PrivacyPageProps = {};

const EMAIL_ADDRESS = "<your-feedback-email-here>";

const PrivacyPage: React.FC<PrivacyPageProps> = () => {
  const clientId = useSelector(selectClientId);
  const dispatch = useDispatch();

  const clearUserData = () => {
    dispatch(userStateReset());
    dispatch(playlistStateReset());
  };

  return (
    <div className="privacy-page frame--view">
      <h2>Privacy</h2>
      <p className="mb-4">
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent
        ultricies erat at dolor scelerisque euismod vel vitae eros. Maecenas a
        convallis eros, vel aliquet ipsum. Ut ac ipsum velit. Sed viverra
        faucibus justo ut rutrum. Phasellus pellentesque volutpat tincidunt.
        Donec hendrerit mauris ut sapien feugiat scelerisque. Suspendisse varius
        quam non vulputate ullamcorper. Pellentesque auctor justo nec dui
        placerat pretium. In ut felis gravida, commodo urna vitae, volutpat
        quam. Aenean et arcu turpis. Sed leo lorem, mattis eget neque et,
        blandit semper dui. Vestibulum id accumsan turpis, et blandit metus.
      </p>
      <p className="mb-4">
        Morbi vehicula magna sapien, id ornare risus condimentum sed. Nullam
        mollis finibus mi, et accumsan sapien tincidunt vitae. Ut finibus urna
        quis tristique viverra. Quisque fermentum mauris at nisi tincidunt, non
        lacinia arcu congue. Ut faucibus quis tortor vitae rutrum. Praesent
        faucibus massa ante, quis consequat ante sodales sit amet. Sed molestie
        quam at laoreet interdum.
      </p>
      <p className="mb-4">
        Vestibulum rhoncus tincidunt dui et faucibus. Praesent mattis rhoncus
        congue. Suspendisse sit amet mi turpis. Etiam nec dapibus metus. Proin
        faucibus ac lorem in facilisis. Proin non fringilla nulla. Quisque quis
        sollicitudin ex. Mauris non felis et lorem euismod auctor. Ut ac turpis
        a felis posuere venenatis. Nunc consequat dui malesuada est vulputate,
        fringilla mattis nunc maximus.
      </p>

      <h4>Deleting your donated speech</h4>
      <p className="mb-4">
        You can remove your donation from the database by contacting
        {"  "}
        <a href={`mailto: ${EMAIL_ADDRESS}`}>{EMAIL_ADDRESS}</a>
        {"  "}
        and telling them your identifier and your wish to remove your donation
        from the database.
      </p>
      <p>Save your browser-specific identifier:</p>
      <p className="mb-4">
        <strong>{clientId}</strong>
      </p>

      <h4>Removing donation-related data from your browser</h4>
      <p className="mb-4">
        If you are using a shared computer (for example, in a library) or you
        otherwise want this browser to forget the amount of speech you donated
        and the choices you made, you can clear the data by pressing the “Clear
        data” button. Your browser-specific identifier will also change, so
        please save your current identifier before clearing the data.
      </p>
      <PlaylistButton
        className="mb-4"
        buttonType="outline"
        text="Clear data"
        onClick={clearUserData}
      />

      <h3 className="mt-5">Information about processing personal data</h3>
      <p className="mb-4">
        Duis pharetra, magna et porttitor lobortis, mi libero hendrerit orci, ac
        condimentum ante purus et est. Suspendisse non accumsan dolor. Phasellus
        auctor dapibus quam, vehicula ultrices urna tristique quis. Vivamus diam
        nisi, posuere vel ex at, luctus malesuada sapien. Praesent quis lorem
        quis nibh facilisis sollicitudin. Nam sit amet accumsan purus.
      </p>
      <p className="mb-4">
        Nullam pharetra tincidunt ante, id feugiat dolor tincidunt nec. Donec
        libero quam, porttitor vitae tellus eu, egestas luctus nunc. Duis
        posuere felis non semper aliquet. Nam in consectetur nisl, id fringilla
        nisi. Nulla orci ex, ultrices porttitor lacus ut, commodo dapibus diam.
        Nam volutpat imperdiet mauris. Sed elementum arcu nec pellentesque
        laoreet.
      </p>

      <h4>Data controllers</h4>
      <p className="mb-4">
        Nam egestas erat lorem, egestas dignissim velit tincidunt eget.
      </p>

      <h5>Data controllers’ contact details</h5>
      <p className="mb-4">
        If you have questions about the processing of personal data or want to
        exercise your data subject rights, please contact
        {"  "}
        <a href="mailto:<your-feedback-email-here>">your-feedback-email-here</a>
        .
      </p>

      <p>Data controllers’ data protection contact details:</p>

      <ul className="mb-4">
        <li>
          University of Helsinki (Data Protection Officer):
          {"  "}
          <a href="mailto:tietosuoja@helsinki.fi">tietosuoja@helsinki.fi</a>
        </li>
      </ul>

      <h5>Data controllers’ responsibilities in processing personal data</h5>

      <p className="mb-4">
        Mauris aliquet, magna et imperdiet finibus, nisi urna auctor ligula, non
        euismod sapien quam in quam. Sed dictum, magna id viverra ultricies,
        lorem leo tincidunt eros, eget convallis quam est at nisl. Aenean ac
        rhoncus massa. Ut massa nunc, dignissim in luctus eget, aliquet vitae
        eros. Sed consectetur, erat ac laoreet aliquam, erat ligula lobortis
        libero, et tincidunt felis ante sit amet felis.
      </p>

      <p className="mb-4">
        Vestibulum rhoncus tincidunt dui et faucibus. Praesent mattis rhoncus
        congue. Suspendisse sit amet mi turpis. Etiam nec dapibus metus. Proin
        faucibus ac lorem in facilisis. Proin non fringilla nulla. Quisque quis
        sollicitudin ex. Mauris non felis et lorem euismod auctor. Ut ac turpis
        a felis posuere venenatis. Nunc consequat dui malesuada est vulputate,
        fringilla mattis nunc maximus.
      </p>

      <h6>Data stored in the Language Bank</h6>

      <p className="mb-4">
        The speech data produced by the campaign is stored in the University of
        Helsinki Language Bank, from which the data may be disclosed to
        companies and other organizations for AI research and development,
        language research, or related higher-education teaching. The University
        of Helsinki is the data controller responsible for storing and
        processing the data in the Language Bank. In the future, the University
        of Helsinki may also transfer the speech data in full to another
        organization, which then becomes a data controller and may also sell
        usage rights to the data for the development of speech-understanding and
        speech-generating applications and services.
      </p>

      <h6>Use of the data in AI development and language research</h6>

      <p className="mb-4">
        The speech data collected in the “Project name” campaign may be used for
        AI development and research and for language research by commercial
        companies and AI developers as well as researchers, universities, and
        research institutes conducting scientific research. In addition,
        universities may use the speech data for teaching related to these
        purposes. These companies or other organizations are data controllers
        responsible for their own AI development, research, or teaching.
        Information about which recipients the speech data has been disclosed to
        and how they process the data will be available at
        {"  "}
        <a
          href="https://www.kielipankki.fi/hankkeen-nimi/"
          target="_blank"
          rel="noopener noreferrer"
        >
          https://www.kielipankki.fi/hankkeen-nimi/
        </a>
        .
      </p>

      <h4>Why are personal data processed?</h4>
      <p className="mb-4">
        Duis pharetra, magna et porttitor lobortis, mi libero hendrerit orci, ac
        condimentum ante purus et est. Suspendisse non accumsan dolor. Phasellus
        auctor dapibus quam, vehicula ultrices urna tristique quis. Vivamus diam
        nisi, posuere vel ex at, luctus malesuada sapien. Praesent quis lorem
        quis nibh facilisis sollicitudin. Nam sit amet accumsan purus.
      </p>

      <h4>What personal data are processed?</h4>
      <p className="mb-4">
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent
        ultricies erat at dolor scelerisque euismod vel vitae eros. Maecenas a
        convallis eros, vel aliquet ipsum. Ut ac ipsum velit. Sed viverra
        faucibus justo ut rutrum. Phasellus pellentesque volutpat tincidunt.
        Donec hendrerit mauris ut sapien feugiat scelerisque.
      </p>

      <h4>What is the legal basis for processing?</h4>
      <p className="mb-4">
        Suspendisse varius quam non vulputate ullamcorper. Pellentesque auctor
        justo nec dui placerat pretium. In ut felis gravida, commodo urna vitae,
        volutpat quam. Aenean et arcu turpis. Sed leo lorem, mattis eget neque
        et, blandit semper dui. Vestibulum id accumsan turpis, et blandit metus.
      </p>

      <p>
        We have carefully assessed, through a balancing test, that we can use
        legitimate interest as the basis for processing personal data.
        Information about the balancing test and its considerations can be found
        {"  "}
        <a href={balanceTest} target="_blank" rel="noopener noreferrer">
          here
        </a>
        {". "}
      </p>

      <h4>
        Who are the recipients or categories of recipients of personal data?
      </h4>
      <p className="mb-4">
        Fusce vitae ante eget erat mattis sodales. Pellentesque auctor gravida
        tellus, eget convallis orci venenatis vitae. Fusce elementum sit amet
        turpis non aliquam.
      </p>

      <h4>Will data be transferred outside the EU?</h4>
      <p className="mb-4">
        Duis ut aliquet purus. Aenean interdum condimentum molestie. Aenean
        porta sed odio at laoreet. In sit amet dui eu libero dignissim
        fermentum. In posuere nisl arcu, quis mollis sapien fermentum sit amet.
        Cras ut consequat turpis. Duis gravida aliquam maximus.
      </p>

      <h4>
        How long will data be stored, or what criteria determine the retention
        period?
      </h4>
      <p className="mb-4">
        Phasellus orci ipsum, congue at nisi vel, interdum fringilla nisi. Duis
        venenatis tellus mi, eu aliquam dolor rhoncus a. Morbi vel massa ex.
        Morbi eu iaculis justo. Vestibulum facilisis imperdiet leo quis
        pulvinar.
      </p>

      <h4>Your rights</h4>
      <p className="mb-4">
        To exercise the rights described below, you must be able to provide your
        identifier with the request or otherwise sufficiently specify which data
        is concerned. Please store the identifier carefully.
      </p>

      <h5>Right to information and access to data</h5>
      <p className="mb-4">
        You have the right to know whether we process your personal data. If we
        do, you have the right to know what data we process.
      </p>

      <h5>Right to request rectification and erasure</h5>
      <p className="mb-4">
        You have the right to request correction of inaccurate data by
        contacting us.
      </p>

      <p className="mb-4">
        You can ask us to delete your personal data from our systems. We will
        carry out the requested actions unless we have a legitimate reason not
        to delete the data. The data may not be removed immediately from all
        backup or other similar systems.
      </p>

      <h5>Direct marketing and automated decision-making</h5>
      <p className="mb-4">
        Nam in leo odio. Maecenas eros metus, semper ut mi molestie, lobortis
        suscipit est. Vivamus tortor dolor, condimentum non velit vitae,
        suscipit egestas purus. Aenean non semper dolor.
      </p>

      <h5>Right to restrict processing</h5>
      <p className="mb-4">
        You can ask us to restrict the processing of certain personal data. A
        request to restrict processing may lead to more limited opportunities to
        use your donated speech in AI development.
      </p>

      <h5>Right to object to processing</h5>
      <p className="mb-4">
        On grounds relating to your particular situation, you can object to the
        processing of your personal data, meaning you can request that the data
        not be processed at all. In that case we will stop processing your data
        unless we can demonstrate compelling legitimate grounds that override
        your interests, rights, and freedoms, or the processing is necessary for
        the establishment, exercise, or defense of legal claims.
      </p>

      <h5>Right to lodge a complaint with a supervisory authority</h5>
      <p className="mb-4">
        You have the right to lodge a complaint with the Data Protection
        Ombudsman if you believe that the processing of your personal data
        violates the law. More information about the right to complain
        {": "}
        <a
          href="https://tietosuoja.fi/onko-tietosuojaoikeuksiasi-loukattu"
          target="_blank"
          rel="noopener noreferrer"
        >
          https://tietosuoja.fi/onko-tietosuojaoikeuksiasi-loukattu
        </a>
      </p>
    </div>
  );
};

export default PrivacyPage;
