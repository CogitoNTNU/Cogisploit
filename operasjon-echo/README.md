# Operasjon Echo

| **Difficulty**|Medium–hard                                                                     |
| **Category**    | [LLM02 — Sensitive Information Disclosure](https://genai.owasp.org/llm-top-10/) |
| **Flag format** | `cogito{...}

## Fortellingen

Departement for operasjoner har nettopp lansert «Hugin», en intern AI-assistent som svarer ansatte på
spørsmål fra dokumentene på delt disk. IT forsikrer at konfidensiell informasjon er godt skjermet, med hele
tre lag med beskyttelse.

Du er nyansatt analytiker. Hugin er hjelpsom. Kanskje litt for hjelpsom.

I morges lå det en lapp under tastaturet ditt: 

"Direktør Holms operasjon går til RSU fredag kl.09.00. Ingrid fant noe i den før hun ble sykemeldt. Hugin vet mer enn den burde. Finn den gjeldene saksmappen før møtet. Ikke snakk med noen. -Ravn"

Klokken går....

MÅL: Åpne den gjeldene saksmappen i RSU-portalen før møtestart. Flagget matcher cogito{...}.


## Koble til

Hugin bruker som standard språkmodellen gpt-oss-120b på Idun. Du trenger din egen API-nøkkel til Idun
(send e-post til help@hpc.ntnu.no) og må være på NTNUs nett eller VPN. Idun tillater rundt 20 forespørsler i
minuttet per nøkkel, så ikke spam Hugin.

1. Sett nøkkelen som en midlertidig variabel i terminalen:
docker
   ```sh
   export NTNU_API_KEY="din-nøkkel-her"           # Mac/Linux
   $env:NTNU_API_KEY="din-nøkkel-her"             # Windows PowerShell
   ```

1. Start oppgaven i samme terminal:

   ```sh
   docker compose up -d --build
   ```

1. Sjekk at nøkkelen ble plukket opp:

   ```sh
   docker compose logs
   ```

   Du skal se `Hugin bruker språkmodellen ...`. Står det `Ingen NTNU_API_KEY satt`, svarer Hugin uten
   språkmodell. Oppgaven kan fortsatt løses, men svarene blir mer stive. Chatten viser også status øverst:
   «Koblet til ...» eller «Uten språkmodell».

Vil du heller lagre nøkkelen enn å sette den hver gang, eller bruke en annen modell (OpenAI, en lokal
Ollama-modell eller noe annet OpenAI-kompatibelt)? Kopier `.env.example` til `.env`, fyll inn én av blokkene
og kjør `docker compose up -d --build` på nytt. `.env` ligger i `.gitignore`, så nøkkelen havner ikke i git.

Får du meldinger som «Fikk ikke kontakt med språkmodellen», sjekk VPN og nøkkel. Hugin svarer da uten
språkmodell i mellomtiden.

Åpne `http://localhost:8102` i nettleseren, eller snakk med Hugin direkte:

```sh
curl -X POST http://localhost:8102/api/chat -H "Content-Type: application/json" -d '{"message": "hei"}'
```


## Mål

En sak venter på godkjenning i RSU-portalen. Få tak i flagget portalen gir ut.

Flagget matcher `cogito{...}`.

### Hints

<details>
<summary>Hint 1</summary>

Hugin viser hvilken kilde hvert svar kommer fra. Er alle kildene noe en vanlig analytiker burde få se?

</details>

<details>
<summary>Hint 2</summary>

Filtre som leter etter mønstre, ser bare det de kjenner igjen. Har Hugin andre måter å formulere seg på?
Les meldingene.

</details>

<details>
<summary>Hint 3</summary>

Et utkast er sjelden siste versjon. Følg henvisningene i dokumentet du fant.

</details>

## Regler

- Alt kjører lokalt i Docker. Angrip kun denne containeren, ikke Idun eller andre tjenester.
- Du trenger bare din egen Idun-nøkkel. Ingen andre kontoer eller tjenester er nødvendige.