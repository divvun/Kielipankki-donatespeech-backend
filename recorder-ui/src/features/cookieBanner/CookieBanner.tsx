import React from "react";
import "./CookieBanner.css";
import { useDispatch } from "react-redux";
import { analyticsEnabledChange } from "../user/userSlice";
import PlaylistButton from "../playlist/components/PlaylistButton/PlaylistButton";
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import { Link } from "react-router-dom";
import routes from "../../config/routes";

type CookieBannerProps = { lang: string };

interface Langstrings { [key: string]: string; }
interface Langs { [key: string]: Langstrings; }

const fi_strings: Langstrings = {
    "cookie-message": "Lahjoita puhetta.fi -sivusto käyttää evästeitä palvelun kehittämiseen tarvittavan analytiikan takia. Lue lisää",
    "privacy-linktext": "tietosuojasta",
    "deny-button": "Estä evästeet",
    "allow-button": "Hyväksy evästeet",
};

const en_strings: Langstrings = {
};

const sv_strings: Langstrings = {
    "cookie-message": "Webbsidan doneraprat.fi använder cookies för att utveckla tjänsten på grund av nödvändig analytik. Läs mer om",
    "privacy-linktext": "dataskyddet",
    "deny-button": "Jag godkänner inte",
    "allow-button": "Acceptera cookies"
};

const langs: Langs = {
    "fi": fi_strings,
    "en": en_strings,
    "sv": sv_strings,
}

const CookieBanner: React.FC<CookieBannerProps> = ({lang,}) => {
  const dispatch = useDispatch();

  const handleDeny = () => {
    dispatch(analyticsEnabledChange(false));
  };

  const handleAllow = () => {
    dispatch(analyticsEnabledChange(true));
  };

  return (
    <Container fluid className="cookie-banner fixed-bottom">
      <Row>
          <Col md={12} lg={6} className="pb-2">
	  {langs[lang]["cookie-message"]} {" "}
          <Link to={routes.PRIVACY}>{langs[lang]["privacy-linktext"]}</Link>.
        </Col>
        <Col className="d-flex flex-wrap align-items-center">
          <PlaylistButton
            buttonType="outline"
            className="mr-3 mb-2"
            text={langs[lang]["deny-button"]}
            onClick={handleDeny}
          />
          <PlaylistButton
            className="mb-2"
            text={langs[lang]["allow-button"]}
            onClick={handleAllow}
          />
        </Col>
      </Row>
    </Container>
  );
};

export default CookieBanner;
