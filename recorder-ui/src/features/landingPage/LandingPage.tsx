import React from "react";
import { Link } from "react-router-dom";
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Themes from "../theme/Themes";
import NavigationBar from "../navigation/NavigationBar/NavigationBar";
import routes from "../../config/routes";
import AppIcons from "../components/AppIcons/AppIcons";

import logo from "./Lahjoita_puhetta_Logo.svg";
import logoSv from "./donera_prat_logo.png";
import image from "./landing-page-img.png";
import imageSv from "./landing-page-img-sv.png";
import yleLogo from "./yleWhite.png";
import hyLogo from "./hyWhite.png";
import slsLogo from "./sls_logo.png";
import "./LandingPage.css";

type LandingPageProps = { lang: string };

interface Langstrings { [key: string]: string; }
interface Langs { [key: string]: Langstrings; }

const fi_strings: Langstrings = {
    "page-title": "Pulistaan meille parempia palveluja",
    "page-description": "Nyt kerätään kaikenlaista puhuttua suomea! Lahjoittamasi puheen avulla esimerkiksi ääniohjatut laitteet voivat oppia ymmärtämään erilaisia murteita ja puhetapoja. Valitse alta aihe, josta haluat puhua.",
    "mobile-app-suggestion": "Lahjoittaminen onnistuu parhaiten mobiilisovelluksella:",
    "content-head": "Puheentunnistus toimimaan myös suomeksi — kauniit murteemme huomioiden",
    "content-body1": "Lahjoita puhetta -hanke kerää suomenkielisiä puhenäytteitä.",
    "content-body2": "Lahjoitukset auttavat kehittämään esimerkiksi puheentunnistusta, joka ymmärtää kaikenlaista suomea – murteineen, taukoineen ja takelteluineen.",
    "content-body3": "Näin pystymme käyttämään tulevaisuuden puheohjattuja laitteita ja palveluja entistä sujuvammin myös suomen kielellä. Sujuva puheohjaus on erityisen tärkeää hoitotyössä, kuten vanhustenhuollossa.",
    "confidentiality-promise-head": "Lahjoittamasi puhe käsitellään luottamuksella",
    "confidentiality-promise-body": "Lahjoittamaasi puhetta käytetään tekoälyn tutkimukseen ja kehitykseen sekä kielentutkimukseen. Lahjoituksesi päätyy Helsingin yliopiston hallintaan ja voidaan Kielipankin kautta välittää edelleen suomalaisille ja kansainvälisille yrityksille sekä tutkijoille. Lahjoittajia ei pyritä tunnistamaan, mutta vältä kuitenkin nimien ja arkaluontoisten asioiden mainitsemista.",
    "privacy-info-linktext": "Lue lisää tietosuojasta",
    "credits-1": "Tämän yleishyödyllisen hankkeen takana ovat muun muassa",
    "credits-2": "Yle ja Helsingin yliopisto",
    "credits-3": "Valtion kehitysyhtiö Vake (nyk. Ilmastorahasto) oli mukana käynnistämässä hanketta vuonna 2020."
}

const en_strings: Langstrings = {
    "page-title": "Talking about better services",
    "page-description": "We're collecting all kinds of spoken language! The speech you donate can be used to improve the ability of voice-controlled devices to understand different dialects and speech patterns. Choose the topic you'd like to speak about below.",
    "mobile-app-suggestion": "Lahjoittaminen onnistuu parhaiten mobiilisovelluksella:",
    "content-head": "Puheentunnistus toimimaan myös suomeksi — kauniit murteemme huomioiden",
    "content-body1": "Lahjoita puhetta -hanke kerää suomenkielisiä puhenäytteitä.",
    "content-body2": "Lahjoitukset auttavat kehittämään esimerkiksi puheentunnistusta, joka ymmärtää kaikenlaista suomea – murteineen, taukoineen ja takelteluineen.",
    "content-body3": "Näin pystymme käyttämään tulevaisuuden puheohjattuja laitteita ja palveluja entistä sujuvammin myös suomen kielellä. Sujuva puheohjaus on erityisen tärkeää hoitotyössä, kuten vanhustenhuollossa.",
    "confidentiality-promise-head": "Lahjoittamasi puhe käsitellään luottamuksella",
    "confidentiality-promise-body": "Lahjoittamaasi puhetta käytetään tekoälyn tutkimukseen ja kehitykseen sekä kielentutkimukseen. Lahjoituksesi päätyy Helsingin yliopiston hallintaan ja voidaan Kielipankin kautta välittää edelleen suomalaisille ja kansainvälisille yrityksille sekä tutkijoille. Lahjoittajia ei pyritä tunnistamaan, mutta vältä kuitenkin nimien ja arkaluontoisten asioiden mainitsemista.",
    "privacy-info-linktext": "Lue lisää tietosuojasta",
    "credits-1": "Tämän yleishyödyllisen hankkeen takana ovat muun muassa",
    "credits-2": "Yle ja Helsingin yliopisto",
    "credits-3": "Valtion kehitysyhtiö Vake (nyk. Ilmastorahasto) oli mukana käynnistämässä hanketta vuonna 2020."
}

