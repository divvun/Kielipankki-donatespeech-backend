import React from "react";
import "./PrivacyPage.css";
import { useSelector, useDispatch } from "react-redux";
import { Link } from "react-router-dom";
import { selectClientId, userStateReset } from "../user/userSlice";
import PlaylistButton from "../playlist/components/PlaylistButton/PlaylistButton";
import { playlistStateReset } from "../playlist/playlistSlice";

import balanceTest from "./tasapainotesti.pdf";
import balanceTestSv from "./jämviktstest.pdf";
import routes from "../../config/routes";

type PrivacyPageProps = { lang: string };

interface Langstrings {
  [key: string]: string;
}
interface Langs {
  [key: string]: Langstrings;
}

const fi_strings = {
  privacy: "Tietosuoja",
  "privacy-p-1": `Lahjoita puhetta toteutetaan Helsingin yliopiston (HY) ja 
Yleisradio Oy:n (Yle) yhteistyönä. Valtion kehitysyhtiö Recorder Oy 
(Recorder, nyk. Ilmastorahasto) oli mukana käynnistämässä hanketta 
vuonna 2020. HY ja Yle ovat yhdessä vastuussa puheen keräämisestä, 
Helsingin yliopisto on vastuullinen taho lahjoitetun puheen 
tallentamisen ja jakamisen osalta ja Yle sovelluksen käytöstä 
kerättävän teknisen tiedon osalta. Mukana ollessaan myös Recorder oli 
vastuussa puheen keräämisestä yhdessä Ylen ja Helsingin yliopiston 
kanssa. Jatkossa HY voi siirtää puheaineiston kokonaisuudessaan 
jollekin toiselle organisaatiolle ja aineistoa voidaan antaa muiden 
käyttöön myös kaupallisesti tässä esitettyjä sääntöjä noudattaen.`,
  "privacy-p-2": `Puhujalla voi olla tekijänoikeuslain mukaisia tai muita oikeuksia
lahjoittamaansa puheeseen. Puhuja antaa Helsingin yliopistolle nämä
oikeutensa, siinä määrin kuin se on puhetta ymmärtävän tai tuottavan
tekoälyn kehittämisen ja tutkimuksen tai kielentutkimuksen kannalta
tarpeellista ja lain mukaan mahdollista.`,
  "privacy-p-3": `Puheen lahjoittaminen ja henkilötietojen ilmoittaminen Lahjoita puhetta
-kampanjassa on täysin vapaaehtoista. Lahjoitettu puhe ja muut siihen
liittyvät tiedot sisältävät puhujan henkilötietoja. Niiden käsittelyssä
noudatetaan Suomessa voimassa olevaa tietosuojalainsäädäntöä, johon myös
tällä sivulla annetut tiedot perustuvat.`,
  "remove-h4": "Lahjoittamasi puheen poistaminen",
  "remove-p-1":
    "Lahjoituksesi voit poistaa tietokannasta ottamalla yhteyttä osoitteeseen",
  "remove-p-2":
    "ja kertomalla heille tunnisteesi sekä ilmaisemalla tahtosi poistaa lahjoituksesi tietokannasta.",
  "your-code": "Ota talteen selainkohtainen tunnisteesi:",
  "clear-browser-h4":
    "Lahjoittamiseen liittyvien tietojen poistaminen selaimesta",
  "clear-browser-p": `Mikäli olet esimerkiksi yhteiskäyttöisellä koneella vaikkapa kirjastossa
tai muuten haluat, ettei tämä käyttämäsi selain muista lahjoittamasi
puheen määrää eikä tekemiäsi valintoja, voit poistaa tiedot selaimesta
painamalla “Tyhjennä tiedot” -painiketta. Samalla vaihtuu
selainkohtainen tunnisteesi, joten otathan nykyisen tunnisteesi talteen
ennen tietojen tyhjentämistä!`,
  "clear-browser": "Tyhjennä tiedot",
  "personal-info-h3": "Tietoa henkilötietojen käsittelystä",
  "personal-info-p-1": `Lahjoita puhetta -kampanjan tuottamat aineistot sisältävät puhujien
henkilötietoja. Näitä henkilötietoja käsitellään Suomessa voimassa
olevan tietosuojalainsäädännön mukaisesti. Puheen lahjoittaminen ja
henkilötietojen ilmoittaminen Lahjoita puhetta -kampanjassa on täysin
vapaaehtoista.`,
  "personal-info-p-2": `Sinulla on oikeus saada tietää, mihin tarkoituksiin ja millä tavoilla
käsittelemme henkilötietojasi. Pyrimme tällä kuvauksella
tietosuojakäytännöistämme antamaan kattavan kuvan henkilötietojen
käsittelystä Lahjoita puhetta -kampanjan tuottamien aineistojen osalta.
Jos jokin osa tästä henkilötietojen käsittelystä jää kuitenkin
epäselväksi, voit esittää meille käsittelyä koskevia tarkentavia
kysymyksiä.`,
  "registry-maintainers-h4": "Rekisterinpitäjät",
  "registry-maintainers-p": `Rekisterinpitäjiä ovat Helsingin yliopisto, Yleisradio Oy ja helmikuuhun 
2021 asti myös Valtion kehitysyhtiö Recorder Oy (nyk. Ilmastorahasto).`,
  "registry-maintainers-contact-h5": `Rekisterinpitäjien yhteystiedot`,
  "registry-maintainers-contact-p": `Mikäli sinulla on kysyttävää henkilötietojen käsittelystä Lahjoita
puhetta -kampanjassa tai haluat käyttää rekisteröidyn oikeuksia, ota
yhteyttä osoitteeseen`,
  "registry-keepers-contact-p":
    "Rekisterinpitäjien tietosuojayhteyshenkilöiden tiedot:",
  "registry-keepers-responsibilities-h5":
    "Rekisterinpitäjien vastuut henkilötietojen käsittelyssä",
  "registry-keepers-responsibilities-p-1": `Lahjoita puhetta -kampanjan ja puheen keräämisen ovat suunnitelleet 
yhdessä Helsingin yliopisto, Valtion kehitysyhtiö Recorder Oy (nyk. Ilmastorahasto) 
ja Yleisradio. Toteuttajina olivat vuonna 2020 Helsingin yliopisto, Recorder 
ja Yleisradio, ja helmikuusta 2021 alkaen Helsingin yliopisto ja Yleisradio. 
Nämä tahot ovat yleisen tietosuoja-asetuksen mukaan yhteisrekisterinpitäjiä 
aineiston keräämisen osalta mukanaolonsa ajalta.`,
  "registry-keepers-responsibilities-p-2": `Aineiston tallennuksen ja jakelun osalta Helsingin yliopisto on rekisterinpitäjä. 
Yle vastaa Lahjoita puhetta -sovelluksen julkaisusta ja sovelluksessa käytettävistä 
puhumiseen aktivoivista sisällöistä. Yle vastaa myös sovelluksen käytöstä kerättävän 
teknisen tiedon käsittelystä. Recordern vastuulla oli vuonna 2020 erityisesti Lahjoita 
puhetta -sovelluksen ja -sivuston toteutus yhteistyössä alihankkijansa kanssa. 
Helsingin yliopiston vastuulla on kerätyn aineiston säilyttäminen ja ylläpitäminen, 
luovuttaminen sen hyödyntäjille, kuten tutkijoille ja yrityksille, ja siitä tiedottaminen.`,
  "data-storage-h6": "Kielipankkiin tallennettu aineisto",
  "data-storage-p": `Kampanjan tuottama puheaineisto tallennetaan Helsingin yliopiston
Kielipankkiin, josta aineistoa voidaan luovuttaa edelleen yrityksille ja
muille organisaatioille tekoälyn tutkimusta ja kehitystä, kielen
tutkimusta tai näihin liittyvää korkeakouluopetusta varten. Aineiston
säilytyksestä ja käsittelystä Kielipankissa vastaa rekisterinpitäjänä
Helsingin yliopisto. Jatkossa Helsingin yliopisto voi myös siirtää
puheaineiston kokonaisuudessaan jollekin toiselle organisaatiolle, josta
tulee omalta osaltaan rekisterinpitäjä ja joka voi myös maksua vastaan
myydä aineiston käyttöoikeuksia puhetta ymmärtävien ja tuottavien
sovellusten ja palveluiden kehitykseen.`,
  "data-use-h6": "Aineiston käyttö tekoälykehityksessä ja kielen tutkimuksessa",
  "data-use-p": `Lahjoita puhetta -kampanjassa kerättyä puheaineistoa voivat käyttää
tekoälyn kehitykseen ja tutkimukseen sekä kielentutkimukseen kaupalliset
yritykset ja tekoälykehittäjät sekä tieteellistä tutkimusta tekevät
tutkijat, korkeakoulut ja tutkimuslaitokset. Lisäksi korkeakoulut voivat
käyttää puheaineistoja näihin tarkoituksiin liittyvään opetukseen. Nämä
yritykset tai muut organisaatiot ovat rekisterinpitäjinä vastuussa
omasta tekoälykehityksestään, tutkimuksestaan tai opetuksestaan. Tietoa
siitä, mille vastaanottajille puheaineistoa on luovutettu ja miten ne
käsittelevät aineistoa, tulee olemaan saatavilla osoitteesta`,
  "why-personal-h4": "Miksi henkilötietoja käsitellään?",
  "why-personal-p-1": `Henkilötietoja käsitellään puhetta ymmärtävien ja tuottavien sovellusten
ja palveluiden kehitystä ja tutkimusta sekä kielentutkimusta ja näihin
tarkoituksiin liittyvää korkeakouluopetusta varten.`,
  "why-personal-p-2": `Toimivan puheentunnistuksen kehittäminen edellyttää sitä, että
aineistossa on mukana erilaisia puhujia. Puheen lahjoittajien
taustatiedot ovat tarpeellisia sen varmistamiseksi, että esimerkiksi eri
murrealueet, ikäryhmät ja eri äidinkieliset puhujat ovat aineistossa
riittävästi edustettuina. Lisäksi taustatiedot ovat tärkeitä
kielentutkijoille, sillä niiden avulla on mahdollista esimerkiksi
kohdistaa tutkimus yksittäiseen alueeseen tai ikäryhmään kerrallaan,
tutkia murteita tai vertailla eri-ikäisten ihmisten puheen
ominaisuuksia. Taustatietojen avulla voidaan myös mukauttaa
puhesovelluksia erilaisten ihmisten, esimerkiksi vanhusten, tarpeisiin.`,
  "why-personal-p-3": `Tekniset tiedot, kuten evästeet tai päätelaitetta koskevat tiedot, ovat
tarpeen keräyksen teknistä toteuttamista ja palvelun käytön tilastointia
varten. Lisäksi näillä tiedoilla mahdollistetaan rekisteröityjen
oikeuksien käyttäminen, kuten poisto kielipankin tietokannasta.`,
  "what-personal-info-h4": "Mitä henkilötietoja käsitellään?",
  "what-personal-info-p-1": `Kampanjassa käsiteltäviä tietoja ovat käyttäjän tallentama äänitallenne,
taustakysymyksiin annetut vastaukset, kuten äidinkieli, ikäryhmä,
sukupuoli ja murretausta, äänitallenteelle annettava yksilöllinen
tunniste sekä tallenteeseen liittyviä teknisiä tietoja, kuten äänityksen
tallennusajankohta sekä selaimen ja käyttöjärjestelmän versiot.`,
  "what-personal-info-p-2": `Äänitallenteelle annettava yksilöllinen tunniste ja tekniset tiedot
kerätään selainkäyttöliittymällä. Palvelun kehittämiseen tarvittava
analytiikka hyödyntää evästeitä.`,
  "legal-basis-h4": "Mikä on käsittelyn oikeusperuste?",
  "legal-basis-p-1": `Henkilötietoja käsitellään rekisterinpitäjien ja kolmansien osapuolten
oikeutettujen etujen toteuttamiseksi. Oikeutettu etu on puheaineistojen
kerääminen ja käsittely puhetta ymmärtävien sovelluksien ja palveluiden
kehittämistä ja tutkimusta ja kielentutkimusta sekä niihin liittyvää
opetusta varten. Olemme huolellisesti arvioineet tasapainotestillä, että
voimme käyttää oikeutettua etua perusteena henkilötietojen käsittelylle.
Tietoa tasapainotestistä ja sen huomioista löytyy`,
  "legal-basis-here": "täältä",
  "legal-basis-p-2": ".",
  "personal-info-who-h4":
    "Keitä ovat henkilötietojen vastaanottajat tai vastaanottajaryhmät?",
  "personal-info-who-p-1": `Helsingin yliopisto luovuttaa hankkeessa kerättyjä henkilötietoja 
tässä selosteessa kuvattujen periaatteiden mukaisesti tekoälykehittäjille, 
yrityksille, tutkijoille, tutkimusorganisaatioille tai korkeakouluille 
puheaineiston osana tai yhteydessä.`,
  "ex-eu-h4": "Aiotaanko tietoja siirtää EU:n ulkopuolelle?",
  "ex-eu-p": `Tietoja vastaanottavat toimijat saattavat käsitellä tietoja myös EU:n
tai Euroopan talousalueen ulkopuolella. Tietoja voidaan siirtää Euroopan
talousalueen ulkopuolelle ainoastaan tietosuoja- asetuksen mukaisia
suojatoimia noudattaen. Tällaisia suojatoimia voivat olla esimerkiksi
EU- komission päätös siitä, että vastaanottajamaan tietosuojan taso on
riittävä, tietosuojaa koskevat komission vakiosopimuslausekkeet tai
valvontaviranomaisen vahvistamat yritystä koskevat sitovat säännöt.`,
  "how-long-h4":
    "Kuinka kauan tietoja säilytetään tai millä kriteerillä säilytysaika määrittyy?",
  "how-long-p": `Tietoja säilytetään niin kauan kuin niitä tarvitaan puhetta ymmärtävien
tai tuottavien sovellusten ja palveluiden kehittämiseen tai tutkimukseen
taikka kielentutkimukseen tai näihin tarkoituksiin liittyvään
korkeakouluopetukseen. Rekisterinpitäjät arvioivat viiden vuoden välein
tai useammin, onko aineiston säilyttäminen edelleen tarpeellista, ja
tarpeettomat tiedot poistetaan. Sovelluksen käytöstä kerätyt
käyttäjätiedot poistetaan heti kampanjan päätyttyä. Muutkin tiedot
voidaan poistaa eikä puhetallenteiden tai muiden tietojen säilymistä
luvata.`,
  "your-rights-h4": "Omat oikeutesi",
  "your-rights-p": `Jotta pystyt käyttämään seuraavassa kuvattuja oikeuksiasi, sinun on
pystyttävä kertomaan tunnisteesi
pyynnön yhteydessä tai muuten kyettävä
riittävästi yksilöimään, mistä tiedoista on kysymys. Tallennathan
tunnisteen huolellisesti.`,
  "your-rights-h5-1": "Oikeus saada tietoa ja pääsy tietoihin",
  "your-rights-h5-2": "Oikeus vaatia tietojen korjaamista ja poistamista",
  "your-rights-h5-3": "Suoramarkkinointi ja automaattinen päätöksenteko",
  "your-rights-h5-4": "Oikeus rajoittaa tiedon käsittelyä",
  "your-rights-h5-5": "Oikeus vastustaa tiedon käsittelyä",
  "your-rights-h5-6": "Oikeus tehdä valitus valvontaviranomaiselle",
  "your-rights-p-1": `Sinulla on oikeus saada tietää, käsittelemmekö henkilötietojasi. Jos
käsittelemme henkilötietojasi, sinulla on oikeus saada tietää, mitä
tietojasi käsittelemme.`,
  "your-rights-p-2-1":
    "Sinulla on oikeus vaatia virheellisen tiedon korjaamista ottamalla meihin yhteyttä.",
  "your-rights-p-2-2": `Voit pyytää meitä poistamaan henkilötietosi järjestelmistämme.
Suoritamme pyyntösi mukaiset toimenpiteet, mikäli meillä ei ole
oikeutettua syytä olla poistamatta tietoa. Tiedot eivät välttämättä
poistu välittömästi kaikista varmuuskopio- tai muista vastaavista
järjestelmistämme.`,
  "your-rights-p-3": `Lahjoita puhetta -kampanjassa kerättyjä tietoja ei käytetä
suoramarkkinointiin puheen lahjoittajille eikä puheen lahjoittajia
koskevaan automaattiseen päätöksentekoon.`,
  "your-rights-p-4": `Voit pyytää meitä rajoittamaan tiettyjen henkilötietojesi käsittelyjä.
Tietojen käsittelyn rajoittamista koskeva pyyntö saattaa johtaa
rajoitetumpiin mahdollisuuksiin hyödyntää lahjoittamaasi puhetta
tekoälyn kehittämisessä.`,
  "your-rights-p-5": `Voit henkilökohtaiseen erityiseen tilanteeseesi liittyvällä perusteella
vastustaa henkilötietojesi käsittelyä eli pyytää, että niitä ei
käsiteltäisi ollenkaan. Tällöin lopetamme tietojesi käsittelyn ellemme
voi osoittaa, että käsittelyyn on olemassa huomattavan tärkeä ja
perusteltu syy, joka syrjäyttää sinun etusi, oikeutesi ja vapautesi, tai
käsittely on tarpeen oikeusvaateen laatimiseksi, esittämiseksi tai
puolustamiseksi.`,
  "your-rights-p-6": `Sinulla on oikeus tehdä valitus tietosuojavaltuutetulle, jos katsot,
että henkilötietojesi käsittelyssä rikotaan lakia. Lisätietoja
valitusoikeudesta`,
};

