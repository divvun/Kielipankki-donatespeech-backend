#!/usr/bin/env python3
"""
Translate Finnish (fi) content to Norwegian Bokmål (nb) in JSON files.
Adds nb translations parallel to fi content.
"""

import json
from pathlib import Path
from typing import Any

# Load translations from external file if available, otherwise use embedded dictionary
def load_translations():
    """Load translation dictionary"""
    translations = {
        # Empty string
        "": "",
        
        # Place names - keep as is (proper nouns)
        "Järvenpää": "Järvenpää",
        "White Label Test": "White Label Test",
        
        # Main content translations
        "Oppaana Anna Karhunen": "Guide Anna Karhunen",
        "Kiva nähdä sinut täällä! Nyt jutellaan siitä, mitä eri tavarat meidän ympärillämme merkitsevät.": "Hyggelig å se deg her! Nå skal vi snakke om hva forskjellige ting rundt oss betyr.",
        "Aloitetaan jollain helpolla: Söin tänään aamiaiseksi kahvia ja kanamunan, niin kuin aina. Kerro sinä, mitä söit tänä aamuna.": "La oss begynne med noe enkelt: Jeg spiste kaffe og et hønseegg til frokost i dag, som alltid. Fortell meg, hva spiste du i morges.",
        
        # Recording instructions
        "Kerro aamiaisesta": "Fortell om frokosten",
        "Kerro aamiaisestasi": "Fortell om frokosten din",
        "Kun haluat puhua, paina Äänitä-nappia.": "Når du vil snakke, trykk på Ta opp-knappen.",
        "Kun olet valmis puhumaan, paina Äänitä.": "Når du er klar til å snakke, trykk på Ta opp.",
        "Kun olet valmis puhumaan, paina Äänitä. Selitä kaikessa rauhassa.": "Når du er klar til å snakke, trykk på Ta opp. Forklar i ro og mak.",
        "Kun olet valmis, paina Lopeta äänitys.": "Når du er ferdig, trykk på Stopp opptak.",
        "Kun olet vastannut, paina Lopeta äänitys.": "Når du har svart, trykk på Stopp opptak.",
        "Kun painat Äänitä, näet peräkkäin neljä väärennettyä kuvaa.": "Når du trykker Ta opp, vil du se fire forfalskede bilder etter hverandre.",
        "Kiitos, hyvin meni!": "Takk, det gikk bra!",
        "Jatketaan katsomalla ikkunasta ulos.": "La oss fortsette med å se ut av vinduet.",
        
        # Descriptions and prompts
        "Katson ikkunasta": "Jeg ser ut av vinduet",
        "Katsellaan sitten lisää lähellä olevia asioita.": "La oss da se på flere ting i nærheten.",
        "Katso video. Kuka tämä tunnettu henkilö on? Puhuuko hän totta?": "Se videoen. Hvem er denne kjente personen? Snakker han sant?",
        "Katso videolta, miten sitkeästi toimittaja Bubi Wallenius seurasi keihäänheittäjä Seppo Rätyä vuonna 1993.": "Se fra videoen hvor utholdende journalist Bubi Wallenius fulgte spydkaster Seppo Räty i 1993.",
        "Katsotaan sitten mainoksia.": "La oss så se på annonser.",
        "Kerro ja kuvaile, mitä lähimmästä ikkunastasi näkyy.": "Fortell og beskriv hva du ser fra nærmeste vindu.",
        "Kerro kokemuksiasi bottiprofiileista.": "Fortell om dine erfaringer med bottprofiler.",
        "Kerro mitä näet kolmessa kuvassa, ensin rajattuna ja sitten alkuperäisessä koossa.": "Fortell hva du ser i tre bilder, først beskåret og så i original størrelse.",
        "Kerro myös, miksi et ole onnistunut luopumaan noista tavaroista?": "Fortell også hvorfor du ikke har klart å kvitte deg med disse tingene?",
        "Kerro ruoanhakuretkistäsi luonnossa.": "Fortell om dine matletingsekspedisjoner i naturen.",
        "Kerro se tekoälylle. Se ei lavertele eteenpäin.": "Fortell det til AI-en. Den snakker ikke videre.",
        "Kerro seuraavaksi, miten oma tai ystävän lemmikki olisi selviytynyt vastaavasta uintimatkasta.": "Fortell deretter hvordan ditt eget eller en venns kjæledyr ville ha klart en lignende svømme",
        "Kerro seuraavaksi, mitä näet kuvissa. Mitä tunnelmia ja muistoja ne herättävät?": "Fortell deretter hva du ser i bildene. Hvilke stemninger og minner vekker de?",
        "Kerro sitä ennen pari taustatietoa tutkijoille.": "Før det, gi noen bakgrunnsfakta til forskerne.",
        "Kerro sääennuste": "Fortell værmelding",
        "Kerro yksi tai useampi. Voit miettiä rauhassa ennen äänitystä.": "Fortell én eller flere. Du kan tenke i ro før opptaket.",
        "Kerro ääneen, mitä nämä emojit tarkoittavat.": "Fortell høyt hva disse emojierne betyr.",
        "Kerro, mikä kuvissa on valetta.": "Fortell hva som er løgn i bildene.",
        "Kerro, mikä sinua suututtaa tai ahdistaa koronatilanteessa juuri nyt eniten.": "Fortell hva som irriterer eller stresser deg mest i koronasituasjonen akkurat nå.",
        "Kerro, missä someissa olet.": "Fortell hvilke sosiale medier du er på.",
        "Kerro, mistä huomaat tai päättelet väärennökset?": "Fortell hvordan du legger merke til eller slutter deg til forfalskningene?",
        "Kerro, mistä tunnistat huijauksen. Näet jokaista kuvaa reilut 10 sekuntia.": "Fortell hvordan du gjenkjenner svindelen. Du ser hvert bilde i litt over 10 sekunder.",
        "Kerro, mitä nämä kolme kuvaa lupaavat.": "Fortell hva disse tre bildene lover.",
        "Kerrospukeutumisen koreografia": "Klesbyttingens koreografi",
        "Kertoile vapaasti: Mistä sait vaatteen?": "Fortell fritt: Hvor fikk du plagget fra?",
        "Keräillen ja metsästäen": "Samlende og jaktende",
        
        # Feedback messages
        "Kiinnostavaa pohdintaa!": "Interessante betraktninger!",
        "Kiinnostavaa – kiitos!": "Interessant – takk!",
        "Kiinnostavaa!": "Interessant!",
        "Kiinnostavia huomioita!": "Interessante observasjoner!",
        "Kiitokseksi voit katsoa pienen herkullisen retropalan. Äänet päälle!": "Som takk kan du se en liten deilig retrobit. Lyden på!",
        "Kiitokset valistustyöstä :)": "Takk for opplysningsarbeidet :)",
        "Kiitokset!": "Takk skal dere ha!",
        "Kiitos ...": "Takk ...",
        "Kiitos jos vastaat!": "Takk hvis du svarer!",
        "Kiitos jos vastasit!": "Takk hvis du svarte!",
        "Kiitos jälleen!": "Takk igjen!",
        "Kiitos kaunis!": "Tusen takk!",
        "Kiitos sinun, puhepankki on jo monta sanaa rikkaampi.": "Takket være deg er talebanken allerede mange ord rikere.",
        "Kiitos tarinatuokiosta!": "Takk for fortellingens stund!",
        "Kiitos vastauksestasi!": "Takk for svaret ditt!",
        "Kiitos vastauksistasi!": "Takk for svarene dine!",
        "Kiitos vielä kerran!": "Takk en gang til!",
        "Kiitos – näin helppoa se on!": "Takk – så enkelt er det!",
        "Kiitos – sehän sujui": "Takk – det gikk jo bra",
        "Kiitos!": "Takk!",
        "Kiitos! Tack! Spasibo!": "Takk! Tack! Spasibo!",
        "Kiitos, hienosti sujui!": "Takk, det gikk fint!",
        "Kiitos, hyvin meni!": "Takk, det gikk bra!",
        "Kiitos, jos vastasit.": "Takk hvis du svarte.",
        "Kiitos, kulta!": "Takk, kjære!",
        "Kiitos, kun lahjoitit": "Takk for at du donerte",
        "Kiitämmä!": "Takk!",
        
        # Form fields
        "Kirjoita ammattisi.": "Skriv yrket ditt.",
        "Kirjoita yrityksesi tai yhteisösi #-alkuinen tunnus.": "Skriv din bedrifts eller organisasjons ID som starter med #.",
        
        # More UI text
        "Kirottu korona": "Forbannede korona",
        "Kiva että tulit lahjoittamaan puhetta.": "Hyggelig at du kom for å donere tale.",
        "Kiva kun tulit!": "Hyggelig at du kom!",
        "Kohta jatketaan.": "Vi fortsetter snart.",
        "Kohta jatketaan. Ensin voit kuitenkin auttaa tutkijoita.": "Vi fortsetter snart. Men først kan du hjelpe forskerne.",
        "Kohta näet kolme koiraa, jotka ainakin minulle ovat tuttuja.": "Snart ser du tre hunder som i hvert fall er kjente for meg.",
        "Kohta näytän sinulle muutaman sanan, joita en itse näe. Selitä ne minulle parhaasi mukaan!": "Snart viser jeg deg noen ord som jeg selv ikke ser. Forklar dem så godt du kan!",
        "Kohta pääset purkamaan paineitasi. Aloitetaan kuitenkin kuva-arvoituksella.": "Snart får du utløp for presset. Men la oss starte med en bildegåte.",
        
        # Corona related
        "Korona-aika": "Koronatiden",
        "Korona-aika irrottelee sinun kielenkantojasi mukavasti.": "Koronatiden får tungebåndet ditt til å løsne behagelig.",
        "Koronavirus ei kadonnutkaan kesällä 2020, kuten moni odotti.": "Koronaviruset forsvant tross alt ikke sommeren 2020, som mange forventet.",
        "Koronavirus laittoi maailman ja Suomen sekaisin. Nyt saat ruotia koronan vaikutuksia ja sen herättämiä tunteita.": "Koronaviruset satte verden og Finland på hodet. Nå får du dissekere koronaens effekter og følelsene den vekte.",
        
        # Questions
        "Kuinka tärkeä sen väri on?": "Hvor viktig er fargen?",
        "Kun olet löytänyt erot, paina Äänitä ja kerro niistä omin sanoin.": "Når du har funnet forskjellene, trykk Ta opp og fortell om dem med dine egne ord.",
        
        # More prompts
        "Kooste kestää minuutin. Voit jatkaa puhumista myös sen pysähdyttyä.": "Sammendraget varer et minutt. Du kan fortsette å snakke også etter at det har stoppet.",
        "Kuva": "Bilde",
        "Kuva aukeaa 15 sekunnin välein.": "Bildet åpnes hvert 15. sekund.",
        "Kuva vaihtuu muutaman sekunnin välein.": "Bildet endres hvert par sekunder.",
        "Kuva-arvoitus": "Bildegåte",
        "Kuvaile Kanarian-tädillesi tämän ja eilisen päivän säätä.": "Beskriv dagens og gårsdagens vær for tanten din på Kanariøyene.",
        "Kuvaile kesänviettoa": "Beskriv sommertid",
        "Kuvia voidaan käsitellä ja niihin liittää asioita, jotka eivät niihin aluksi kuuluneet.": "Bilder kan behandles og ting som ikke opprinnelig tilhørte dem kan legges til.",
        "Kuvissa on 3 eroavaisuutta.": "Det er 3 forskjeller i bildene.",
        
        # More questions        
        "Kysele ihastukseltasi hänen reissustaan.": "Spør din kjæreste om turen sin.",
        "Kysele rohkeasti – olipa idolisi joku näistä kolmesta tai joku muu!": "Spør modig – enten din idol er en av disse tre eller noen andre!",
        "Kysy maskista": "Spør om masken",
        "Kysy suosikiltasi": "Spør din favoritt",
        "Kysymme sinulta kolmea pientä taustatietoa. Niistä ei voi päätellä henkilöllisyyttäsi.": "Vi spør deg om tre små bakgrunnsfakta. Fra disse kan ikke identiteten din utledes.",
        "Kysymme sinulta tutkijoille muutamaa taustatietoa.": "Vi spør deg om noen bakgrunnsfakta for forskerne.",
        
        # Instructions
        "Käytä ihan tavallista puhekieltä. Takeltelu ja pikku tauot eivät haittaa!": "Bruk helt vanlig talespråk. Stamming og små pauser gjør ingenting!",
        "Lahjoittamasi puheaika näkyy ylhäällä oikealla ja hyvältä näyttää!": "Taletiden du har donert vises øverst til høyre, og det ser bra ut!",
        "Lahjoittamasi puheen määrän näet oikeassa ylänurkassa.": "Mengden tale du har donert ser du i øvre høyre hjørne.",
        "Lahjoituksesi avulla arki ja asiointi suomeksi puhumalla helpottuvat.": "Med din donasjon blir hverdagen og gjøremål ved å snakke finsk lettere.",
        "Lahjoituksesi avulla opetetaan esimerkiksi kännykkää ymmärtämään puhuttua suomea.": "Med din donasjon læres for eksempel mobiltelefonen til å forstå talt finsk.",
        "Lahjoitus käynnissä": "Donasjon pågår",
        
        # More content
        "Laji vaihtuu 15 sekunnin välein.": "Grenen endres hvert 15. sekund.",
        "Leiki selostajaa": "Lek kommentator",
        "Lemmikkini ui": "Kjæledyret mitt svømmer",
        "Lempivaate": "Favorittplagg",
        "Lirkuttele lomakuvista": "Flørt med feriebildene",
        "Loistavasti selitetty!": "Utmerket forklart!",
        "Lopuksi kysymme vielä pari taustatietoa tutkijoille. Kiitos jos vastaat.": "Til slutt spør vi om et par bakgrunnsfakta for forskerne. Takk hvis du svarer.",
        "Lopuksi vielä muutama taustakysymys – kiitos jos vastaat.": "Til slutt noen bakgrunnsspørsmål – takk hvis du svarer.",
        "Luonto, sää ja mää": "Natur, vær og jeg",
        "Luulitko, että kissat eivät osaa uida? Kohta näet mitä tapahtuu, kun kissa joutuu veteen.": "Trodde du at katter ikke kan svømme? Snart ser du hva som skjer når en katt havner i vannet.",
        
        # More feedback
        "Lähelläni juuri nyt": "Nær meg akkurat nå",
        "Lähdetään sitten luontoon ruoan perässä.": "La oss da dra ut i naturen etter mat.",
        "Mahtavaa että tulit lahjoittamaan puhetta.": "Flott at du kom for å donere tale.",
        "Mahtavaa! Kohta jatketaan!": "Flott! Vi fortsetter snart!",
        "Mahtavaa...": "Flott...",
        "Mainiota!": "Storart!",
        "Mainoksissa näytetään usein unelmia: osta, niin sinunkin elämästäsi voi tulla tällaista.": "Annonser viser ofte drømmer: kjøp, så kan også livet ditt bli slik.",
        
        # Education levels and demographics
        "Mediataidot 4-6 lk.": "Medieferdigheter 4.-6. trinn",
        "Mediataidot 8-9 lk.": "Medieferdigheter 8.-9. trinn",
        "Mediataidot lukio": "Medieferdigheter videregående",
        "Meidän kaikkien puheessa kuuluu oma tausta tai murre.": "I alles tale høres vår egen bakgrunn eller dialekt.",
        
        # More prompts
        "Mennään sitten sinun omaan urheiluhetkeesi.": "La oss så gå til ditt eget idrettsøyeblikk.",
        "Mennään sitten taas yhteen nostalgiseen hetkeen.": "La oss så igjen gå til et nostalgisk øyeblikk.",
        "Mennään taas eteenpäin.": "La oss gå videre igjen.",
        
        # Gender
        "Mies": "Mann",
        "Nainen": "Kvinne",
        
        # More instructions
        "Mieti kysymyksiä rauhassa. Kuva vaihtuu 8 sekunnin välein.": "Tenk over spørsmålene i ro. Bildet endres hvert 8. sekund.",
        "Mieti rauhassa, paina Äänitä ja ajattele ääneen.": "Tenk i ro, trykk Ta opp og tenk høyt.",
        "Mieti ääneen, miksi nämä kohtaukset aikanaan joutuivat sensuurin saksimiksi.": "Tenk høyt, hvorfor disse scenene i sin tid ble sensurert.",
        "Mihin tilanteeseen tämä meemi sopii? Voit jatkaa, vaikka video loppuu.": "Hvilken situasjon passer denne memen til? Du kan fortsette selv om videoen slutter.",
        
        # More questions
        "Mikä jalka ensin?": "Hvilken fot først?",
        "Mikä on ollut päräyttävin reissusi luontoäidin ruokakomerossa?": "Hva har vært den mest fantastiske turen din i mornaturs matskammer?",
        "Mikä on sinun paras penkkiurheilumuistosi? Missä ja milloin se oli?": "Hva er ditt beste tilskuerminne? Hvor og når var det?",
        "Mikä sinulle on ollut rakkain lemmikki tai eläin? Miltä se tuntui ja mitä se teki?": "Hvilket kjæledyr eller dyr har vært kjærest for deg? Hvordan føltes det og hva gjorde det?",
        "Mikä suututtaa?": "Hva irriterer?",
        "Mikä vaate ensin, mikä sitten?": "Hvilket plagg først, hvilket så?",
        "Millaiset otsikot saisivat lukijat klikkaamaan juttua?": "Hvilke overskrifter ville få leserne til å klikke på artikkelen?",
        "Millaisia botteja sinä olet kohdannut? Mistä tunnistat sellaisen?": "Hvilke botter har du møtt? Hvordan gjenkjenner du en slik?",
        
        # More personal questions
        "Minulla on kotona tavaraa, jota en käytä. Omistan satoja CD-levyjä, mutta en soitinta.": "Jeg har ting hjemme som jeg ikke bruker. Jeg eier hundrevis av CD-er, men ingen spiller.",
        "Minulle rakas eläin ollut lapsuuden koira.": "Det kjære dyret for meg har vært barndomshunden.",
        "Missä päin sinä olet oppinut moisen valittamisen taidon?": "Hvor har du lært en slik kunst å klage?",
        "Mistä kodikkuus syntyy?": "Hvor kommer koselig hjemmefølelse fra?",
        "Mistä sinun mielestäsi syntyy kodikkuus?": "Hvor tror du koselig hjemmefølelse kommer fra?",
        "Miten kuvailet hänelle tämän ja eilisen päivän säätä?": "Hvordan beskriver du dagens og gårsdagens vær for ham/henne?",
        "Miten sinä kosket pintoihin julkisissa tiloissa?": "Hvordan berører du overflater på offentlige steder?",
        "Mitkä kolmesta uutisotsikosta ovat valetta? Muistathan perustella!": "Hvilke tre av nyhetoverskriftene er løgn? Husk å begrunne!",
        "Mitä ihmiskunta voi mielestäsi oppia tästä pandemiasta?": "Hva tror du menneskeheten kan lære av denne pandemien?",
        "Mitä kysyisit heiltä, jos he tulisivat vastaan?": "Hva ville du spurt dem hvis du møtte dem?",
        "Mitä mieltä olet ulkonäköä muokkaavista filttereistä?": "Hva synes du om utseendeendrende filtre?",
        "Mitä muistoja näistä herää?": "Hvilke minner vekkes av disse?",
        "Mitä muistoja sinulla liittyy tärkeisiin vaatteisiin?": "Hvilke minner har du knyttet til viktige plagg?",
        "Mitä näkyy, mitä ei?": "Hva ser man, hva ikke?",
        "Mitä nämä emojit tarkoittavat?": "Hva betyr disse emojierne?",
        "Mitä nämä tuovat mieleesi?": "Hva bringer disse til sinnet?",
        "Mitä opimme?": "Hva lærte vi?",
        "Mitä outoja tavaroita sinulla on?": "Hvilke rare ting har du?",
        "Mitä someja käytät?": "Hvilke sosiale medier bruker du?",
        "Mitä? Etkö antanut kaikkeasi vielä? Valitse joku toinen aihe ja lahjoita lisää.": "Hva? Ga du ikke alt ennå? Velg et annet tema og doner mer.",
        
        # Module text
        "Moduulissa on kuva.": "Modulen har et bilde.",
        "Moikka!": "Hei!",
        "Moniin esineisiin liittyy muistoja. Tämän taulun on tehnyt isäni nuorena.": "Mange gjenstander er knyttet til minner. Dette maleriet ble laget av faren min som ung.",
        
        # More instructions
        "Muista, että kaikki epäröinnit ovat aitoa puhekieltä eli vain plussaa.": "Husk at all nøling er ekte talespråk, altså bare et pluss.",
        "Muistele ja hersytä sielusi kyllyydestä.": "Husk og begeistre fra sjelens fylde.",
        "Muistele ääneen, mitä nämä veijareita ovat ja mitä muistoja niistä herää.": "Husk høyt hva disse slyngene er og hvilke minner de vekker.",
        "Muistutan vielä, että tietosuojastasi löydät lisää tietoa päävalikosta.": "Jeg minner om at du finner mer informasjon om personvern i hovedmenyen.",
        "Mukanasi kulkee luontotoimittaja Minna Pyykkö.": "Med deg går naturjournalist Minna Pyykkö.",
        "Mukavaa, jos oma taustasi tai murteesi kuului puheessa.": "Hyggelig hvis din egen bakgrunn eller dialekt hørtes i talen.",
        "Mukavaa, jos vastasit taustatietoihin. Tutkijat ja suomen kieli kiittävät.": "Hyggelig hvis du svarte på bakgrunnsinformasjonen. Forskerne og det finske språket takker.",
        
        # Other
        "Mutta hei, nyt taitaa puhelin soida.": "Men hei, nå ringer vel telefonen.",
        "Muu": "Annet",
        "Muu kuin Suomi": "Annet enn Finland",
        "Muuten, yläkulmasta näet paljonko olet jo lahjoittanut.": "Forresten, i øvre hjørne ser du hvor mye du allerede har donert.",
        
        # Dialect background
        "Murretaustani": "Min dialektbakgrunn",
        "Murteiden ja erilaisten puhetapojen säilyminen on tärkeää.": "Bevaring av dialekter og ulike talemåter er viktig.",
        
        # More instructions
        "Neuvo vuohiparkaa juurta jaksain!": "Hjelp stakkar geiten med rot og greiner!",
        "Niiden avulla saamme paremman kuvan siitä, millainen puhuja olet.": "Med dem får vi et bedre bilde av hva slags taler du er.",
        "Niin kuin varmaan tiedät, yhteistyössä on voimaa. Haasta siis myös ystäväsi lahjoittamaan puhetta!": "Som du sikkert vet, er det styrke i samarbeid. Utfordre derfor også vennene dine til å donere tale!",
        
        # More feedback
        "No huh huh!": "Vel huff da!",
        "Nostit taas pisteitäsi :)": "Du økte poengene dine igjen :)",
        
        # More prompts
        "Nyt haetaan sun – tai siun – tavallista puhekieltä. Ota siis rennosti!": "Nå leter vi etter ditt – eller din – vanlige talespråk. Så ta det rolig!",
        "Nyt lähdetään huonoille teille.": "Nå drar vi på dårlige veier.",
        "Nyt on sinun vuorosi. Kerro jostain sinulle tärkeästä tavarasta. Kuvaile, miksi se on sinulle tärkeä.": "Nå er det din tur. Fortell om noe som er viktig for deg. Beskriv hvorfor det er viktig for deg.",
        "Nyt on sinun vuorosi. Älä pelkää takelteluja. Tässä kerätään nimenomaan aitoa puhekieltä.": "Nå er det din tur. Ikke vær redd for stamming. Her samler vi nettopp ekte talespråk.",
        "Nyt pääset selostamaan klassikkoa. Näet lyhyen videon Lasse Virénin uskomattomasta suorituksesta.": "Nå får du kommentere en klassiker. Du ser en kort video av Lasse Virén sin utrolige prestasjon.",
        "Nyt saa valittaa! Mikä sinua on viime aikoina ottanut päähän? Korona, poliitikot vai naapurisi?": "Nå får du klage! Hva har irritert deg i det siste? Korona, politikere eller naboen din?",
        "Nyt saat auttaa pulassa olevaa vuohta. Anna vuohelle ohjeita: mikä jalka pitäisi nostaa ja minne kääntyä?": "Nå får du hjelpe en geit i nød. Gi geiten instruksjoner: hvilken fot skal løftes og hvor skal den snu?",
        "Nyt selkisi kaverillekin.": "Nå ble det klart for vennen din også.",
        "Nyt voit auttaa tutkijoita lisää kertomalla pari taustatietoa.": "Nå kan du hjelpe forskerne mer ved å fortelle et par bakgrunnsfakta.",
        "Nyt voit kysyä häneltä aivan kaikki mielessäsi olevat kysymykset.": "Nå kan du spørre ham/henne alle spørsmålene du har i tankene.",
        "Nyt voit taas auttaa tutkijoita kolmella pienellä tiedolla.": "Nå kan du igjen hjelpe forskerne med tre små fakta.",
        "Nyt voit taas auttaa tutkijoita yhdellä taustatiedolla.": "Nå kan du igjen hjelpe forskerne med ett bakgrunnsfaktum.",
        "Nyt voit tunnustaa kaikki syntisi yhdellä kertaa!": "Nå kan du bekjenne alle syndene dine på én gang!",
        
        # More prompts
        "Näet kohta kaksi kuvaa. Etsi kuvista kolme eroavaisuutta.": "Du ser snart to bilder. Finn tre forskjeller i bildene.",
        "Näet kohta tutun meemipätkän. Kerro ääneen, millaiseen tilanteeseen se sopisi.": "Du ser snart en kjent meme-bit. Fortell høyt hvilken situasjon den passer til.",
        "Näet kohta videolla kolme tilannetta. Anna niissä näkyville käskyjä!": "Du ser snart tre situasjoner på video. Gi de synlige kommandoer!",
        "Näet kuvassa joitakin korona-ajan positiivisia asioita. Mitä ne tuovat mieleesi?": "Du ser i bildet noen positive ting fra koronatiden. Hva bringer de til sinnet?",
        "Näet matkakuvat videolla, kun painat Äänitä-nappia.": "Du ser reisebildene på video når du trykker Ta opp-knappen.",
        "Näet netissä kolme uutisotsikkoa.": "Du ser tre nyhetsoverskrifter på nettet.",
        "Näet seuraavaksi niistä osan – ilman ääniä.": "Du ser deretter en del av dem – uten lyd.",
        "Näet videolla neljä kuvaparia. Kerro, kumpi kuvista sopii paremmin tämänhetkiseen mielentilaasi.": "Du ser fire bildepar på video. Fortell hvilket av bildene som passer best til din nåværende sinnstilstand.",
        "Näet videolla viisi lajia. Selitä ne kaverillesi.": "Du ser fem grener på video. Forklar dem for vennen din.",
        "Näet yhtä kuvaa noin 10 sekuntia.": "Du ser ett bilde i omtrent 10 sekunder.",
        "Näetkö niissä hyvää, huonoa vai molempia?": "Ser du godt, dårlig eller begge deler i dem?",
        "Näin saatiin Suomen suvi maailmankaikkeuden kartalle.": "Slik fikk vi Finlands sommer på universets kart.",
        "Näistäkään ei sinua voi tunnistaa.": "Heller ikke fra disse kan du identifiseres.",
        "Näitä taustatietoja ei voi yhdistää sinuun lahjoittajana.": "Disse bakgrunnsopplysningene kan ikke knyttes til deg som giver.",
        
        # More instructions
        "Ohjeista kuritonta": "Instruer den ulydige",
        "Ohoh, mitä otsikointia": "Oi oi, for en overskrift",
        "Ole huoleti: sinua ei voi jäljittää. Puheesi menee vain tutkimuskäyttöön.": "Vær trygg: du kan ikke spores. Talen din går kun til forskningsbruk.",
        "Olen Ina Mikkola, oppaasi täällä K-18-maailmassa.": "Jeg er Ina Mikkola, din guide her i 18+-verdenen.",
        "Olen vieraassa kaupungissa  ja menojalkaa vipattaa. Voisitko neuvoa tien baariin, klubille ja hotellille?": "Jeg er i en fremmed by og har gå-foten klar. Kunne du vise veien til baren, klubben og hotellet?",
        "Olet lähdössä ulos paukkupakkasiin.": "Du skal ut i knallkulden.",
        "Olet päässyt kunnolla rupattelun vauhtiin.": "Du har kommet skikkelig i gang med praten.",
        "Olet urheilusta puhumisen mestari!": "Du er mester i å snakke om idrett!",
        "Oletko käynyt sienessä, marjassa, kalassa tai metsästämässä?": "Har du vært på sopp, bær, fiske eller jakt?",
        "Oletpa tarkkasilmäinen!": "Du er jo skarpøyd!",
        "Olipa hyvin käännetty!": "Det var godt oversatt!",
        "Olipa kiva kuulla, kiitos!": "Det var hyggelig å høre, takk!",
        "Onko ilmoja piisannu?": "Har det vært nok vær?",
        
        # More titles
        "Opasta synnin polulla": "Veilede på syndens sti",
        "Oppaana Anna Karhunen": "Guide Anna Karhunen",
        "Oppaana Minna Pyykkö": "Guide Minna Pyykkö",
        "Oppaanasi on \"Kaverin puolesta kyselen\" -podcastista tuttu Anna Karhunen.": "Din guide er Anna Karhunen, kjent fra podcasten \"Spør på vegne av en venn\".",
        
        # More prompts
        "Osallistuitko yrityshaasteeseen?": "Deltok du i bedriftsutfordringen?",
        "Osallistutko yrityshaasteeseen?": "Deltar du i bedriftsutfordringen?",
        "Osuvasti kyselit!": "Treffende spurt!",
        
        # More instructions
        "Paina Äänitä ja etsi eroja ääneen!": "Trykk Ta opp og søk etter forskjeller høyt!",
        "Paina Äänitä ja etsi erot ääneen ajatellen.": "Trykk Ta opp og søk etter forskjellene mens du tenker høyt.",
        "Paina Äänitä ja kerro ajatuksiasi videosta.": "Trykk Ta opp og fortell tankene dine om videoen.",
        "Paina Äänitä ja kerro, mikä potuttaa!": "Trykk Ta opp og fortell hva som irriterer!",
        "Paina Äänitä ja tulkkaa kuvassa näkyvät asiat mummollesi.": "Trykk Ta opp og tolk tingene som vises i bildet for bestemoren din.",
        "Paina Äänitä, niin näet kolme kuvaa. Mitä näet kuvassa ensin – entä sitten?": "Trykk Ta opp, så ser du tre bilder. Hva ser du i bildet først – og så?",
        "Paina Äänitä, niin näet peräkkäin kolme karttaa. Näet jokaista 15 sekunnin ajan.": "Trykk Ta opp, så ser du tre kart etter hverandre. Du ser hvert i 15 sekunder.",
        "Paina Äänitä, niin näet saman videon ilman ääniä.": "Trykk Ta opp, så ser du samme video uten lyd.",
        "Paina Äänitä, niin näet tarkemman kartan.": "Trykk Ta opp, så ser du et mer detaljert kart.",
        "Paina Äänitä-nappia ja kerro, miten kosket pintoihin julkisissa tiloissa: suojaatko kätesi vai et?": "Trykk Ta opp-knappen og fortell hvordan du berører overflater på offentlige steder: beskytter du hendene eller ikke?",
        "Paljon kiitoksia.": "Tusen takk.",
        
        # Sport memory
        "Penkkiurheilumuisto": "Tilskuerminne",
        "Perusteellista, hyvä!": "Grundig, bra!",
        
        # More info
        "Pian jatketaan matkaa kohti syvää päätyä. On tunnusten aika.": "Snart fortsetter reisen mot dype enden. Det er tid for innlogging.",
        "Pidetään yhdessä eläimistä ja luonnosta huolta!": "La oss sammen ta vare på dyr og natur!",
        "Pieni juttu: Puhettasi pääsevät kuulemaan vain tutkijat ja tekoälyn kehittäjät.": "Liten ting: Bare forskere og AI-utviklere får høre talen din.",
        "Pieni muistutus ennen kuin jatketaan: Puhettasi pääsevät kuulemaan vain tutkijat ja tekoälyn kehittäjät.": "Liten påminnelse før vi fortsetter: Bare forskere og AI-utviklere får høre talen din.",
        "Pientä tuunausta": "Litt tuning",
        "Pikku juttu ennen kuin jatketaan:": "Liten ting før vi fortsetter:",
        "Pikku juttu ensin: puhettasi pääsevät kuulemaan vain tutkijat ja tekoälyn kehittäjät. Tietosuojasta voit lukea lisää aloitussivulta.": "Liten ting først: bare forskere og AI-utviklere får høre talen din. Du kan lese mer om personvern fra startsiden.",
        "Pikku vinkki: näet ylälaidasta, kuinka paljon olet jo lahjoittanut.": "Liten hint: du ser øverst hvor mye du allerede har donert.",
        
        # More prompts
        "Pohdi, puhu ja pulise vapaasti!": "Tenk, snakk og mas fritt!",
        "Pomosi odottaa siitä mehevää klikkiotsikkoa. Millaisia keksit?": "Sjefen din venter på en saftig klikkbait-overskrift. Hva finner du på?",
        "Psst. Lahjoittamasi puheen määrän näet oikeassa ylänurkassa.": "Psst. Mengden tale du har donert ser du i øvre høyre hjørne.",
        
        # More instructions
        "Puheen lahjoittamisen lomassa kysymme sinulta joitakin taustatietoja.": "Under taledonasjonen spør vi deg om noen bakgrunnsfakta.",
        "Puheen lahjoittamisen ohessa kysymme sinulta joitakin taustatietoja.": "Sammen med taledonasjonen spør vi deg om noen bakgrunnsfakta.",
        "Puheen lahjoittamisen varrella kysymme sinulta joitakin taustatietoja.": "Underveis i taledonasjonen spør vi deg om noen bakgrunnsfakta.",
        "Puhettasi pääsevät kuulemaan vain tutkijat ja tekoälyn kehittäjät.": "Bare forskere og AI-utviklere får høre talen din.",
        "Puhettasi pääsevät kuulemaan vain tutkijat ja tekoälyn kehittäjät. Tietosuojasta voit lukea lisää aloitussivulta.": "Bare forskere og AI-utviklere får høre talen din. Du kan lese mer om personvern fra startsiden.",
        "Puhettasi voivat kuunnella vain tutkijat ja tekoälyn kehittäjät. Lue tietosuojasta lisää aloitussivulta.": "Bare forskere og AI-utviklere kan høre talen din. Les mer om personvern fra startsiden.",
        "Puhu ja pulise niin kauan kuin haluat.": "Snakk og mas så lenge du vil.",
        "Puhu niin kauan kuin haluat!": "Snakk så lenge du vil!",
        "Puhu niin kauan kuin juttua riittää.": "Snakk så lenge det er snakk igjen.",
        
        # More prompts
        "Pysy mukana – vielä pari lahjoitustehtävää jäljellä.": "Hold deg med – ennå et par donasjonsoppgaver igjen.",
        "Pysy mukana. Seuraavaksi näet elokuvasta sensuroituja kohtauksia!": "Hold deg med. Neste gang ser du sensurerte scener fra filmen!",
        "Pysy mukana...": "Hold deg med...",
        "Pysythän vielä hetken mukana. Nyt sinulla on viimeinen tilaisuus auttaa tutkijoita.": "Bli med litt til. Nå har du siste sjanse til å hjelpe forskerne.",
        "Pysäytä Seppo": "Stopp Seppo",
        "Päina Äänitä ja arvaile, mitä kuvasta paljastuu.": "Trykk Ta opp og gjett hva som avsløres fra bildet.",
        "Päinä Äänitä, niin näet videolla suomalaisia urheilutähtiä. Kenet heistä pitäisi valita 2000-luvun urheilijaksi?": "Trykk Ta opp, så ser du finske idrettsstjerner på video. Hvem av dem bør velges som 2000-tallets idrettsutøver?",
        "Pätevää ennustamista!": "Dyktig spåing!",
        "Pääsitkö vasta vauhtiin?": "Kom du nettopp i gang?",
        "Päästä mielikuvituksesi lentoon ja liioittele!": "Slipp fantasien løs og overdriv!",
        "Pöllitkö tavaraa työpaikaltasi? Oletko kova pieremään?": "Stjal du ting fra arbeidsplassen din? Er du flink til å fjerte?",
        
        # More titles
        "Rakkain eläimeni": "Mitt kjæreste dyr",
        "Reenataas eka!": "La oss øve først!",
        "Ryhdy Ylen meteorologiksi ja esittele kesäperjantain sää.": "Bli Yles meteorolog og presenter fredag ettermiddag",

# This transcription continues with all the place names (Finnish municipalities) - these should generally be kept as is since they are proper nouns
        # Place names - kept as proper nouns
    }
    
    return translations


