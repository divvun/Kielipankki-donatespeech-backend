import React from "react";
import { useDispatch } from "react-redux";
import { Link } from "react-router-dom";
import PlaylistButton from "../../playlist/components/PlaylistButton/PlaylistButton";
import { termsAndConditionAccepted } from "../../user/userSlice";

import "./TermsAndConditionsView.css";
import routes from "../../../config/routes";

const CAMPAIGN_URL = "https://lahjoitapuhetta.fi";
const KIELIPANKKI_URL = "https://www.kielipankki.fi";
const SPRAKBANKEN_URL = "https://www.kielipankki.fi/sprakbanken";

const largerBodyTextStyle = {
  fontSize: "larger",
};

type TermsAndConditionsViewProps = { lang: string };

interface Langstrings {
  [key: string]: string;
}
interface Langs {
  [key: string]: Langstrings;
}

const fi_strings: Langstrings = {
  "h4-thanks": "Kiitos, kun tulit!",
  "p-thanks":
    "Tällä sivulla on perustiedot hankkeesta. Kun olet lukenut ne, pääset sivun alalaidasta aloittamaan lahjoittamisen.",
  "h4-what": "Mikä on Lahjoita puhetta -kampanja?",
  "p-what-1":
    "Lahjoita puhetta -kampanja kerää luonnollista puhetta ja siihen liittyviä tietoja kaikkialta Suomesta, erilaisilta ihmisiltä.",
  "p-what-2":
    "Tavoitteena on, että kielen tutkijat sekä tekoälyn kehittäjät ja tutkijat voisivat hyödyntää suomea puhetta ymmärtävien ja tuottavien sovellusten ja palveluiden kehitykseen ja tutkimukseen sekä kielentutkimukseen. Tätä tavoitetta varten puheaineistoa luovutetaan tutkijoille ja yrityksille.",
  "p-what-3": "Lisätietoja kampanjasta löytyy",
  "p-what-3-linktext": "täältä",
  "h4-who": "Kuka puhetta kerää?",
  "p-who":
    "Lahjoita puhetta toteutetaan Helsingin yliopiston Kielipankin, Valtion kehitysyhtiö Recorder Oy:n ja Yleisradio Oy:n yhteistyönä. Helsingin yliopisto Recorder ja Yle ovat yhdessä vastuussa puheen keräämisestä ja Helsingin yliopisto on vastuullinen taho lahjoitetun puheen tallentamisen ja käytön osalta. Jatkossa Helsingin yliopisto voi siirtää puheaineiston kokonaisuudessaan jollekin toiselle organisaatiolle ja aineistoa voidaan antaa muiden käyttöön tässä esitettyjä sääntöjä noudattaen.",
  "h4-voluntary": "Täysin vapaaehtoista!",
  "p-voluntary":
    "Puheen lahjoittaminen ja henkilötietojen ilmoittaminen Lahjoita puhetta -kampanjassa on täysin vapaaehtoista.",
  "h4-handling": "Miten henkilötietoja käsitellään?",
  "p-handling":
    "Lahjoitettu puhe ja muut siihen liittyvät tiedot sisältävät puhujan henkilötietoja. Niiden käsittelyssä noudatetaan Suomessa voimassa olevaa tietosuojalainsäädäntöä. Lisätietoja henkilötietojen käsittelystä löytyy",
  "p-handling-linktext": "täältä",
  "h4-rights": "Oikeudet puheeseen",
  "p-rights-1":
    "Sinulla voi olla tekijänoikeuslain mukaisia tai muita oikeuksia lahjoittamaasi puheeseen.",
  "p-rights-2":
    "Annat Helsingin yliopistolle nämä oikeutesi, siinä määrin kuin se on puhetta ymmärtävän tai tuottavan tekoälyn kehittämisen ja tutkimuksen, kielentutkimuksen tai näihin tarkoituksiin liittyvän korkeakouluopetuksen kannalta tarpeellista ja lain mukaan mahdollista. Helsingin yliopisto saa luovuttaa ne edelleen.",
  "p-rights-3":
    "Ethän käytä puheessasi muiden kirjoittamaa tekstiä, kuten runoja, näytelmien vuorosanoja tai tekstin katkelmia etkä kerro itseäsi tai muita ihmisiä koskevia yksityisiä, arkaluonteisia tai luottamuksellisia asioita.",
  "h4-more-info": "Lisätietoja",
  "footer-p":
    "Painamalla alla olevaa Hyväksyn-nappia hyväksyn edellä olevat puheen lahjoittamisen ehdot. Jos olen alle 18-vuotias, huoltajani hyväksyy ehdot puolestani.",
  accept: "Hyväksyn",
};

const en_strings: Langstrings = {};

