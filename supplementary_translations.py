#!/usr/bin/env python3
"""
Add supplementary translations for missing strings.
This script adds translations for common UI elements, form labels, and keeps place names as-is.
"""

# Supplementary translations to add to the main dictionary
SUPPLEMENTARY_TRANSLATIONS = {
    # Age ranges
    "1-10 vuotta": "1-10 år",
    "11-20 vuotta": "11-20 år",
    "21-30 vuotta": "21-30 år",
    "31-40 vuotta": "31-40 år",
    "41-50 vuotta": "41-50 år",
    "51-60 vuotta": "51-60 år",
    "61-70 vuotta": "61-70 år",
    "71-80 vuotta": "71-80 år",
    "81-90 vuotta": "81-90 år",
    "91-100 vuotta": "91-100 år",
    "101+ vuotta": "101+ år",
    "Ikäni": "Min alder",
    "Valitse valikosta ikäryhmäsi.": "Velg aldersgruppen din fra menyen.",
    
    # Languages
    "suomi": "finsk",
    "ruotsi": "svensk",
    "venäjä": "russisk",
    "viro (eesti)": "estisk",
    "arabia": "arabisk",
    "somali": "somali",
    "englanti": "engelsk",
    "kurdi": "kurdisk",
    "persia (farsi)": "persisk (farsi)",
    "muu kieli": "annet språk",
    "Jokin muu kieli": "Et annet språk",
    "Jos valitsit Muu kieli, kirjoita sen nimi:": "Hvis du valgte Annet språk, skriv itssnavn:",
    "Äidinkieleni": "Mitt morsmål",
    "Jos sinulla on lapsesta asti ollut kaksi äidinkieltä, valitse molemmat. Tai valitse se, jolla puhut useammin.": "Hvis du har hatt to morsmål fra barndommen, velg begge. Eller velg det du snakker oftest.",
    "Ihanaa, että tänne kertyy puhetta suomea äidinkielenään puhuvalta.": "Flott at det samles tale fra noen som har finsk som morsmål.",
    
    # Education
    "peruskoulu (tai vastaava)": "grunnskole (eller tilsvarende)",
    "ammatillinen koulutus tai lukio": "yrkesopplæring eller videregående",
    "korkeakoulu": "høyskole/universitet",
    "Koulutustaustani": "Min utdanningsbakgrunn",
    
    # Gender and personal info
    "En halua kertoa": "Jeg ønsker ikke å oppgi",
    "Sukupuoleni": "Mitt kjønn",
    "Synnyinpaikkani": "Mitt fødested",
    "Murretaustani": "Min dialektbakgrunn",
    
    # Finnish regions (keep as-is since they're proper nouns)
    "Uusimaa": "Uusimaa",
    "Varsinais-Suomi": "Varsinais-Suomi",
    "Satakunta": "Satakunta",
    "Häme": "Häme",
    "Pirkanmaa": "Pirkanmaa",
    "Päijät-Häme": "Päijät-Häme",
    "Kymenlaakso": "Kymenlaakso",
    "Etelä-Karjala": "Etelä-Karjala",
    "Etelä-Savo": "Etelä-Savo",
    "Pohjois-Savo": "Pohjois-Savo",
    "Pohjois-Karjala": "Pohjois-Karjala",
    "Keski-Suomi": "Keski-Suomi",
    "Etelä-Pohjanmaa": "Etelä-Pohjanmaa",
    "Pohjanmaa": "Pohjanmaa",
    "Keski-Pohjanmaa": "Keski-Pohjanmaa",
    "Pohjois-Pohjanmaa": "Pohjois-Pohjanmaa",
    "Kainuu": "Kainuu",
    "Lappi": "Lappi",
    "Ahvenanmaa": "Ahvenanmaa",
    "Karjala": "Karelia",
    
    # More UI strings
    "Valitse valikosta maakunta tai alue, joka on eniten vaikuttanut sinun tapaasi puhua.": "Velg fra menyen fylket eller området som har påvirket talemåten din mest.",
    "Valitse valikosta maakunta tai alue, joka on eniten vaikuttanut tapaasi puhua.": "Velg fra menyen fylket eller området som har påvirket talemåten din mest.",
    "Valitse yltä maakunta tai alue, joka on eniten vaikuttanut sinun tapaasi puhua.": "Velg ovenfra fylket eller området som har påvirket talemåten din mest.",
    "Suomen kielen puhepankkiin on tosi tärkeätä saada mukaan kaikenlaista suomea. Kerro, miltä alueelta murteesi tai puhetapasi tulee.": "Det er veldig viktig å få alle slags finsk med i den finske talebanken. Fortell hvilken region dialekten eller talemåten din kommer fra.",
    "Valitse valikosta.": "Velg fra menyen.",
    "Valikossa ovat Suomen kunnat. Löydät omasi nopeimmin kirjoittamalla nimen alkua.": "Menyen inneholder finske kommuner. Du finner din raskest ved å skrive begynnelsen av navnet.",
    "Valikossa ovat Suomen nykyiset ja entiset kunnat.": "Menyen inneholder nåværende og tidligere finske kommuner.",
    
    # More feedback and instructions
    "Hyvin kerrottu!": "Godt fortalt!",
    "Hyvä!": "Bra!",
    "Tärkeä esine": "Viktig gjenstand",
    "Tärkeä esineeni": "Min viktige gjenstand",
    "Turha tavara": "Unødvendige ting",
    "Turhat tavarani": "Mine unødvendige ting",
    "Auta taas tutkijaa": "Hjelp forskeren igjen",
    "Henkilöllisyyttäsi ei voi niistä tunnistaa.": "Din identitet kan ikke identifiseres fra dem.",
    "Iso kiitos ...": "Stor takk ...",
    "... jos vastasit taustatietoihin!": "... hvis du svarte på bakgrunnsinformasjonen!",
    "Jos haluat, voit vielä kertoa tutkijoille neljä pientä taustatietoa.": "Hvis du vil, kan du fortsatt fortelle forskerne fire små bakgrunnsfakta.",
    "Sitten puhutaan esineistä.": "Så snakker vi om gjenstander.",
    "Jatkossa älylaitteet ja palvelut ymmärtävät paremmin puhetta.": "I fremtiden vil smarte enheter og tjenester forstå tale bedre.",
    "Aamukahvia juodessa katselen puuta, joka vaihtaa ulkomuotoaan kausittain.": "Mens jeg drikker morgenkaffe, ser jeg på et tre som endrer utseende etter årstidene.",
    "Kodikkuudesta": "Om hjemlig følelse",
    "Kodikkuus syntyy monesta eri asiasta. Myös kodin esineistä.": "Hjemlig følelse kommer fra mange forskjellige ting. Også fra hjemmets gjenstander.",
    "Vaatteisiin liittyy myös paljon muistoja. Nämä ken": "Klær er også knyttet til mange minner. Disse sko",  # incomplete sentence
    "Sitten voit taas auttaa tutkijoita yhdellä tiedolla.": "Da kan du igjen hjelpe forskerne med ett faktum.",
    
    # Common place name prefixes
    "Muu kuin Suomi": "Andre enn Finland",
    
    # Video-related
    "Video": "Video",
    "Video alkaa, kun painat Äänitä.": "Videoen starter når du trykker Ta opp.",
    "Video alkaa, kun painat Äänitä. Se kestää reilun minuutin.": "Videoen starter når du trykker Ta opp. Den varer litt over et minutt.",
    "Video kestää 2 minuuttia.": "Videoen varer 2 minutter.",
    "Video kestää 40 sekuntia.": "Videoen varer 40 sekunder.",
    "Video kestää reilun minuutin.": "Videoen varer litt over et minutt.",
    "Video kestää reilun minuutin. Kun olet valmis, paina Lopeta äänitys.": "Videoen varer litt over et minutt. Når du er ferdig, trykk Stopp opptak.",
    "Video kestää vajaan minuutin.": "Videoen varer litt under et minutt.",
    "Video käynnistyy Äänitä-napista.": "Videoen starter fra Ta opp-knappen.",
    "Video käynnistyy, kun painat Äänitä.": "Videoen starter når du trykker Ta opp.",
    
    # More prompts
    "Voit jatkaa myös videon pysähdyttyä.": "Du kan fortsette også etter at videoen har stoppet.",
    "Voit jatkaa ohjeistamista, vaikka kuva ei enää vaihdu. Kun olet valmis, paina Lopeta äänitys.": "Du kan fortsette å instruere selv om bildet ikke lenger endres. Når du er ferdig, trykk Stopp opptak.",
    "Voit jatkaa puhumista vielä videon loputtua.": "Du kan fortsette å snakke også etter at videoen er slutt.",
    "Voit kerrankin puhua suusi puhtaaksi.": "Du kan endelig snakke deg ut.",
    "Voit kertoa lemmikistä tai muusta eläimestä. Paina Äänitä-nappia, kun olet valmis puhumaan.": "Du kan fortelle om et kjæledyr eller et annet dyr. Trykk Ta opp-knappen når du er klar til å snakke.",
    "Voit kertoa myös viime päivien havainnoistasi luonnossa.": "Du kan også fortelle om observasjonene dine i naturen de siste dagene.",
    "Voit myös lahjoittaa lisää turisemalla jostain toisesta aiheesta.": "Du kan også donere mer ved å snakke om et annet tema.",
    "Voit myös pohtia rajausten keinoja.": "Du kan også tenke på måter å beskjære på.",
    "Voit vinkata puheen lahjoittamisesta muillekin! Alle 18-vuotiat lahjoittavat vanhempien luvalla.": "Du kan også tipse andre om taledonasjon! Under 18 år donerer med foreldres tillatelse.",
    "Voitto kotiin!": "Seier!",
    
    # Etc
    "Wow!": "Wow!",
    "Tervetuloa sporttisiin hetkiin!": "Velkommen til sportslige øyeblikk!",
    "Tervetuloa!": "Velkommen!",
    "Urheiluhetket": "Idrettsøyeblikk",
    "Urheilu": "Idrett",
    "Urheilusta puhumalla autoit juuri suomen kieltä. Haasta myös urheiluhullut kaverisi mukaan!": "Ved å snakke om idrett hjalp du nettopp det finske språket. Utfordre også de idrettsgale vennene dine!",
    "Upeata!": "Flott!",
    
    # Locations
    "Vastauksista ei voi päätellä henkilöllisyyttäsi.": "Din identitet kan ikke utledes fra svarene.",
    "Vastauksista ei voi päätellä henkilöllisyyttäsi. Ensin kysymme murretaustastasi.": "Din identitet kan ikke utledes fra svarene. Først spør vi om dialektbakgrunnen din.",
    "Vastauksista ei voi päätellä, kuka olet. Seuraavaksi voit kertoa ikäsi ja äidinkielesi.": "Det kan ikke utledes hvem du er fra svarene. Neste gang kan du fortelle alderen og morsmålet ditt.",
    
    # More instructions
    "Vedetään henkeä": "Trekk pusten",
    "Verrytellään ensin": "La oss varme opp først",
    "Verrytellään ensin. Kuvan Suomi-faneissa on kolme pientä eroa.": "La oss varme opp først. I bildet av Finland-fansen er det tre små forskjeller.",
    
    # More titles and prompts
    "Vielä yksi aihe. Kohta saat filosofoida sielun täydeltä!": "Ett tema til. Snart får du filosofere fra hjertet!",
    "Vinkkaa puheen lahjoittamisesta myös kavereille (alle 18-vuotiaat lahjoittavat vanhempien luvalla)!": "Tipse også venner om taledonasjon (under 18 år donerer med foreldres tillatelse)!",
    
    # More feedback
    "Tutkijat kiittävät!": "Forskerne takker!",
    "Tutkijat ja suomen kieli hyötyvät näiden tietojen kertomisesta.": "Forskerne og det finske språket drar nytte av at du forteller denne informasjonen.",
    "Tutkijat ja suomen kieli hyötyvät näistä tiedoista.": "Forskerne og det finske språket drar nytte av denne informasjonen.",
    "Tutkijat ja suomen kieli kiittävät.": "Forskerne og det finske språket takker.",
    "Tutkijat ja suomen kielekin kiittävät.": "For forskerne og det finske språket takker også.",
    
    # More prompts
    "Suuret kiitokset!": "Tusen takk!",
    "Suomen Kieli kiittää!": "Det finske språket takker!",
    "Tai lahjoita itse lisää juttelemalla jostain toisesta aiheesta.": "Eller doner mer selv ved å snakke om et annet tema.",
    "Tai lahjoita itse lisää.": "Eller doner mer selv.",
    "Tauot ja takeltelut ovat edelleen sallittuja!": "Pauser og stamming er fortsatt tillatt!",
    "Taustatiedoista sinua ei voi tunnistaa.": "Du kan ikke identifiseres fra bakgrunnsinformasjonen.",
    "Tee jotain muuta": "Gjør noe annet",
    "Testaamme osaammeko luoda uusia teemoja itse": "Vi tester om vi kan lage nye temaer selv",
    "Testiteema (title)": "Testtema (tittel)",
    "Tiesitkö, että puhelahjoitus on salatumpi kuin spermapankki? Lahjoittaja jää aina tuntemattomaksi.": "Visste du at taledonasjon er mer hemmelig enn sædbank? Giveren forblir alltid anonym.",
    "Tietosuojasta voit lukea lisää aloitussivulta.": "Du kan lese mer om personvern fra startsiden.",
    "Tiukimpien rajoitustoimien aikana moni asia oli kielletty. Mitä asiaa sinä kaipasit silloin eniten?": "Under de strengeste restriksjonene var mange ting forbudt. Hva savnet du mest da?",
    "Tiukka": "Streng",
    "Tiukkaa ohjeistusta!": "Strenge instruksjoner!",
    "Toinen leipätekstirivi. (body2)": "Andre brødtekstlinje. (body2)",
    "Tosiasiassa Mikael Gabriel jakaa kuvassa ruokaa vähävaraisille jouluna 2017.": "I virkeligheten deler Mikael Gabriel ut mat til trengende på bildet jul 2017.",
    "Tosielämässä olemme tietenkin kohteliaita ja kunnioittavia muita kohtaan.": "I virkeligheten er vi selvfølgelig høflige og respektfulle mot andre.",
    "Tässä moduulissa on suoratoistovideo.": "Denne modulen har en streaming-video.",
    "Tässä on yksi esimerkki. Kun painat Äänitä, näet toisen.": "Her er ett eksempel. Når du trykker Ta opp, ser du et annet.",
    "Tässä testataan metaotsikon muuttamista.": "Her testes endring av metatittelen.",
    "Tähän puhepankkiin on tärkeätä saada mukaan aivan kaikenlaista suomea. Auta siis tutkijoita ja kerro itsestäsi yksi taustatieto.": "Det er viktig å få alle slags finsk med i denne talebanken. Så hjelp forskerne og fortell ett bakgrunnsfaktum om deg selv.",
    "Tällä ajolistalla testataan erilaisia moduuleita. (body1)": "Denne spillelisten tester forskjellige moduler. (body1)",
    "Tämä juttutuokio oli pieni, mutta tärkeä osa suomen kielen puhepankkia.": "Denne prateøkten var en liten, men viktig del av den finske talebanken.",
    "Tämä on Ylen Urheiluruudun kaikkein aikojen suosituin tunnusmusiikki.": "Dette er Yle Sportsruta sin mest populære signatursmusikk gjennom tidene.",
    "Tämän avulla älylaitteet tulevat toivottavasti ymmärtämään meitä paremmin.": "Med dette vil forhåpentligvis smarte enheter forstå oss bedre.",
    "Tätisi Kanarialta soittaa kyselläkseen kuulumisia. Sää on hänen lempiaiheensa.": "Tanten din ringer fra Kanariøyene for å høre hvordan det går. Været er favorittemaet hennes.",
    "Tätisi on taas ajan tasalla kotimaan keleistä.": "Tanten din er igjen oppdatert på hjemlandets vær.",
    "Tätä kaipasin": "Dette savnet jeg",
    
    # Choice prompts
    "Tunnista koirat": "Gjenkjenn hundene",
    "Tunnista niistä valheelliset ja perustele vastauksesi.": "Identifiser de falske og begrunn svaret ditt.",
    "Tunnistatko valekuvat oikeista? Paina Äänitä, niin saat arvioitavaksesi neljä kuvaa.": "Kan du gjenkjenne falske bilder fra ekte? Trykk Ta opp, så får du fire bilder å vurdere.",
    "Tunnustusten huone": "Bekjennelsesrommet",
    "Tuore ihastuksesi esittelee matkakuviaan. Tee vaikutus häneen ja kysele kuvista.": "Din nye crush viser reisebildene sine. Imponér ham/henne og spør om bildene.",
    
    # Sport-related
    "Tsemppaa kissaa omaan tyyliisi. Päästä sisäinen Antero Mertarantasi valloilleen!": "Hei på katten på din egen måte. Slipp den indre Antero Mertaranta løs!",
    "Paikka on Munchenin olympiastadion ja vuosi 1972. Video alkaa, kun painat Äänitä.": "Stedet er München olympiastadion og året er 1972. Videoen starter når du trykker Ta opp.",
    "Paikat vaihtuvat 15 sekunnin välein.": "Stedene endres hvert 15. sekund.",
    "Selosta Virénin juoksu": "Kommenter Virén sitt løp",
    "Selosta heille, mitä videon tilanteissa tapahtuu. Video alkaa, kun painat Äänitä.": "Kommenter for dem hva som skjer i situasjonene i videoen. Videoen starter når du trykker Ta opp.",
    "Selosta, missä järjestyksessä puet päälle nämä tamineet.": "Kommenter i hvilken rekkefølge du tar på disse klærne.",
    "Seppo pakoilee": "Seppo rømmer",
    "Seuraavaksi hoksottimia tarvitaan otsikoiden kanssa.": "Neste gang trengs hjerneceller med overskriftene.",
    "Seuraavaksi kuva-arvoitus": "Neste gang bildegåte",
    "Seuraavaksi kyselemme kuvien avulla tämän päivän tunnelmistasi.": "Neste gang spør vi om dagens stemninger med hjelp av bilder.",
    "Seuraavaksi laitetaan vaatetta päälle.": "Neste gang tar vi på klær.",
    "Seuraavaksi näet kolme mainoskuvaa. Millaisia unelmia niissä näkyy?": "Neste gang ser du tre annonsebilder. Hvilke drømmer vises i dem?",
    "Seuraavaksi on sinun vuorosi: Yritä saada Seppo pysähtymään!": "Neste gang er det din tur: Prøv å få Seppo til å stoppe!",
    "Seuraavaksi pari nopeaa kysymystä tutkijoiden avuksi.": "Neste gang et par raske spørsmål for å hjelpe forskerne.",
    "Seuraavaksi pari sanaa boteista.": "Neste gang et par ord om botter.",
    "Seuraavaksi pääset avautumaan.": "Neste gang får du åpne deg.",
    "Seuraavaksi pääset tutkimaan kuvia.": "Neste gang får du undersøke bilder.",
    "Seuraavaksi saat komentaa hiukan kurittomia kansalaisia.": "Neste gang får du kommandere litt ulydige borgere.",
    
    # More content
    "Siellä voit kertoa muun muassa sen, onko Teemu Pukki Suomen paras urheilija.": "Der kan du blant annet fortelle om Teemu Pukki er Finlands beste idrettsutøver.",
    "Siis ensin tie hotellista baariin, sitten klubille ja lopuksi hotellille.": "Så først veien fra hotellet til baren, så til klubben og til slutt til hotellet.",
    "Siksi on tärkeää saada talteen kaikenlaista puhetta. Auta tutkijoita ja kerro omasta taustasi vähän.": "Derfor er det viktig å ta vare på alle slags tale. Hjelp forskerne og fortell litt om din egen bakgrunn.",
    "Sitten eteenpäin!": "Så fremover!",
    "Sitten eteenpäin! Olet voittanut tapaamisen suosikkiurheilijasi kanssa.": "Så fremover! Du har vunnet et møte med favorittsidrettsutøveren din.",
    "Sitten eteenpäin.": "Så fremover.",
    "Sitten jatketaan!": "Så fortsetter vi!",
    "Sitten kysymme taas muutaman taustatiedon tutkijoille.": "Så spør vi igjen om et par bakgrunnsfakta for forskerne.",
    "Sitten kysymme vielä pari taustatietoa tutkijoille. Kiitos jos vastaat!": "Så spør vi ennå et par bakgrunnsfakta for forskerne. Takk hvis du svarer!",
    "Sitten pieni tauko puhumiseen.": "Så en liten pause fra snakkingen.",
    "Sitten pureskellaan kuvien maailmaa.": "Så tygger vi på bildeverdenen.",
    "Sitten siirrytään hurmaushommiin.": "Så går vi over til sjarmering.",
    "Sitten sään pariin.": "Så til været.",
    "Sitten taas muutama pieni tieto tutkijoille.": "Så igjen noen få små fakta for forskerne.",
    "Sitten vesille ja ratkomaan kuva-arvoitusta. Kuva paljastuu vähän kerrallaan.": "Så til vannet og løse en bildegåte. Bildet avsløres litt om gangen.",
    "Sitten voit auttaa tutkijoita. Meidän kaikkien puheessa kuuluu oma tausta tai murre.": "Så kan du hjelpe forskerne. I alles tale høres vår egen bakgrunn eller dialekt.",
    "Sitten voit taas auttaa tutkijoita yhdellä tiedolla.": "Så kan du igjen hjelpe forskerne med ett faktum.",
    
    # Some/Social media
    "Some-suomi -tulkkaus": "Sosiale medier-finsk tolkning",
    "Somella on oma kielioppi, jota vanhemmat eivät välttämättä tunne.": "Sosiale medier har sin egen grammatikk som foreldre kanskje ikke kjenner.",
    "Somen botit": "Sosiale medier-botter",
    "Somessa on profiileja, jotka esittävät ihmistä, mutta niiden takana on osin tai kokonaan tietokoneohjelma.": "På sosiale medier er det profiler som later som de er mennesker, men bak dem er delvis eller helt et dataprogram.",
    "Suomen kesässä kisataan erikoisissa urheilulajeissa. Ulkomainen kaverisi ei ole koskaan kuullut tällaisista.": "I finsk sommer konkurreres det i spesielle idrettsgrener. Den utenlandske vennen din har aldri hørt om slikt.",
    "Suuria uutisia": "Store nyheter",
    "Saat ulkoavaruudesta vieraita, joilla on videokuvaa suomalaisesta kesänvietosta.": "Du får besøk fra verdensrommet som har videoopptak av finsk sommertilværelse.",
    "Sait Ohoh!-lehden toimittajana tuoreen silminnäkijäkuvan Mikael Gabrielista.": "Som journalist for bladet Ohoh! fikk du et friskt øyevitnebilde av Mikael Gabriel.",
    "Sanaselityspeli": "Ordforklaringsspill",
    "Sana vaihtuu 10  sekunnin välein.": "Ordet endres hvert 10. sekund.",
    "Se on iloisen haukahduksen arvoinen suoritus.": "Det er en prestasjon verdt et gledeshyl.",
    "Sehän meni hienosti": "Det gikk jo fint",
    "Sehän meni hienosti!": "Det gikk jo fint!",
    "Seksiä ja saksia!": "Sex og saks!",
    "Selitä oikein rautalangasta vääntäen, mistä lajissa on kyse!": "Forklar skikkelig fra bunnen av hva grenen handler om!",
    "Selitä, mitä nämä lyhenteet ja emojit tarkoittavat – tai siis ne, jotka itse tunnet.": "Forklar hva disse forkortelsene og emojierne betyr – eller i hvert fall de du selv kjenner.",
    "Siinähän ovat Pikku Kakkosesta tutut Karvakuonot: Riku, Eno-Elmeri sekä Ransu.": "Der er de kjente Karvakuonot fra Pikku Kakkonen: Riku, Eno-Elmeri og Ransu.",
    "Siirrytään sitten arvovaltaiseen seuraan.": "La oss så gå til anstendig selskap.",
    "Terveisiä perseestä!": "Hilsen fra rævhølet!",
    "Virén on sinipaita numero 228. Antaa mennä!": "Virén er blå trøye nummer 228. La oss gå!",
    "Yleensä Suomessa valitaan Vuoden urheilija. Nyt venytetään aikarajaa vähän pidemmäksi.": "Vanligvis velges Årets idrettsutøver i Finland. Nå strekker vi tidsrammen litt lenger.",
    "Uskomatonta, mutta totta!": "Utrolig, men sant!",
    "Usko tai älä!": "Tro det eller ei!",
    "Unelmien mainos": "Drømmeannonse",
    "Kalavaleet sallittuja!": "Fiskeløgner tillatt!",
    "K-18": "18+",
    "Valehtelevat kuvat": "Løgnaktige bilder",
    "Valeuutistarkastaja": "Falske nyheter-sjekker",
    "Tätisi Kanarilta soittaa kyselläkseen kuulumisia. Sää on hänen lempiaiheensa.": "Tanten din ringer fra Kanariøyene for å høre hvordan det går. Været er favorittemaet hennes.",
    "Kuvaile Kanarian-tädillesi tämän ja eilisen päivän säätä.": "Beskriv dagens og gårsdagens vær for tanten din på Kanariøyene.",
    "Äänet päälle!": "Lyd på!",
    "Älä katso, älä kuuntele": "Ikke se, ikke lytt",
    "Äitini kotikylässä viännettiin savvoo niin, että digilaitteet olisivat menneet siitä solmuun.": "I morens hjemlandsby ble dialekten snakket så sterkt at digitale enheter ville ha gått i knutepunktet av det.",
    "Keräillen ja metsästäen": "Samlende og jaktende",
    "Koska tekoälyalgoritmit ovat yhtä hyviä kuin ne data, josta ne oppivat": "Fordi AI-algoritmer er like bra som dataene de lærer fra",
}

if __name__ == "__main__":
    print("Supplementary translations:")
    print(f"Total: {len(SUPPLEMENTARY_TRANSLATIONS)} translations")
    for fi, nb in list(SUPPLEMENTARY_TRANSLATIONS.items())[:10]:
        print(f"  {fi[:50]:50} -> {nb[:50]}")
