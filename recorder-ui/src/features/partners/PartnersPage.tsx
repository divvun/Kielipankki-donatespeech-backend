import React from "react";
import yleLogo from "./yleBlack.png";
import hyLogo from "./hyBlack.png";
import slsLogo from "./sls_logo.png";
import "./PartnersPage.css";

type PartnersPageProps = { lang: string };

interface Langstrings { [key: string]: string; }
interface Langs { [key: string]: Langstrings; }

const fi_strings: Langstrings = {
    "h2": "Yhteistyökumppanit",
    "p": "Lahjoita puhetta -kampanja toteutetaan Ylen ja Helsingin yliopiston yhteistyönä. Valtion kehitysyhtiö Vake (nyk. Ilmastorahasto) oli mukana käynnistämässä hanketta vuonna 2020.",
}

const en_strings: Langstrings = {
}

const sv_strings: Langstrings = {
    "h2": "Samarbetspartner",
    "p": "Kampanjen Donera prat är ett samarbete mellan Yle, Helsingfors universitet och Svenska litteratursällskapet i Finland. Statens utvecklingsbolag Vake (nuförtiden Klimatfonden) var med och startade motsvarande projekt på finska år 2020.",
}

const langs: Langs = {
    "fi": fi_strings,
    "en": en_strings,
    "sv": sv_strings,
}


const PartnersPage: React.FC<PartnersPageProps> = ({lang, }) => {
    var partner_icons = lang !== "sv" ?
	<div className="partner-page--icons partner-page--icons-1 d-flex flex-wrap justify-content-center">
        <div className="d-flex flex-wrap justify-content-center">
        <img src={hyLogo} alt="Helsingin yliopisto" />
        <img src={yleLogo} alt="Yle" />
        </div>
	</div> :
	<div className="partner-page--icons partner-page--icons-1 d-flex flex-wrap justify-content-center">
        <div className="d-flex flex-wrap justify-content-center">
        <img src={hyLogo} alt="Helsingfors Universitet" />
        <img src={yleLogo} alt="Yle" />
	<img src={slsLogo} alt="SLS" />
        </div>
	</div>
	;

  return (
    <div className="partners-page frame--view">
      <h2>{langs[lang]["h2"]}</h2>
	  <p className="mb-4">
	  {langs[lang]["p"]}
      </p>
	  {partner_icons}
    </div>
  );
};

export default PartnersPage;