const en_strings = {};

const sv_strings = {
  privacy: "Dataskydd",
  "privacy-p-1":
    "Kampanjen Donera prat är ett samarbete mellan Rundradion Ab (Yle), Helsingfors universitet (HU) och Svenska litteratursällskapet i Finland (SLS). HU och Yle ansvarar gemensamt för insamlingen av talet, Helsingfors universitet är ansvarig instans i fråga om upptagning och utdelning av donerat tal och i fråga om den tekniska information som samlas in om användningen av Yle applikationen. I fortsättningen kan HU överföra talmaterialet i sin helhet till någon annan organisation och materialet kan också ställas till andras förfogande kommersiellt med iakttagande av de regler som anges här.",
  "privacy-p-2": `Talaren kan ha rättigheter enligt upphovsrättslagen eller andra rättigheter till det prat han eller hon donerar. Talaren överlåter dessa rättigheter till Helsingfors universitet och Svenska litteratursällskapet i Finland, i den utsträckning som enligt lag är möjligt och som det är nödvändigt med tanke på utvecklingen av och forskningen eller språkforskningen kring artificiell intelligens som förstår eller producerar tal.`,
  "privacy-p-3":
    "Det är helt frivilligt att donera prat och att uppge sina personuppgifter i kampanjen Donera Prat. Det donerade pratet och andra uppgifter som anknyter till det innehåller talarens personuppgifter. Vid behandlingen av dessa iakttas den finländska dataskyddslagstiftningen, som också de uppgifter som ges på denna sida baserar sig på.",
  "remove-h4": "Radering av det prat som du donerat",
  "remove-p-1":
    "Du kan radera din donation ur databasen genom att sända ett meddelande om att du vill radera din donation till adressen",
  "remove-p-2":
    "I din epost ska du bekräfta din identitet genom att sända koden nedan.",
  "your-code": "Ta tillvara din webbläsarspecifika kod:",
  "clear-browser-h4": "Radering av uppgifter om din donation från webbläsaren",
  "clear-browser-p":
    "Om du använder en gemensam dator t.ex. på ett bibliotek eller du annars vill att den webbläsare du använder inte ska minnas hur många inlägg du har gjort eller de val du har gjort, kan du radera uppgifterna från webbläsaren genom att klicka på ”Radera uppgifterna”. Samtidigt byts din webbläsarspecifika identifikationskod, så ta tillvara din nuvarande identifikationskod innan du tömmer uppgifterna!",
  "clear-browser": "Radera uppgifterna",
  "personal-info-h3": "Information om behandling av personuppgifter",
  "personal-info-p-1":
    "Det material som kampanjen Donera Prat producerar innehåller talarnas personuppgifter. Dessa personuppgifter behandlas i enlighet med den gällande dataskyddslagstiftningen i Finland. Det är helt frivilligt att donera ditt prat och ge dina personuppgifter i kampanjen Donera Prat.",
  "personal-info-p-2":
    "Du har rätt att få veta för vilka ändamål och på vilket sätt vi behandlar dina personuppgifter. Med denna beskrivning strävar vi efter att ge en heltäckande bild av vår dataskyddspraxis när det gäller behandlingen av personuppgifter för det material som uppkommer i kampanjen Donera Prat. Om någon del av denna behandling av personuppgifter ändå förblir oklar, kan du ställa preciserande frågor om behandlingen till oss.",
  "registry-maintainers-h4": "Personuppgiftsansvariga",
  "registry-maintainers-p":
    "Personuppgiftsansvariga är Helsingfors universitet, Rundradion Ab och Svenska litteratursällskapet i Finland rf.",
  "registry-maintainers-contact-h5":
    "Kontaktuppgifter till de personuppgiftsansvariga",
  "registry-maintainers-contact-p":
    "Om du har frågor om behandlingen av personuppgifter i kampanjen Donera Prat eller vill utnyttja de rättigheter du har som registrerad, ta kontakt via adressen på",
  "registry-keepers-contact-p":
    "Kontaktuppgifter till de personuppgiftsansvariga organisationernas ansvarspersoner för dataskydd:",
  "registry-keepers-responsibilities-h5":
    "De personuppgiftsansvarigas ansvar vid behandlingen av personuppgifter",
  "registry-keepers-responsibilities-p-1":
    "Kampanjen Donera Prat och insamlingen av talet har planerats gemensamt av Helsingfors universitet, Yle och Svenska litteratursällskapet i Finland. Dessa aktörer är enligt dataskyddsförordningen gemensamt registeransvariga i fråga om insamling av material under den tid de deltar.",
  "registry-keepers-responsibilities-p-2":
    "När det gäller lagring och distribution av material är Helsingfors universitet och Svenska litteratursällskapet i Finland registeransvariga för det material de arkiverar och distribuerar. Yle ansvarar för publikationen av applikationen Donera Prat och för det innehåll som aktiverar talet och som används i applikationen. Yle svarar också för behandlingen av den tekniska information som samlas in om användningen av applikationen. Helsingfors universitet och Svenska litteratursällskapet ansvarar för förvaring och underhåll av det insamlade materialet, för överlåtelse av materialet till dem som utnyttjar materialet, såsom forskare och företag, och för informationen om detta.",
  "data-storage-h6":
    "Material som lagrats i Språkbanken i Finland eller i SLS arkiv",
  "data-storage-p":
    "Det talmaterial som kampanjen producerar sparas i Språkbanken i Finland vid Helsingfors universitet och i SLS arkiv. Från Språkbanken eller arkivet kan materialet överlåtas vidare till företag och andra organisationer för forskning och utveckling inom artificiell intelligens samt för vetenskaplig forskning, inklusive språkforskning, eller högskoleundervisning i anslutning till denna forskning. Helsingfors universitet svarar som registeransvarig för förvaringen och behandlingen av materialet i Språkbanken.  Svenska litteratursällskapet i Finland svarar som registeransvarig för förvaringen och behandlingen av materialet i SLS arkiv. I fortsättningen kan Helsingfors universitet överföra talmaterialet i sin helhet till någon annan organisation som blir registeransvarig och som också mot avgift kan sälja nyttjanderätter till materialet för utveckling av tillämpningar och tjänster som förstår och producerar talet.",
  "data-use-h6":
    "Användning av material i utveckling av artificiell intelligens och vetenskaplig forskning",
  "data-use-p":
    "Talmaterial som samlats in under kampanjen Donera prat kan användas för utveckling och forskning inom artificiell intelligens samt för språkforskning av kommersiella företag och utvecklare av artificiell intelligens samt av forskare, högskolor och forskningsinstitut som bedriver vetenskaplig forskning. Dessutom kan högskolorna använda talmaterial för undervisning i dessa syften. Dessa företag eller andra organisationer ansvarar i egenskap av registeransvariga för sin egen utveckling av artificiell intelligens, forskning eller undervisning. Information om till vilka mottagare talmaterial har lämnats ut och hur de behandlar materialet kommer att finnas tillgänglig på adressen",
  "why-personal-h4": "Varför behandlas personuppgifter?",
  "why-personal-p-1":
    "Personuppgifter behandlas för utveckling och forskning i tillämpningar och tjänster som förstår och producerar tal samt för vetenskaplig forskning, inklusive språkforskning, och högskoleundervisning i anslutning till denna forskning.",
  "why-personal-p-2":
    "Utvecklandet av en fungerande igenkänning av tal förutsätter att olika talare deltar i materialet. Bakgrundsinformation om talarna behövs för att säkerställa att t.ex. olika dialektområden, åldersgrupper och talare med olika modersmål är tillräckligt representerade i materialet. Dessutom är bakgrundsinformation viktig för vetenskapliga forskare, eftersom den t.ex. gör det möjligt att inrikta forskningen på ett enskilt område eller en enskild åldersgrupp åt gången, forska i dialekter eller jämföra egenskaperna hos tal från personer i olika åldrar. Bakgrundsinformationen gör det också möjligt att anpassa taltillämpningarna till olika människors behov, som t.ex. äldre personer.",
  "why-personal-p-3":
    "Tekniska uppgifter, såsom kakor eller uppgifter om terminalutrustning, behövs för det tekniska genomförandet av insamlingen och för statistikföringen av användningen av tjänsten. Dessa uppgifter gör det dessutom möjligt för de registrerade att utöva sina rättigheter, såsom att radera uppgifter ur språkbankens databas.",
  "what-personal-info-h4": "Vilka personuppgifter behandlas?",
  "what-personal-info-p-1":
    "De uppgifter som behandlas i kampanjen är den ljudupptagning som användaren sparat, svaren på bakgrundsfrågorna, såsom modersmål, åldersgrupp, kön och dialektbakgrund, den unika identifikationskod som ska ges till ljudupptagningen samt tekniska uppgifter som hänför sig till upptagningen, såsom tidpunkten för upptagningen av ljudupptagningen samt versionerna av webbläsaren och operativsystemet.",
  "what-personal-info-p-2":
    "Den unika identifikationskod och de tekniska uppgifter som ska ges till en ljudupptagning samlas in genom en webbläsare. Den analys som behövs för att utveckla tjänsten utnyttjar kakor.",
  "legal-basis-h4":
    "Vilken är den rättsliga behandlingsgrunden för behandlingen av personuppgifter?",
  "legal-basis-p-1":
    "Personuppgifterna behandlas för att tillgodose de personuppgiftsansvarigas och tredje parters berättigade intressen. De berättigade intressena är att samla in och behandla talmaterial för utveckling av tillämpningar och tjänster som förstår tal och för vetenskaplig forskning, inklusive språkforskning, samt högskoleundervisning i anslutning till denna forskning. Med hjälp av ett jämviktstest har vi gjort en bedömning att detta berättigade intresse utgör en rättsligt motiverad behandlingsgrund för behandlingen av personuppgifterna. Information om jämviktstestet och dess kommentarer finns",
  "legal-basis-here": "här",
  "legal-basis-p-2":
    ". Den rättsliga grunden för behandlingen i SLS arkiv är att den utgör i dataskyddslagstiftningen avsett allmännyttigt arkivändamål.",
  "personal-info-who-h4":
    "Till vem eller till vilka grupper överlåts personuppgifter?",
  "personal-info-who-p-1":
    "Helsingfors universitet och/eller Svenska litteratursällskapet i Finland lämnar ut personuppgifter som samlats in inom ramen för projektet i enlighet med de principer som beskrivs i denna beskrivning till utvecklare av artificiell intelligens, företag, forskare, forskningsorganisationer eller högskolor som en del av det insamlade materialet eller i samband med materialet.",
  "ex-eu-h4": "Kommer uppgifterna att överföras till länder utanför EU?",
  "ex-eu-p":
    "De aktörer som tar emot uppgifter kan behandla uppgifterna också utanför EU eller Europeiska ekonomiska samarbetsområdet. Uppgifter får överföras utanför Europeiska ekonomiska samarbetsområdet endast med iakttagande av tillräckliga skyddsåtgärder enligt dataskyddsförordningen. Sådana skyddsåtgärder kan vara t.ex. EU-kommissionens beslut om att mottagarlandets dataskyddsnivå är tillräcklig, kommissionens standardavtalsklausuler om dataskydd eller bindande regler för företag som fastställts av tillsynsmyndigheten.",
  "how-long-h4":
    "Hur länge lagras uppgifterna eller enligt vilket kriterium bestäms förvaringstiden?",
  "how-long-p":
    "Uppgifterna lagras så länge som de behövs för utveckling av tillämpningar och tjänster som förstår eller producerar tal eller för olika slag av vetenskaplig forskning, såsom språkforskning, eller högskoleundervisning som hör samman med denna forskning. De personuppgiftsansvariga ska åtminstone vart femte år bedöma om det fortfarande är nödvändigt att bevara materialet och avlägsna onödiga uppgifter.",
  "your-rights-h4": "Dina rättigheter",
  "your-rights-p":
    "För att kunna utöva de rättigheter som beskrivs nedan, måste du kunna uppge din webbläsarspecifika kod i samband med din begäran eller på annat tillräckligt sätt kunna identifiera vilken information det är fråga. Spara din kod omsorgsfullt.",
  "your-rights-h5-1": "Rätt till information och tillgång till information",
  "your-rights-h5-2": "Oikeus vaatia tietojen korjaamista ja poistamista",
  "your-rights-h5-3": "Direktmarknadsföring och automatiserat beslutsfattande",
  "your-rights-h5-4": "Rätten att begränsa behandlingen av uppgifter",
  "your-rights-h5-5": "Rätten att invända mot behandling av uppgifter",
  "your-rights-h5-6": "Rätt att framföra klagomål till tillsynsmyndigheten",
  "your-rights-p-1":
    "Du har rätt att få veta om vi behandlar dina personuppgifter. Om vi behandlar dina personuppgifter, har du rätt att få veta vilka uppgifter vi behandlar.",
  "your-rights-p-2-1":
    "Du har rätt att begära rättelse av felaktiga uppgifter genom att kontakta oss.",
  "your-rights-p-2-2":
    "Du kan be oss att ta bort din personinformation från våra system. Vi kommer att vidta åtgärder på din begäran, om vi inte har någon berättigad orsak att låta bli att radera informationen. Data raderas inte nödvändigtvis omedelbart från alla våra säkerhetskopior eller liknande system.",
  "your-rights-p-3":
    "Informationen som samlas in genom kampanjen Donera tal används inte för direkt marknadsföring till taldonatorer eller för automatiskt beslutsfattande om taldonatorer.",
  "your-rights-p-4":
    "Du kan be oss begränsa behandlingen av vissa av dina personuppgifter. En begäran om att begränsa behandlingen av uppgifter kan leda till mer begränsade möjligheter att använda talet du donerar för att utveckla artificiell intelligens.",
  "your-rights-p-5":
    "Du kan invända mot behandlingen av dina personuppgifter utifrån din specifika personliga situation, det vill säga begära att de inte behandlas alls. I så fall kommer vi att sluta behandla dina uppgifter om vi inte kan påvisa att det finns en ytterst viktig och välgrundad orsak för behandlingen, som åsidosätter dina intressen, rättigheter och friheter, eller att behandlingen är nödvändig för att fastställa, framlägga eller försvara ett rättsligt anspråk.",
  "your-rights-p-6":
    "Du har rätt att klaga till Dataskyddsombudet om du anser att behandlingen av dina personuppgifter bryter mot lagen. Mer information om överklaganderätten",
};

