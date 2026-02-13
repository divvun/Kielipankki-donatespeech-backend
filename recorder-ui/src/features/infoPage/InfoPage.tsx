import React from "react";

import "./InfoPage.css";
import { Link } from "react-router-dom";
import routes from "../../config/routes";

type InfoPageProps = { lang: string };

interface Langstrings { [key: string]: string; }
interface Langs { [key: string]: Langstrings; }

const fi_strings: Langstrings = {
    "h2": "Tietoa hankkeesta",
    "p-1": "Lahjoita puhetta -kampanja kerää luonnollista puhetta ja siihen liittyviä tietoja kaikkialta Suomesta, erilaisilta ihmisiltä. Lahjoittamalla puhettasi autat tutkijoita ja tekoälyä kehittäviä yrityksiä ymmärtämään ja mallintamaan suomenkielisen puheen, suomen murteiden ja erilaisten puhetyylien piirteitä. Tavoitteena on kehittää esimerkiksi puheella ohjattavia sovelluksia ja palveluita, jotka toimivat sujuvasti suomeksi.",
    "p-2": "Puheen lahjoittaminen ja omien taustatietojen ilmoittaminen Lahjoita puhetta -kampanjassa on täysin vapaaehtoista. Kun lahjoitat puhettasi tai muita tietojasi, luovutat samalla Helsingin yliopistolle niihin liittyvät oikeudet. Tämä tarkoittaa, että Helsingin yliopisto voi käyttää ja luovuttaa niitä edelleen kielentutkimukseen sekä tekoälyn tutkimukseen ja kehittämiseen. Ethän lue ääneen tai esitä muiden kirjoittamaa tekstiä, kuten runoja, näytelmien vuorosanoja tai tekstin katkelmia. Nyt saat olla luova!",
    "p-3": "Lahjoittamaasi puhetta ja muita antamiasi tietoja säilytetään ja käsitellään turvallisesti ja suojatusti. Lahjoitetut puhenäytteet ovat ainoastaan luvan saaneiden tutkijoiden ja kehittäjien käytettävissä. Puhenäytteitä tutkittaessa ei pyritä tunnistamaan yksittäisiä henkilöitä. Koska ihmisen puheääni ja puhetapa on yksilöllinen, aineiston käyttäjä voi sattumalta tunnistaa sinut äänesi tai kertomiesi asioiden perusteella. Aineiston käsittely on kuitenkin luottamuksellista. Voit siis jutella ihan vapaasti! Älä kuitenkaan kerro yksityisiä, arkaluonteisia tai luottamuksellisia asioita itsestäsi tai muista ihmisistä.",
    "privacy-prompt": "Lue lisää tietosuojasta",
    "feedback": "Mikäli et löydä sivustolta vastausta kysymykseesi tai kohtaat teknisen ongelman, otathan yhteyttä",
    "faq-h3": "Usein kysytyt kysymykset",
    "faq-h5-why-collect": "Miksi puhetta kerätään?",
    "faq-p-why-collect": "Puhetta kerätään puhetta ymmärtävien ja tuottavien sovellusten ja palveluiden tutkimuksen ja kehityksen sekä kielentutkimuksen tarpeisiin. Lahjoitetun puheen avulla voidaan kehittää suomea paremmin ymmärtäviä ääniohjattuja sovelluksia hyödynnettäviksi esimerkiksi vanhustenhuollossa. Suomenkielisten sovellusten kehittämiseen tarvitaan kuitenkin valtava määrä ihan tavallista puhetta. Tämän yleishyödyllisen Lahjoita puhetta -kampanjan tavoitteena on varmistaa, että voimme käyttää tulevaisuuden palveluita myös suomeksi, juuri siinä muodossa kuin sitä puhumme. Samalla kielentutkijoiden käyttöön syntyy merkittävä aineisto, jonka perusteella he pystyvät tutkimaan esimerkiksi suomen murteiden nykytilannetta, suomen ääntämistä ja sävelkulkua, erilaisten käsitteiden käyttöä, suomen kielen sanastoa, vuorovaikutuksen ilmiöitä – ja varmasti paljon asioita, joista ei vielä nyt tiedetä mitään!",
    "faq-p-why-collect-2": "",
    "faq-h5-how": "Miten lahjoittaminen tapahtuu?",
    "faq-p-how": "Puhetta lahjoitetaan seuraamalla lahjoituskoneen antamia tehtäviä ja ohjeita. Parhaiten lahjoitus onnistuu mobiilisovelluksella, johon linkin löydät etusivulta.",
    "faq-h5-what": "Mitä puheella oikeastaan tarkoitetaan?",
    "faq-p-what": "Puheella tarkoitetaan aivan tavallista arkipuhetta kaikkine takelteluineen, epäröinteineen ja taukoineen. Voit puhua aivan kuin puhuisit muutenkin!",
    "faq-h5-who": "Kuka puhetta kerää?",
    "faq-p-who-1": "Lahjoita puhetta -kampanja toteutetaan Ylen ja Helsingin yliopiston yhteistyönä. Valtion kehitysyhtiö Vake (nyk. Ilmastorahasto) oli mukana käynnistämässä hanketta vuonna 2020. Yle ja Helsingin yliopisto ovat yhdessä vastuussa puheen keräämisestä, ja Helsingin yliopisto on vastuullinen taho lahjoitetun puheen tallentamisen ja käytön osalta. Mukana ollessaan myös Vake oli vastuussa puheen keräämisestä yhdessä Ylen ja Helsingin yliopiston kanssa. Helsingin yliopisto voi arvionsa mukaan luovuttaa aineistoa muiden käyttöön myös kaupallisesti tai siirtää puheaineiston kokonaisuudessaan jollekin toiselle organisaatiolle. Luovutukset toteutetaan aina ",
    "privacy-word": "Tietosuoja",
    "privacy-word-2": "Tietosuoja",
    "faq-p-who-2": " -sivulla esitettyjä periaatteita noudattaen.",
    "faq-h5-how-much": "Miten paljon puhetta on tarkoitus kerätä?",
    "faq-p-how-much": "Hankkeen tavoitteena on kerätä yli 10 000 tuntia suomenkielistä arkipuhetta. Tällaisen määrän arvioidaan merkittävästi parantavan esimerkiksi suomenkielisen automaattisen puheentunnistuksen luotettavuutta. Lisäksi halutaan varmistaa, että mukaan saadaan paljon puhetta mahdollisimman erilaisilta ihmisiltä ja eri puolilta Suomea.",
    "faq-h5-why-diverse": "Miksi tarvitaan kaikkien suomea puhuvien panosta?",
    "faq-p-why-diverse": "Tarvitsemme mahdollisimman monimuotoista puhuttua suomen kieltä, jotta ääniohjatut laitteet toimisivat kaikilla suomen murteilla ja puhetyyleillä sekä kaikenikäisillä käyttäjillä.",
    "faq-h5-remove": "Pystyykö äänittämäni puheen poistamaan?",
    "faq-p-remove-1": "Lahjoituksesi voit poistaa tietokannasta ottamalla yhteyttä osoitteeseen",
    "faq-p-remove-2": "ja kertomalla heille tunnisteesi sekä ilmaisemalla tahtosi poistaa lahjoituksesi tietokannasta. Löydät selainkohtaisen tunnisteesi",
    "privacy-page-word": "Tietosuoja",
    "from-page": " -sivulta",
    "faq-p-remove-4": "Lisäksi aineistoa hallinnoiva taho voi tarvittaessa poistaa puhetallenteita tai muita tietoja.",
    "faq-h5-privacy": "Pääseekö joku kuuntelemaan lahjoitettua puhettani?",
    "faq-p-privacy-1": "Puhettasi saa kuunnella vain henkilö, joka on perustellusta syystä saanut luvan aineiston käyttämiseen. Yksittäisiä puhenäytteitä voivat kuunnella esimerkiksi puheen litteroijat eli henkilöt, jotka kirjoittavat puheen sanallista sisältöä tekstimuotoon. Puheen rinnalla tarvitaan pohja-aineistona myös suuri määrä puheesta litteroituja sanoja ja lauseita, jotta automaattisia järjestelmiä voitaisiin tehokkaasti opettaa tunnistamaan ja tuottamaan suomea. Yksittäisiä näytteitä saattaa kuunnella myös kielentutkija tai esimerkiksi yrityksessä työskentelevä, puhesovellusta kehittävä henkilö, mikäli näytteen kuunteleminen on tarpeellista tutkimuksen tai puhesovelluksen toiminnan varmistamisen kannalta. Myös tällaisissa tilanteissa aineiston käsittely tapahtuu luottamuksellisesti.",
    "faq-p-privacy-2": "Koska Lahjoita puhetta -kampanjan tavoitteena on kerätä mahdollisimman suuri määrä puhetta, jokaista tekemääsi tallennusta ei välttämättä ole mahdollista kuunnella tai tutkia käsityönä. On todennäköistä, että mahdollisen litterointivaiheen jälkeen puhettasi tuleekin “kuuntelemaan” vain kone.",
    "faq-h5-secrecy": "Voidaanko puheeni julkaista jossain?",
    "faq-p-secrecy": "Puhettasi voidaan käyttää ainoastaan tieteellisen tutkimuksen ja korkeakouluopetuksen yhteydessä sekä puhesovellusten kehittämisessä. Valmiissa puhesovelluksissa yksittäisen puhujan lahjoittamaa puhetta ei kuitenkaan ole sellaisenaan mukana: alkuperäisiä puhenäytteitä hyödynnetään ainoastaan järjestelmän tai sen toimintaperiaatteen kehittämisessä. Tulevaisuuden puheohjattavasta sovelluksesta ei siis ole mahdollista tunnistaa, kenen puhetta sen tekemiseen on käytetty, eikä myöskään alkuperäistä puhetta voi kuunnella sen kautta. Myöskään Yle ei julkaise puhettasi minkään kanavansa kautta.",
    "faq-h5-bio-record": "Onko tallennettu puheeni biotunniste?",
    "faq-p-bio-record": "Ihmisen puheääni ja puhetapa ovat yksilöllisiä, joten puhetta voidaan pitää biotunnisteena. Tämä biotunniste on kuitenkin huomattavasti julkisempi kuin esimerkiksi sormenjälkesi tai verkkokalvosi, koska ihmisen puhetta on mahdollista kuulla tai tallentaa lähes kaikissa julkisissa tiloissa. Lahjoita puhetta -kampanjassa kerättävää puheaineistoa ei kuitenkaan käytetä yksittäisen henkilön tunnistamiseen.",
    "faq-h5-handling": "Miten henkilötietoja käsitellään?",
    "faq-p-handling": "Lahjoitettu puhe ja muut siihen liittyvät tiedot sisältävät puhujan henkilötietoja. Niiden käsittelyssä noudatetaan Suomessa voimassa olevaa tietosuojalainsäädäntöä. Lisätietoja henkilötietojen käsittelystä löytyy",
    "faq-h5-selling": "Voiko lahjoittamaani puhetta myydä eteenpäin?",
    "faq-p-selling": "Lahjoitettua puhetta hallinnoivat tahot voivat myydä kerättyä puhetta ja siitä kehitettyjä malleja tai litteroitua tekstiä suomalaisille sekä kansainvälisille tutkijoille ja yrityksille suomenkielistä puhetta ymmärtävien ja tuottavien sovellusten ja palveluiden kehittämisen ja tutkimuksen sekä kielentutkimuksen tarpeisiin.",
    "faq-h5-confidentiality": "Kuka varmistaa lahjoitetun puheen luottamuksellisen käsittelyn?",
    "faq-p-confidentiality-1": "Hankkeen takana seisovat luotettavat yhteiskunnalliset toimijat, kuten Yle, Helsingin yliopisto sekä vuoden 2021 helmikuuhun asti myös Valtion kehitysyhtiö Vake (nyk. Ilmastorahasto). Yle ja Helsingin yliopisto ovat yhdessä vastuussa puheen keräämisestä, ja Helsingin yliopisto on vastuullinen taho lahjoitetun puheen tallentamisen ja käytön osalta. Mukana ollessaan myös Vake oli vastuussa puheen keräämisestä yhdessä Ylen ja Helsingin yliopiston kanssa. Helsingin yliopisto voi arvionsa mukaan luovuttaa aineistoa muiden käyttöön myös kaupallisesti tai siirtää puheaineiston kokonaisuudessaan jollekin toiselle organisaatiolle. Luovutukset toteutetaan aina",
    "on-page": "-sivulla",
    "faq-p-confidentiality-2": "esitettyjä periaatteita noudattaen, ja aineiston käsittely on luottamuksellista.",
    "faq-h5-use": "Miten voin hyödyntää lahjoitettua puhetta omassa tutkimuksessani / omissa liiketoimintasovelluksissamme?",
    "faq-p-use": "Kerätty puhe päätyy Helsingin yliopiston hallintaan, jonka Kielipankista sitä voidaan luovuttaa edelleen niin tutkijoille kuin yrityksillekin, puhesovellusten kehittämiseen ja tutkimukseen sekä kielentutkimukseen.",
    "faq-h5-what-do-i-get": "Mitä minä saan, kun lahjoitan puhetta?",
    "faq-p-what-do-i-get": "Digitalisaation ulottuessa kaikille elämänaloille ja tekoälyn ohjatessa tulevaisuudessa suurta osaa palveluistamme on tärkeää, että teknologia ymmärtää käyttäjiä heidän omilla kielillään. Seurauksena on helpompi tulevaisuuden arki kaikille. Lahjoittaminen on myös hauskaa.",
    "faq-h5-nonnative": "Voinko lahjoittaa puhetta, vaikka äidinkieleni ei ole suomi?",
    "faq-p-nonnative": "Totta kai! Mitä monipuolisemmin saamme kerättyä suomenkielistä puhetta, sitä hyödyllisempi kertyvä aineisto on tutkimuksen ja puhesovellusten kehityksen kannalta - ja sitä monipuolisemmin tulevaisuuden palvelut ymmärtävät kaikkia meitä suomen puhujia."
}

