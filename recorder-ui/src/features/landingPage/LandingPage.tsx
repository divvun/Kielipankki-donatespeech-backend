import React from "react";
import { Link } from "react-router-dom";
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Themes from "../theme/Themes";
import NavigationBar from "../navigation/NavigationBar/NavigationBar";
import routes from "../../config/routes";
import AppIcons from "../components/AppIcons/AppIcons";

import hyLogo from "./hyWhite.png";
import "./LandingPage.css";

type LandingPageProps = {};

const LandingPage: React.FC<LandingPageProps> = () => {
  return (
    <Container fluid>
      <Row className="landing-page">
        <Col>
          <Row className="landing-page-part landing-page-part-1 ">
            <Col className="landing-page-part-content">
              <Row>
                <Col>
                  <NavigationBar />
                </Col>
              </Row>
              <Row>
                <Col className="landing-page-part-1-content">
                  <Row>
                    <h2 className="landing-page-title">
                      Let’s chat our way to better services
                    </h2>
                    <p className="landing-page-description">
                      We’re collecting all kinds of spoken Finnish! Your
                      donation helps, for example, voice-controlled devices
                      learn to understand different dialects and ways of
                      speaking. Choose a topic below that you want to talk
                      about.
                    </p>
                  </Row>
                  <Row className="landing-page-themes">
                    <Col className="px-0">
                      <Themes />
                    </Col>
                  </Row>
                  <Row className=" landing-page-app-icons">
                    <Col>
                      <p>Donating works best with the mobile app:</p>
                      <AppIcons />
                    </Col>
                  </Row>
                </Col>
              </Row>
            </Col>
          </Row>
          <Row className="landing-page-part landing-page-part-2 ">
            <Col xs={12} className="landing-page-part-content">
              <Row className="justify-content-end">
                <Col sm={12} md={8}>
                  <h2>
                    Speech recognition that works in Finnish too — including our
                    beautiful dialects
                  </h2>
                  <p>
                    The “Project name” campaign collects Finnish speech samples.
                  </p>
                  <p>
                    Donations help develop, for example, speech recognition that
                    understands all kinds of Finnish — with its dialects,
                    pauses, and stumbles.
                  </p>
                  <p>
                    This way we can use future voice-controlled devices and
                    services more smoothly in Finnish as well. Fluent voice
                    control is especially important in care work, such as elder
                    care.
                  </p>
                </Col>
              </Row>
            </Col>
          </Row>
          <Row className="landing-page-part landing-page-part-3 ">
            <Col className="landing-page-part-content" xs={12}>
              <h2>Your donated speech is handled confidentially</h2>
              <p>
                Your donated speech is used for AI research and development as
                well as language research. Your donation is managed by the
                University of Helsinki and may be shared via the Language Bank
                with Finnish and international companies and researchers. Donors
                are not identified, but please avoid mentioning names and
                sensitive matters.
              </p>
              <Link to={routes.PRIVACY}>Read more about privacy</Link>
            </Col>
          </Row>
          <Row className="landing-page-part landing-page-part-4">
            <Col className="landing-page-part-content " xs={12}>
              <p>
                This public-interest initiative is backed by, among others,
                {"  "}
                <b>the University of Helsinki</b>
                {". "}
              </p>
              <div className="d-flex flex-wrap justify-content-center">
                <img src={hyLogo} alt="University of Helsinki" />
              </div>
            </Col>
          </Row>
        </Col>
      </Row>
    </Container>
  );
};

export default LandingPage;