const sv_strings: Langstrings = {
    "page-title": "Prata - för bättre betjäning på svenska",
    "page-description": "Nu samlar vi in talad svenska på alla olika dialekter! Tack vare det prat du donerar lär vi till exempel röststyrda enheter att förstå olika dialekter och olika sätt att tala. Nedan får du välja vilket ämne just du vill prata om.",
    "mobile-app-suggestion": "",
    "content-head": " Taligenkänning på finlandssvenska — med alla våra härliga dialekter",
    "content-body1": "Donera prat är ett projekt som samlar in vardagligt tal på finlandssvenska.",
    "content-body2": "Med hjälp av alla donationer kan vi till exempel utveckla en taligenkänning som förstår finlandssvenska - med språkets alla dialekter och uttal.",
    "content-body3": "Då kan vi smidigt använda framtidens röststyrda apparater på vårt eget språk - till och med på vår egen dialekt. En fungerande röststyrning är extra viktigt inom vården, till exempel åldringsvården.",
    "confidentiality-promise-head": "Vi hanterar din donation med respekt för dina rättigheter",
    "confidentiality-promise-body": "Det prat som du donerar används för vetenskaplig forskning, t.ex. språkvetenskap, och för utveckling av artificiell intelligens. Din donation hanteras av Helsingfors universitet och Svenska litteratursällskapet i Finland (SLS) och kan via Språkbanken och SLS delas vidare till forskare samt finska och internationella företag. Vi kommer inte att försöka identifiera de personer som donerar. Undvik ändå att nämna namn och annan känslig information.",
    "privacy-info-linktext": "Läs mer om dataskyddet",
    "credits-1": "Det här allmännyttiga projektet genomförs av",
    "credits-2": "Yle, Helsingfors universitet och Svenska Litteratursällskapet i Finland (SLS)",
    "credits-3": "Statens utvecklingsbolag Vake (nuförtiden Klimatfonden) var med om att starta motsvarande projekt på finska år 2020."
}

const langs: Langs = {
    "fi": fi_strings,
    "en": en_strings,
    "sv": sv_strings,
}

const LandingPage: React.FC<LandingPageProps> = ({
    lang,
}) => {
    var s = langs[lang]

    var sls_logo = lang === "sv" ?
	<img src={slsLogo} alt="SLS - Svenska Litteratursällskapet i Finland" />: "";
    
    var mobile_app = s["mobile-app-suggestion"] !== "" ? <Row className=" landing-page-app-icons">
	<Col>
	<p>
	{s["mobile-app-suggestion"]}
    </p>
	<AppIcons />
	</Col>
	</Row>
	: "";
    
  return (
    <Container fluid>
      <Row className="landing-page">
        <Col>
          <Row className="landing-page-part landing-page-part-1 ">
            <Col className="landing-page-part-content">
              <Row>
                <Col>
                  <NavigationBar lang={lang}/>
                </Col>
              </Row>
              <Row>
                <Col className="landing-page-part-1-content">
                  <Row className="landing-page-logo">
          <img src={lang !== "sv"? logo: logoSv} alt="Lahjoita puhetta" />
                  </Row>
                  <Row>
                    <h2 className="landing-page-title">
          {s["page-title"]}
                    </h2>
          <p className="landing-page-description">
	  {s["page-description"]}
                    </p>
                  </Row>
                  <Row className="landing-page-themes">
                    <Col className="px-0">
          <Themes lang={lang}/>
                    </Col>
          </Row>
	  {mobile_app}
                </Col>
              </Row>
            </Col>
          </Row>
          <Row className="landing-page-part landing-page-part-2 ">
            <Col xs={12} className="landing-page-part-content">
              <Row className="justify-content-end">
                <Col sm={12} md={8}>
          <h2>
	  {s["content-head"]}
                  </h2>
          <p>
	  {s["content-body1"]}
                  </p>
          <p>
	  {s["content-body2"]}
                  </p>
          <p>
	  {s["content-body3"]}
                  </p>
                </Col>
                <Col className="mx-auto" xs={8} sm={6} md={4}>
          <img src={lang !== "sv"? image: imageSv} alt={lang !== "sv"? "Moro, terve, tsau!": "Tjena, hej, hallå!"} />
                </Col>
              </Row>
            </Col>
          </Row>
          <Row className="landing-page-part landing-page-part-3 ">
            <Col className="landing-page-part-content" xs={12}>
          <h2>
	  {s["confidentiality-promise-head"]}
      </h2>
          <p>
	  {s["confidentiality-promise-body"]}
          </p>
          <Link to={routes.PRIVACY}>{s["privacy-info-linktext"]}</Link>
            </Col>
          </Row>
          <Row className="landing-page-part landing-page-part-4">
            <Col className="landing-page-part-content " xs={12}>
          <p>
	  {s["credits-1"]}
                {"  "}
                <b>{s["credits-2"]}</b>
                {". "}
      {s["credits-3"]}
              </p>
              <div className="d-flex flex-wrap justify-content-center">
                <img src={hyLogo} alt="Helsingin yliopisto" />
                <img src={yleLogo} alt="Yle" />
	  {sls_logo}
              </div>
            </Col>
          </Row>
        </Col>
      </Row>
    </Container>
  );
};

export default LandingPage;
