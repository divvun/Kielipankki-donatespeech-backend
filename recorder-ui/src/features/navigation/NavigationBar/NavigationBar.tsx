import React from "react";
import { useDispatch } from "react-redux";
import { useLocation } from "react-router-dom";
import Navbar from "react-bootstrap/Navbar";
import NavItem from "react-bootstrap/NavItem";
import Nav from "react-bootstrap/Nav";
import NavigationItem from "../NavigationItem/NavigationItem";
import TotalRecordingDuration from "../../playlist/components/TotalRecordingDuration/TotalRecordingDuration";
import routes from "../../../config/routes";
import { setLangFi, setLangSv } from "../../user/userSlice";

import "./NavigationBar.css";

type NavigationBarProps = { lang: string };

interface Langstrings { [key: string]: string; }
interface Langs { [key: string]: Langstrings; }

const fi_strings: Langstrings = {
    "home": "Lahjoita puhetta",
    "partners": "Yhteistyökumppanit",
    "privacy": "Tietosuoja",
    "info": "Tietoa hankkeesta",
    "duration": "Olet lahjoittanut:",
    "campaign": "Kampanjasivulle",
}

const en_strings: Langstrings = {
    "home": "Donate speech",
    "partners": "Partners",
    "privacy": "Privacy policy",
    "info": "Info",
    "duration": "You've donated:",
    "campaign": "Main page",
}

const sv_strings: Langstrings = {
    "home": "Donera prat",
    "partners": "Samarbetspartner",
    "privacy": "Dataskydd",
    "info": "Om projektet",
    "duration": "Du har donerat:",
    "campaign": "Till kampanjsidan",
}

const langs: Langs = {
    "fi": fi_strings,
    "en": en_strings,
    "sv": sv_strings,
}

const NavigationBar: React.FC<NavigationBarProps> = ({lang}) => {
    const { pathname } = useLocation();
    const dispatch = useDispatch();
    const setLangFiAndReload = () => {
	dispatch(setLangFi());
	const url = new URL(window.location.href);
	if (url.searchParams.has('lang')) {
	    url.searchParams.set('lang', 'fi');
	    window.history.pushState({}, '', url.href);
	}
	setTimeout(function() {window.location.reload();}, 500);
    }
    const setLangSvAndReload = () => {
	dispatch(setLangSv());
	const url = new URL(window.location.href);
	if (url.searchParams.has('lang')) {
	    url.searchParams.set('lang', 'sv');
	    window.history.pushState({}, '', url.href);
	}
	setTimeout(function() {window.location.reload();}, 500);
    }

    const isFISelected = lang === "fi" ? "navbar-langchoice-selected" : "";
    const isSVSelected = lang === "sv" ? "navbar-langchoice-selected" : "";


  if (pathname && pathname.startsWith(routes.SCHEDULE)) {
    // Do not show navbar for playlist
    return null;
  }

    var s = langs[lang]
  return (
    <Navbar expand="lg">
      <Navbar.Toggle aria-controls="basic-navbar-nav" />
      <Navbar.Collapse id="basic-navbar-nav">
        <Nav>
          <NavItem>
            <NavigationItem
              isFirst={true}
      text={s["home"]}
              to={routes.HOME}
            />
          </NavItem>
          <NavItem>
          <NavigationItem text={s["partners"]} to={routes.PARTNERS} />
          </NavItem>
          <NavItem>
          <NavigationItem text={s["privacy"]} to={routes.PRIVACY} />
          </NavItem>
          <NavItem>
          <NavigationItem text={s["info"]} to={routes.INFO} />
          </NavItem>
          <Nav.Link
            target="_blank"
            rel="noopener noreferrer"
      href={lang !== "sv" ? "https://yle.fi/lahjoitapuhetta" : "https://svenska.yle.fi/doneraprat"}
          >
          {s["campaign"]}
      </Nav.Link>
	  <div className="navbar-langchoice-container">
	  <span className={`navbar-langchoice ${isFISelected}`} title="Lahjoita puhetta suomeksi" role="link" tabIndex={0} onClick={setLangFiAndReload}>FI</span> <span className="navbar-langchoice-divider">|</span> <span className={`navbar-langchoice ${isSVSelected}`} title="Donera prat på svenska" role="link" tabIndex={0} onClick={setLangSvAndReload}> SV </span>
	  </div>
        </Nav>
      </Navbar.Collapse>
      <div className="float-right mt-3">
          <TotalRecordingDuration label={s["duration"]} />
      </div>
    </Navbar>
  );
};

export default NavigationBar;