const sv_strings: Langstrings = {
  "h4-thanks": "Tack för att du kom!",
  "p-thanks":
    "Här kan du läsa den centrala informationen om kampanjen. När du läst den kan du börja donera prat nere på sidan.",
  "h4-what": "Vad är kampanjen Donera prat?",
  "p-what-1":
    "Donera prat är en kampanj som samlar in vardagligt prat och information om hur vi talar i vardagen från olika slags svensktalande människor i hela Finland.",
  "p-what-2":
    "Målet med kampanjen är att till exempel kunna utveckla röststyrda program och tjänster som förstår flytande finlandssvenska. Pratet du donerar kan också användas för annan forskning, såsom språkforskning.",
  "p-what-3": "Du hittar mer information om kampanjen",
  "p-what-3-linktext": "här",
  "h4-who": "Vem samlar in pratet?",
  "p-who":
    "Kampanjen genomförs av Yle, Helsingfors universitet (HU) och Svenska litteratursällskapet i Finland (SLS). Yle, HU och SLS ansvarar tillsammans för att samla in pratet och HU och SLS ansvarar för hanteringen och arkiveringen av materialet. HU och SLS kan ge andra aktörer (även kommersiella) rätt att använda materialet helt eller delvis i enlighet med de principer som uppges under rubriken Dataskydd.",
  "h4-voluntary": "Helt frivilligt!",
  "p-voluntary":
    "Det är helt frivilligt att donera prat eller fylla i personuppgifter i den här kampanjen.",
  "h4-handling": "Hur hanteras personuppgifter?",
  "p-handling":
    "Talet som spelas in och övrig relaterad data innehåller personuppgifter om den som pratar. Vi följer Finlands dataskyddslagstiftning vid hanteringen av uppgifterna. Du hittar mer information om hur personuppgifter hanteras på vår",
  "p-handling-linktext": "dataskyddssida",
  "h4-rights": "Rättigheter till ditt prat",
  "p-rights-1":
    "Enligt t.ex. upphovsrättslagen kan du ha rättigheter till pratet du donerar.",
  "p-rights-2":
    "Då du donerar ditt prat ger du de här rättigheterna till Helsingfors universitet (HU) och Svenska Litteratursällskapet i Finland (SLS) i den mån mån de behövs för följande typer av verksamhet: utvecklandet av röststyrning och annan artificiell intelligens, forskning eller forskningsrelaterad verksamhet inom högskoleundervisningen. Rättigheterna överlåts ändå bara i den utsträckning lagen möjliggör. HU och SLS har också rätt att dela uppgifterna vidare.",
  "p-rights-3":
    "Läs eller presentera inte texter skrivna av andra, såsom dikter, repliker ur pjäser eller textsnuttar.",
  "h4-more-info": "Mer information",
  "footer-p":
    "Genom att klicka på Godkänner-knappen nedan godkänner jag villkoren för att donera prat. Om jag är under 18 år, godkänner min vårdnadshavare villkoren i stället.",
  accept: "Godkänner",
};

const langs: Langs = {
  fi: fi_strings,
  en: en_strings,
  sv: sv_strings,
};

const TermsAndConditionsView: React.FC<TermsAndConditionsViewProps> = ({
  lang,
}) => {
  const EMAIL_ADDRESS =
    lang !== "sv"
      ? "lahjoita-puhetta@kielipankki.fi"
      : "doneraprat@kielipankki.fi";

  var s = langs[lang];

  var moreinfo =
    lang !== "sv" ? (
      <p>
        Kampanjan sivusto:
        {"  "}
        <a href={CAMPAIGN_URL}>lahjoitapuhetta.fi</a>
        <br />
        Helsingin yliopisto, Kielipankki,
        {"  "}
        <a target="_blank" rel="noopener noreferrer" href={KIELIPANKKI_URL}>
          {KIELIPANKKI_URL}
        </a>
        {", "}
        <a href={`mailto: ${EMAIL_ADDRESS}`}>{EMAIL_ADDRESS}</a>
      </p>
    ) : (
      <p>
        Kampanjens sida:
        {"  "}
        <a href={CAMPAIGN_URL}>doneraprat.fi</a>
        <br />
        Helsingfors universitet, Språkbanken,
        {"  "}
        <a target="_blank" rel="noopener noreferrer" href={SPRAKBANKEN_URL}>
          {KIELIPANKKI_URL}
        </a>
        {", "}
        <a href={`mailto: ${EMAIL_ADDRESS}`}>{EMAIL_ADDRESS}</a>
      </p>
    );

  const dispatch = useDispatch();
  return (
    <div className="terms-and-conditions-view">
      <h4>{s["h4-thanks"]}</h4>
      <p>
        <strong style={largerBodyTextStyle}>{s["p-thanks"]}</strong>
      </p>
      <h4>{s["h4-what"]}</h4>
      <p>{s["p-what-1"]}</p>
      <p>{s["p-what-2"]}</p>
      <p>
        {s["p-what-3"]}
        {"  "}
        <Link to={routes.INFO}>{s["p-what-3-linktext"]}</Link>
        {". "}
      </p>
      <h4>{s["h4-who"]}</h4>
      <p>{s["p-who"]}</p>
      <h4>{s["h4-voluntary"]}</h4>
      <p>{s["p-voluntary"]}</p>
      <h4>{s["h4-handling"]}</h4>
      <p>
        {s["p-handling"]}
        {"  "}
        <Link to={routes.PRIVACY}>{s["p-handling-linktext"]}</Link>
        {". "}
      </p>
      <h4>{s["h4-rights"]}</h4>
      <p>{s["p-rights-1"]}</p>
      <p>{s["p-rights-2"]}</p>
      <p>{s["p-rights-3"]}</p>
      <h4>{s["h4-more-info"]}</h4>
      {moreinfo}
      <div className="terms-and-conditions-footer">
        <p>{s["footer-p"]}</p>
        <PlaylistButton
          text={s["accept"]}
          onClick={() => dispatch(termsAndConditionAccepted())}
        />
      </div>
    </div>
  );
};

export default TermsAndConditionsView;