const en_strings: Langstrings = {
}

const sv_strings: Langstrings = {
    "h2": "Om Projektet",
    "p-1": "Donera prat är en kampanj som samlar in vardagligt prat och information om hur vi talar i vardagen från olika slags svensktalande människor i hela Finland. Då du donerar ditt prat hjälper du forskare och företag som utvecklar artificiell intelligens att förstå och efterlikna olika dialekter och sätt att prata. Målet med kampanjen är att till exempel kunna utveckla röststyrda program och tjänster som förstår flytande finlandssvenska. Ditt donerade prat kan också användas för annan forskning.",
    "p-2": "Det är helt frivilligt att donera prat och fylla i bakgrundsuppgifterna. Då du donerar ditt prat eller övrig information skänker du samtidigt rättigheterna till ditt material till Helsingfors universitet och Svenska litteratursällskapet i Finland (SLS). Det betyder att Helsingfors universitet och SLS kan ge möjlighet för forskare att använda materialet för olika slag av vetenskaplig forskning, såsom språkforskning, och för företag att använda materialet  för utveckling av artificiell intelligens. Läs eller presentera inte texter skrivna av andra, såsom dikter, repliker ur pjäser eller textsnuttar. Det här är din chans att vara kreativ!",
    "p-3": "Vi hanterar ditt prat och din övriga information (om du fyller i den) säkert och  med respekt för dina rättigheter. Dina donerade talprover kan endast användas av forskare och utvecklare som beviljats tillstånd att använda dessa data. Vi strävar inte efter att identifiera enskilda personer vid forskning kring de insamlade talproverna, men eftersom våra röster och sätt att prata är individuella kan den som använder materialet slumpmässigt känna igen dig utifrån din röst eller något ämne du pratar om. Allt material hanteras endast för forskning och utveckling och sprids inte på annat sätt, så du kan prata helt fritt! Undvik trots det att berätta privata och känsliga saker om dig själv eller någon annan.",
    "privacy-prompt": "Läs mer om dataskyddet",
    "feedback": "Kontakta oss om vi inte lyckats svara på dina frågor eller om du stött på ett tekniskt problem: ",
    "faq-h3": "Ofta ställda frågor",
    "faq-h5-why-collect": "Varför samlas pratet in?",
    "faq-p-why-collect": "Pratet samlas in för att stödja vetenskaplig forskning av olika slag, bl.a. språkforskning, och för utveckling av program och tjänster som förstår och producerar tal. Med hjälp av det prat som doneras kan man t.ex. utveckla röststyrda program som förstår svenska som sedan till exempel kan användas i äldrevården. För att skapa program som förstår talad svenska behövs en enorm mängd av helt vardagligt tal.",
    "faq-p-why-collect-2": "Målet med den här allmännyttiga kampanjen är att garantera att vi i framtiden kan använda tjänster på vårt eget språk, precis så som vi själva talar det. Samtidigt får bl.a. språkforskare tillgång till en stor mängd material som till exempel kan användas inom dialektforskningen och för att undersöka frågor kring uttal, intonation, begreppsanvändning och mycket annat som vi inte ens känner till i dagens läge!",
    "faq-h5-how": "Hur donerar jag mitt prat?",
    "faq-p-how": "Du donerar prat genom att följa anvisningarna och göra uppgifterna som kommer fram i olika teman. Kom samtidigt ihåg att det är ditt prat som räknas, inte vad du pratar om, så du behöver inte vara rädd för att prata bredvid ämnet!",
    "faq-h5-what": "Vad menas egentligen med ”prat”?",
    "faq-p-what": "”Prat” betyder i det här fallet helt normalt vardagligt tal, med allt vad det innebär. Använd din egen dialekt. Det gör inget om du stakar dig, stammar, tvekar eller håller pauser. Prata precis som du brukar göra!",
    "faq-h5-who": "Vem samlar in pratet?",
    "faq-p-who-1": "Donera prat är en kampanj som genomförs av Yle, Helsingfors universitet och Svenska litteratursällskapet i Finland (SLS). Yle, Helsingfors universitet och SLS ansvarar tillsammans för att samla in pratet och Helsingfors universitet och SLS ansvarar för hanteringen och arkiveringen av materialet. Helsingfors universitet och SLS kan ge andra aktörer (även kommersiella)  rätt att använda materialet helt eller delvis. Användningen av materialet  sker i så fall i enlighet med de principer som uppges under rubriken",
    "privacy-word": "Dataskydd",
    "faq-p-who-2": ".",
    "faq-h5-how-much": "Hur mycket prat vill vi samla in?",
    "faq-p-how-much": "Projektet strävar efter att samla in över tusen timmar av finlandssvenskt vardagsprat. Den här mängden beräknas göra finlandssvensk taligenkänning betydligt pålitligare. Dessutom vill vi försäkra oss om att få så många olika finlandssvenskar som möjligt från olika håll i landet med i kampanjen.",
    "faq-h5-why-diverse": "Varför behövs alla svenskspråkigas insats?",
    "faq-p-why-diverse": "För att kunna skapa program som förstår alla varianter av finlandssvenska krävs en stor mängd material av den svenska som talas av människor i olika åldrar från olika orter i Svenskfinland.",
    "faq-h5-remove": "Kan jag i efterhand radera mitt inspelade prat?",
    "faq-p-remove-1": "Genom att kontakta",
    "faq-p-remove-2": "och meddela den identifikationskod som du fått samt berätta att du önskar radera din donation från databasen kan du under insamlingstiden radera pratet du donerat. Identifikationskoden är specifik för ditt donationsformulär och hittas på",
    "privacy-page-word": "Dataskyddssidan",
    "from-page": "",
    "faq-p-remove-4": "Dessutom kan den aktör som hanterar materialet vid behov radera inspelat prat eller annan information.",
    "faq-h5-privacy": "Kommer någon åt att lyssna på det prat jag donerat?",
    "faq-p-privacy-1": "Enbart personer som har grundad orsak att använda materialet kan lyssna på ditt prat. Till exempel transkriberare eller personer som skriver ner pratet i textform kan höra på enskilda talprover. Vid sidan av pratet behövs också en stor mängd transkriberade ord och meningar som basmaterial för att man effektivt ska kunna lära automatiska program att känna igen och uttrycka sig på svenska. Vetenskapliga forskare eller personer som jobbar i företag som utvecklar program kan även lyssna på talprover. Man får lyssna på talprover endast om det är nödvändigt för forskning eller utvecklande av program.",
    "faq-p-privacy-2": "Eftersom målet med kampanjen Donera prat är att samla in en så stor mängd prat som möjligt är det inte säkert att det är någon människa som kommer att lyssna på ditt prat. Det är möjligtvis endast en maskin som kommer att ”lyssna på” ditt prat efter att det transkriberats.",
    "faq-h5-secrecy": "Kan mitt prat publiceras någonstans?",
    "faq-p-secrecy": "Ditt prat kan enbart användas i samband med vetenskaplig forskning eller högskoleundervisning samt i utvecklandet av program och tjänster som hanterar och genererar tal. I färdiga program eller appar kommer prat som donerats av en enskild person inte att förekomma som sådant. Det är alltså inte möjligt att i framtida program känna igen vems prat som använts då programmet skapats. Man kan heller inte lyssna på det ursprungliga pratet via programmet. Yle kommer heller inte på något sätt att publicera ditt prat via någon av sina kanaler.",
    "faq-h5-bio-record": "Kan jag bli identifierad utifrån det prat jag donerat?",
    "faq-p-bio-record": "Människans röst och sätt att tala är individuella och prat kan därför fungera som biometrisk identifikation. Eftersom en persons prat kan avlyssnas eller spelas in på så gott som alla offentliga platser, så är det betydligt mera offentligt än till exempel dina fingeravtryck eller din näthinna. Materialet som samlas in i Donera prat-kampanjen kommer inte att användas för att identifiera enskilda individer.",
    "faq-h5-handling": "Hur hanteras personuppgifter?",
    "faq-p-handling": "Talet som spelas in och övrig relaterad data innehåller personuppgifter om den som pratar. Vi följer Finlands dataskyddslagstiftning vid hanteringen av uppgifterna. Du hittar mer information om hur personuppgifter hanteras på vår",
    "privacy-word-2": "dataskyddssida",
    "faq-h5-selling": "Kan mitt donerade prat överlåtas eller säljas vidare?",
    "faq-p-selling": "Aktörerna som ansvarar för kampanjen Donera prat kan överlåta eller sälja  inspelat material, transkriberingar eller modeller som genererats ur materialet till inhemska och internationella forskare eller företag som forskar och utvecklar program och tjänster som förstår eller producerar svenskspråkigt tal.",
    "faq-h5-confidentiality": "Vem ser till att det prat som doneras behandlas med respekt för mina rättigheter?",
    "faq-p-confidentiality-1": "Projektet drivs av pålitliga aktörer såsom Yle, Helsingfors universitet och Svenska litteratursällskapet i Finland (SLS). Yle, Helsingfors universitet och SLS är tillsammans ansvariga över att samla in prat och Helsingfors universitet och SLS ansvarar för hanteringen och arkiveringen av materialet och dess användning. Helsingfors universitet och SLS kan ge andra aktörer (även kommersiella) rätt att använda materialet helt eller delvis. Det sker i så fall alltid enligt principerna på vår",
    "on-page": "",
    "faq-p-confidentiality-2": "och materialet behandlas även i fortsättningen med respekt för dina rättigheter.",
    "faq-h5-use": "Hur kan jag utnyttja prat som doneras i min egen forskning / i vårt företags program?",
    "faq-p-use": "Allt inspelat prat hanteras av Helsingfors universitet och SLS som i sin tur kan överlåta materialet till vetenskaplig forskning  eller till företag  som forskar och utvecklar program och tjänster som förstår eller producerar svenskspråkigt tal. Materialet överlåts via Språkbanken eller SLS.",
    "faq-h5-what-do-i-get": "Vad får jag ut av att donera prat?",
    "faq-p-what-do-i-get": "I och med att digitaliseringen fortsätter utvecklas och många av våra tjänster i framtiden kommer att styras av artificiell intelligens är det viktigt att teknologin förstår användarna på deras eget språk. Följden är att alla får en enklare vardag i framtiden. Dessutom är det roligt att donera prat.",
    "faq-h5-nonnative": "Kan jag donera prat fastän svenska inte är mitt modersmål?",
    "faq-p-nonnative": "Så klart! Ju mångsidigare svenskt prat vi samlar in, desto mer nytta har vi av materialet inom forskningen och utvecklingen av röststyrda program och appar - samtidigt som framtida tjänster förstår oss svensktalande på allt fler olika sätt."
}