const langs: Langs = {
  fi: fi_strings,
  en: en_strings,
  sv: sv_strings,
};

const EMAIL_ADDRESS_FI = "lahjoita-puhetta@kielipankki.fi";
const EMAIL_ADDRESS_SV = "doneraprat@kielipankki.fi";

const PrivacyPage: React.FC<PrivacyPageProps> = ({ lang }) => {
  var s = langs[lang];
  var EMAIL_ADDRESS = lang !== "sv" ? EMAIL_ADDRESS_FI : EMAIL_ADDRESS_SV;
  var DATAPROTECTION_URL =
    lang !== "sv"
      ? "https://tietosuoja.fi/onko-tietosuojaoikeuksiasi-loukattu"
      : "https://tietosuoja.fi/sv/har-dina-dataskyddsrattigheter-krankts";
  var registry_keepers_contact =
    lang !== "sv" ? (
      <ul className="mb-4">
        <li>
          Helsingin yliopisto (tietosuojavastaava):
          {"  "}
          <a href="mailto:tietosuoja@helsinki.fi">tietosuoja@helsinki.fi</a>
        </li>
        <li>
          Yleisradio Oy (tietosuojavastaava):
          {"  "}
          <a href="mailto:tietosuoja@yle.fi">tietosuoja@yle.fi</a>
        </li>
        <li>
          Valtion kehitysyhtiö Recorder Oy (nyk. Ilmastorahasto):
          {"  "}
          <a href="mailto:info@ilmastorahasto.fi">info@ilmastorahasto.fi</a>
        </li>
      </ul>
    ) : (
      <ul className="mb-4">
        <li>
          Helsingfors universitet (dataskyddsombud):
          {"  "}
          <a href="mailto:tietosuoja@helsinki.fi">tietosuoja@helsinki.fi</a>
        </li>
        <li>
          Rundradion Ab (dataskyddsombud)::
          {"  "}
          <a href="mailto:tietosuoja@yle.fi">tietosuoja@yle.fi</a>
        </li>
        <li>
          Svenska litteratursällskapet i Finland:
          {"  "}
          <a href="mailto:dataskydd@sls.fi">dataskydd@sls.fi</a>
        </li>
      </ul>
    );
  var personal_info_who_p_2 =
    lang !== "sv" ? (
      <p className="mb-4">
        Helsingin yliopisto käyttää puheaineiston tallennuksessa ja käsittelyssä
        henkilötietojen käsittelijänä CSC – Tieteen tietotekniikan keskus Oy:tä
        {" ("}
        <a href="mailto:asiakaspalvelu@csc.fi">asiakaspalvelu@csc.fi</a>
        {", PL "}
        405, 02101 Espoo). Helsingin yliopisto ja Yle käyttävät yhdessä
        puheaineiston keräämisessä henkilötietojen käsittelijänä Solita Oy:tä
        {" ("}
        <a href="mailto:contact@solita.fi">contact@solita.fi</a>
        {", "}
        Eteläesplanadi 8, 00130 Helsinki). Tietojen keräämisen ja säilytyksen
        teknisessä toteutuksessa käytetään alihankkijoina Googlen Firebase- ja
        Amazon Web Services -palveluja.
      </p>
    ) : (
      <p className="mb-4">
        Vid lagring och behandling av talmaterial använder Helsingfors
        universitet CSC – Tieteen tietotekniikan keskus Oy som
        personuppgiftsbiträde.
        {" ("}
        <a href="mailto:asiakaspalvelu@csc.fi">asiakaspalvelu@csc.fi</a>
        {", PB "}
        405, 02101 Esbo). I det tekniska genomförandet av insamlingen och
        lagringen av uppgifter används Googles Firebase- och Amazon Web
        Services-tjänster som underleverantörer.
      </p>
    );

  const clientId = useSelector(selectClientId);
  const dispatch = useDispatch();

  const clearUserData = () => {
    dispatch(userStateReset());
    dispatch(playlistStateReset());
  };

  return (
    <div className="privacy-page frame--view">
      <h2>{s["privacy"]}</h2>
      <p className="mb-4">{s["privacy-p-1"]}</p>
      <p className="mb-4">{s["privacy-p-2"]}</p>
      <p className="mb-4">{s["privacy-p-3"]}</p>

      <h4>{s["remove-h4"]}</h4>
      <p className="mb-4">
        {s["remove-p-1"]}
        {"  "}
        <a href={`mailto: ${EMAIL_ADDRESS}`}>{EMAIL_ADDRESS}</a>
        {"  "}
        {s["remove-p-2"]}
      </p>
      <p>{s["your-code"]}</p>
      <p className="mb-4">
        <strong>{clientId}</strong>
      </p>

      <h4>{s["clear-browser-h4"]}</h4>
      <p className="mb-4">{s["clear-browser-p"]}</p>
      <PlaylistButton
        className="mb-4"
        buttonType="outline"
        text={s["clear-browser"]}
        onClick={clearUserData}
      />

      <h3 className="mt-5">{s["personal-info-h3"]}</h3>
      <p className="mb-4">{s["personal-info-p-1"]}</p>
      <p className="mb-4">{s["personal-info-p-2"]}</p>

      <h4>{s["registry-maintainers-h4"]}</h4>
      <p className="mb-4">{s["registry-maintainers-p"]}</p>

      <h5>{s["registry-maintainers-contact-h5"]}</h5>
      <p className="mb-4">
        {s["registry-maintainers-contact-p"]}
        {"  "}
        <a href={`mailto: ${EMAIL_ADDRESS}`}>{EMAIL_ADDRESS}</a>.
      </p>

      <p>{s["registry-keepers-contact-p"]}</p>

      {registry_keepers_contact}

      <h5>{s["registry-keepers-responsibilities-h5"]}</h5>

      <p className="mb-4">{s["registry-keepers-responsibilities-p-1"]}</p>

      <p className="mb-4">{s["registry-keepers-responsibilities-p-2"]}</p>

      <h6>{s["data-storage-h6"]}</h6>

      <p className="mb-4">{s["data-storage-p"]}</p>

      <h6>{s["data-use-h6"]}</h6>

      <p className="mb-4">
        {s["data-use-p"]}
        {"  "}
        <a
          href="https://www.kielipankki.fi/lahjoita-puhetta/"
          target="_blank"
          rel="noopener noreferrer"
        >
          https://www.kielipankki.fi/lahjoita-puhetta/
        </a>
        .
      </p>

      <h4>{s["why-personal-h4"]}</h4>
      <p className="mb-4">{s["why-personal-p-1"]}</p>

      <p className="mb-4">{s["why-personal-p-2"]}</p>

      <p className="mb-4">{s["why-personal-p-3"]}</p>

      <h4>{s["what-personal-info-h4"]}</h4>
      <p className="mb-4">{s["what-personal-info-p-1"]}</p>

      <p className="mb-4">{s["what-personal-info-p-2"]}</p>

      <h4>{s["legal-basis-h4"]}</h4>
      <p className="mb-4">
        {s["legal-basis-p-1"]}
        {"  "}
        <a
          href={lang !== "sv" ? balanceTest : balanceTestSv}
          target="_blank"
          rel="noopener noreferrer"
        >
          {s["legal-basis-here"]}
        </a>
        {s["legal-basis-p-2"]}
      </p>

      <h4>{s["personal-info-who-h4"]}</h4>
      <p className="mb-4">{s["personal-info-who-p-1"]}</p>

      {personal_info_who_p_2}

      <h4>{s["ex-eu-h4"]}</h4>
      <p className="mb-4">{s["ex-eu-p"]}</p>

      <h4>{s["how-long-h4"]}</h4>
      <p className="mb-4">{s["how-long-p"]}</p>

      <h4>{s["your-rights-h4"]}</h4>
      <p className="mb-4">{s["your-rights-p"]}</p>

      <h5>{s["your-rights-h5-1"]}</h5>
      <p className="mb-4">{s["your-rights-p-1"]}</p>

      <h5>{s["your-rights-h5-2"]}</h5>
      <p className="mb-4">{s["your-rights-p-2-1"]}</p>

      <p className="mb-4">{s["your-rights-p-2-2"]}</p>

      <h5>{s["your-rights-h5-3"]}</h5>
      <p className="mb-4">{s["your-rights-p-3"]}</p>

      <h5>{s["your-rights-h5-4"]}</h5>
      <p className="mb-4">{s["your-rights-p-4"]}</p>

      <h5>{s["your-rights-h5-5"]}Oikeus vastustaa tiedon käsittelyä</h5>
      <p className="mb-4">{s["your-rights-p-5"]}</p>

      <h5>{s["your-rights-h5-6"]}</h5>
      <p className="mb-4">
        {s["your-rights-p-6"]}
        {": "}
        <a
          href="{DATAPROTECTION_URL}"
          target="_blank"
          rel="noopener noreferrer"
        >
          {DATAPROTECTION_URL}
        </a>
      </p>
    </div>
  );
};

export default PrivacyPage;