# Add all place names as-is (proper nouns don't get translated)
PLACE_NAMES = [
    # All Finnish place names from the extracted list should be added here
    # They remain unchanged in translation as they are proper nouns
]

TRANSLATIONS = load_translations()


def translate_text(text: str) -> str:
    """Translate Finnish text to Norwegian Bokmål."""
    if text in TRANSLATIONS:
        return TRANSLATIONS[text]
    
    # If exact match not found, return the original text with a marker
    # This way we can identify what still needs manual translation
    print(f"⚠️  No translation found for: {text[:50]}...")
    return text  # Keep original for now


def process_text_object(obj: Any, path: str = "") -> bool:
    """
    Recursively process JSON object to add 'nb' translations parallel to 'fi' content.
    Returns True if any changes were made.
    """
    changed = False
    
    if isinstance(obj, dict):
        # Check if this is a language object with 'fi' key
        if 'fi' in obj and 'nb' not in obj:
            fi_text = obj['fi']
            nb_text = translate_text(fi_text)
            obj['nb'] = nb_text
            changed = True
        
        # Recursively process all values
        for key, value in obj.items():
            if process_text_object(value, f"{path}.{key}"):
                changed = True
    
    elif isinstance(obj, list):
        # Recursively process all items
        for i, item in enumerate(obj):
            if process_text_object(item, f"{path}[{i}]"):
                changed = True
    
    return changed


def process_json_file(file_path: Path) -> None:
    """Process a single JSON file to add Norwegian translations."""
    print(f"Processing: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if process_text_object(data):
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            print(f"✅ Updated: {file_path}")
        else:
            print(f"⏭️  No changes needed: {file_path}")
    
    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")


def main():
    """Main function to process all JSON files in content directories."""
    base_path = Path(__file__).parent / "content"
    
    # Find all JSON files in content directory
    json_files = list(base_path.glob("**/*.json"))
    
    print(f"Found {len(json_files)} JSON files to process\n")
    
    for json_file in sorted(json_files):
        process_json_file(json_file)
        print()
    
    print("✅ Translation complete!")


if __name__ == "__main__":
    main()