const langs: Langs = {
    "fi": fi_strings,
    "en": en_strings,
    "sv": sv_strings,
}


const InfoPage: React.FC<InfoPageProps> = ({ lang, }) => {
    const s = langs[lang];

    var mailto = lang !== "sv" ?
	<a href="mailto:lahjoita-puhetta@kielipankki.fi">
          lahjoita-puhetta@kielipankki.fi
    </a>
	:
	<a href="mailto:donaraprat@kielipankki.fi">
          doneraprat@kielipankki.fi
    </a>;


    
    var mobile_remove = lang === "fi" ? (<span>
	Mobiilisovellusta käytettäessä asennuskohtainen tunnisteesi
        löytyy
        {"  "}
        <strong>Lisätietoa</strong>
        {"  "}
        -näkymästä.</span>): "";

  return (
    <div className="info-page frame--view">
	  <h2>{s["h2"]}</h2>
	  <p className="mb-4">
	  {s["p-1"]}
      </p>
	  <p className="mb-4">
	  {s["p-2"]}
      </p>
	  <p className="mb-4">
	  {s["p-3"]}
      </p>
      <p className="mb-4">
          <Link to={routes.PRIVACY}>{s["privacy-prompt"]}</Link>
      </p>

	  <p className="mb-4">
	  {s["feedback"]}
      {"  "}
      {mailto}
        .
      </p>

	  <h3 className="mt-5 mb-4">{s["faq-h3"]}</h3>


	  <h5>{s["faq-h5-how"]}</h5>
	  <p className="mb-4">
	  {s["faq-p-how"]}
      </p>

      <h5>{s["faq-h5-what"]}</h5>
	  <p className="mb-4">
	  {s["faq-p-what"]}
      </p>

      <h5>{s["faq-h5-who"]}</h5>
	  <p className="mb-4">
	  {s["faq-p-who-1"]}
        {"  "}
        <Link to={routes.PRIVACY}>{s["privacy-word"]}</Link>
      {s["faq-p-who-2"]}
      </p>

	  <h5>{s["faq-h5-why-collect"]}</h5>
	  <p className="mb-4">
	  {s["faq-p-why-collect"]}
      </p>
	  <p className="mb-4">
	  {s["faq-p-why-collect-2"]}
      </p>


      <h5>{s["faq-h5-how-much"]}</h5>
	  <p className="mb-4">
	  {s["faq-p-how-much"]}
      </p>

      <h5>{s["faq-h5-why-diverse"]}</h5>
	  <p className="mb-4">
	  {s["faq-p-why-diverse"]}
      </p>

	  <h5>{s["faq-h5-what-do-i-get"]}</h5>
	  <p className="mb-4">
	  {s["faq-p-what-do-i-get"]}
      </p>

      <h5>{s["faq-h5-nonnative"]}</h5>
	  <p className="mb-4">
	  {s["faq-p-nonnative"]}
      </p>


      <h5>{s["faq-h5-remove"]}</h5>
	  <p className="mb-4">
	  {s["faq-p-remove-1"]}
      {"  "}
      {mailto}
          {"  "}
      {s["faq-p-remove-2"]}
        {"  "}
        <Link to={routes.PRIVACY}>{s["privacy-page-word"]}</Link>
      {s["from-page"]}. {"  "}
      {mobile_remove}
      </p>

	  <p className="mb-4">
	  {s["faq-p-remove-4"]}
      </p>

      <h5>{s["faq-h5-privacy"]}</h5>

	  <p className="mb-4">
	  {s["faq-p-privacy-1"]}
      </p>

	  <p className="mb-4">
	  {s["faq-p-privacy-2"]}
      </p>

      <h5>{s["faq-h5-secrecy"]}</h5>
	  <p className="mb-4">
	  {s["faq-p-secrecy"]}
      </p>

      <h5>{s["faq-h5-bio-record"]}</h5>
	  <p className="mb-4">
	  {s["faq-p-bio-record"]}
      </p>

      <h5>{s["faq-h5-handling"]}</h5>
	  <p className="mb-4">
	  {s["faq-p-handling"]}
        {"  "}
        <Link to={routes.PRIVACY}>{s["privacy-word-2"]}</Link>
        {s["from-page"]}.
      </p>

      <h5>{s["faq-h5-selling"]}</h5>
	  <p className="mb-4">
	  {s["faq-p-selling"]}
      </p>

      <h5>{s["faq-h5-confidentiality"]}</h5>
	  <p className="mb-4">
	  {s["faq-p-confidentiality-1"]}
      {" "}
        <Link to={routes.PRIVACY}>{s["privacy-word-2"]}</Link>
          {s["on-page"]} {s["faq-p-confidentiality-2"]}
      </p>

      <h5>{s["faq-h5-use"]}
      </h5>
	  <p className="mb-4">
	  {s["faq-p-use"]}
      </p>

    </div>
  );
};

export default InfoPage;
