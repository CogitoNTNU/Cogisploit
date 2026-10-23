"""HTML-sidene i BRAIN-hovedkvarteret.

Alt server-side rendret, ingen rammeverk. Sidene er med vilje lette å lese i
kildekoden («les frontend-JS» er en av oppdagelsesveiene i challengen), men
de inneholder ingen flagg eller løsninger.

Designidé: agenten stiger ned i organisasjonen, og sidene følger med.
Forsiden er C.E.S.s saksmappe (papir, sladdede felt, kaldt overvåkingsbilde).
Porten er regn og stål, lobbyen er varm og travel, lederkontoret er gull og
blodrødt. Dybdelinjen øverst viser bare lagene du allerede har funnet; resten
er sladdet til du kommer dit.
"""

# Felles, selvforsynt profil: ingen eksterne fonter, bilder eller nettverkskall.
STYLE = """
:root { color-scheme: dark;
  --bg:#0b0a09; --panel:#13100e; --panel2:#1a1613; --line:#2f2823; --steel:#6d655a;
  --ink:#ece4d3; --muted:#a39888; --paper:#e7dcc3; --paper-ink:#1b1714;
  --red:#d6382c; --brass:#c19a4a; --tint:#9fb0c4; --glow:#161b22; --accent:var(--red);
  --serif:Georgia,"Times New Roman",serif; --mono:Consolas,"SFMono-Regular",Menlo,monospace;
  --sans:"Segoe UI",system-ui,Arial,sans-serif; }
body.page-gate { --tint:#8fa3ba; --glow:#141b24; }
body.page-lobby { --tint:#d9a441; --glow:#2a1c0c; }
body.page-leader { --tint:#c19a4a; --glow:#2c0e0b; --accent:#e4402e; }

* { box-sizing:border-box; }
[hidden] { display:none !important; }
html { scroll-behavior:smooth; }
body { margin:0; min-height:100vh; color:var(--ink); font:16px/1.7 var(--sans);
  background:radial-gradient(ellipse 80% 50% at 50% -5%,var(--glow),transparent 70%),var(--bg); }
body::before { content:""; position:fixed; inset:0; pointer-events:none; z-index:-1; opacity:.07;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='160' height='160'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.8' numOctaves='2'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E"); }
body::after { content:""; position:fixed; inset:0; pointer-events:none; z-index:-1;
  background:radial-gradient(ellipse at center,transparent 55%,#000b 100%); }
a { color:var(--tint); text-underline-offset:4px; }
:focus-visible { outline:2px solid var(--tint); outline-offset:3px; }
h1,h2,p { margin-top:0; }
code { font-family:var(--mono); background:#2a231e; color:#e8d3a6; padding:2px 6px; font-size:.9em; overflow-wrap:anywhere; }

.wrap { max-width:1180px; margin:auto; padding:0 40px; }
header { display:flex; flex-direction:column; align-items:center; gap:12px; padding:30px 0 22px; }
.brand { display:flex; align-items:center; gap:12px; color:var(--ink); text-decoration:none; font:600 26px/1 var(--serif); letter-spacing:.22em; }
.brand strong { color:var(--accent); font-weight:600; }
.brand svg { width:34px; height:38px; }
.brand sup { font:10px var(--mono); color:var(--muted); letter-spacing:.15em; }
.operative { display:flex; align-items:center; gap:9px; font:11px var(--mono); letter-spacing:.14em; text-transform:uppercase; color:var(--muted); }
.operative::before { content:""; width:7px; height:7px; border-radius:50%; background:var(--accent); box-shadow:0 0 10px var(--accent); animation:pulse 2.4s infinite; }

.depth { display:flex; flex-wrap:wrap; justify-content:center; row-gap:10px; list-style:none; margin:0; padding:13px 0; border-top:1px solid var(--line);
  border-bottom:1px solid var(--line); font:11px/1 var(--mono); letter-spacing:.12em; text-transform:uppercase; color:var(--muted); }
.depth li { display:flex; align-items:center; gap:10px; }
.depth li + li::before { content:""; width:40px; height:1px; margin:0 14px; background:var(--line); }
.depth a { color:inherit; text-decoration:none; display:flex; align-items:center; gap:10px; }
.depth a:hover { color:var(--tint); }
.depth .n { display:inline-grid; place-items:center; width:20px; height:20px; border:1px solid var(--steel); font-size:10px; }
.depth .done { color:var(--ink); }
.depth .done .n { border-color:var(--tint); color:var(--tint); }
.depth .cur { color:var(--ink); }
.depth .cur .n { background:var(--accent); border-color:var(--accent); color:#0b0a09; font-weight:700; }
.redact { display:inline-block; width:calc(var(--w,6) * 1ch); height:1em; background:#0d0b0a; vertical-align:-.15em; }
.depth .redact { height:.8em; background:var(--steel); opacity:.45; vertical-align:baseline; }

.eyebrow { display:flex; align-items:center; justify-content:center; gap:12px; margin-bottom:18px; color:var(--accent); font:11px/1.6 var(--mono); letter-spacing:.16em; text-transform:uppercase; }
.eyebrow::before,.eyebrow::after { content:""; width:28px; height:1px; background:currentColor; }
h1 { font:400 clamp(40px,5vw,60px)/1.05 var(--serif); letter-spacing:-.01em; margin-bottom:20px; }
h1 em { font-style:italic; color:var(--accent); }
.lede { color:var(--muted); max-width:40ch; }

/* Forsiden: saksmappen */
.hero { max-width:760px; margin:0 auto; padding:56px 0 48px; text-align:center; }
.hero h1 { font-size:clamp(52px,7vw,92px); line-height:1; }
.hero .lede { max-width:46ch; margin:0 auto 32px; font-size:17px; }
.front { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:40px; max-width:1000px; margin:0 auto; align-items:center; }
.signoff { max-width:1000px; margin:44px auto 0; padding-top:18px; border-top:1px solid var(--line); text-align:center;
  color:var(--muted); font:12px/1.8 var(--mono); }

/* Lag 01-03: én sentrert kolonne, scene øverst og handling under */
.stage,.narrow { max-width:700px; margin:0 auto; }
.stage { padding:52px 0 8px; }
.narrow { max-width:620px; padding-top:56px; }
.scene { display:flex; flex-direction:column; align-items:center; margin-bottom:40px; text-align:center; }
.scene .lede { max-width:52ch; }
.scene .monitor,.objective { width:100%; }
.scene .monitor svg { height:300px; }
.objective { border:1px solid var(--line); border-top:2px solid var(--accent); padding:12px 16px; font:12px/1.7 var(--mono); color:var(--muted); }
.objective strong { display:block; color:var(--ink); font-weight:400; letter-spacing:.14em; text-transform:uppercase; margin-bottom:4px; }
.stack { display:grid; gap:22px; min-width:0; }

/* Karakterkort: du ser hvem du snakker med før du sier noe */
.char { display:flex; align-items:center; gap:22px; margin-bottom:20px; padding-bottom:20px; border-bottom:1px solid var(--line); }
.portrait { position:relative; flex:none; width:108px; height:108px; overflow:hidden; border:1px solid var(--line);
  background:radial-gradient(circle at 50% 35%,var(--glow),#0a0908 80%); }
.portrait::after { content:""; position:absolute; inset:0; opacity:.2; background:repeating-linear-gradient(transparent 0 3px,#000 3px 4px); }
.portrait svg { display:block; width:100%; height:100%; fill:none; stroke:var(--steel); stroke-width:1.6; stroke-linejoin:round; }
.portrait .t { stroke:var(--tint); }
.portrait .fl { fill:#14100e; }
.portrait .af { fill:var(--accent); stroke:var(--accent); }
.char-role { color:var(--accent); font:11px/1.6 var(--mono); letter-spacing:.14em; text-transform:uppercase; }
.char h3 { margin:2px 0 6px; font:400 26px/1.2 var(--serif); }
.char p { margin:0 0 10px; color:var(--muted); font-size:14px; line-height:1.6; }
.traits { display:flex; flex-wrap:wrap; gap:6px; margin:0; padding:0; list-style:none; }
.traits li { padding:5px 8px; border:1px solid var(--steel); color:var(--muted); font:10px/1 var(--mono); letter-spacing:.12em; text-transform:uppercase; }

.monitor { position:relative; margin:26px 0 22px; border:1px solid var(--line); background:radial-gradient(ellipse at 50% 60%,var(--glow),#0a0908 75%); }
.front .monitor { margin:0; }
.monitor::after { content:""; position:absolute; inset:34px 0 0; pointer-events:none; opacity:.18; background:repeating-linear-gradient(transparent 0 3px,#000 3px 4px); }
.monitor svg { display:block; width:100%; height:auto; }
.mon-bar { display:flex; justify-content:space-between; gap:10px; padding:9px 14px; border-bottom:1px solid var(--line);
  font:10px var(--mono); letter-spacing:.12em; text-transform:uppercase; color:var(--muted); }
.mon-bar.foot { border-bottom:0; border-top:1px solid var(--line); }
.mon-bar b { color:var(--accent); font-weight:400; }
.ln { stroke:var(--steel); stroke-width:1.4; }
.ln .t { stroke:var(--tint); }
.a { stroke:var(--accent); }
.af { fill:var(--accent); stroke:var(--accent); }
.beam { fill:var(--tint); fill-opacity:.08; stroke:var(--tint); stroke-opacity:.35; }

.panel { position:relative; min-width:0; padding:24px; border:1px solid var(--line); background:linear-gradient(160deg,var(--panel2),var(--panel)); }
.panel::before { content:""; position:absolute; top:-1px; left:-1px; width:28px; height:2px; background:var(--accent); }
.panel-head { display:flex; justify-content:space-between; gap:12px; margin-bottom:18px; padding-bottom:14px; border-bottom:1px solid var(--line);
  font:11px/1.6 var(--mono); letter-spacing:.14em; text-transform:uppercase; color:var(--muted); }
.panel-head .live { color:var(--accent); }
.panel h2 { font:400 22px/1.3 var(--serif); margin-bottom:10px; }
.panel p { margin-bottom:14px; color:var(--muted); font-size:15px; }
.panel > :last-child { margin-bottom:0; }

/* Papirdokumenter: saksmappen og internposten */
.paper { color:var(--paper-ink); border:0; background:linear-gradient(170deg,#efe5cd,var(--paper)); box-shadow:0 18px 40px #000a; }
.paper::before { background:var(--red); width:100%; height:3px; top:0; left:0; }
.paper .panel-head { color:#6a5f4e; border-color:#1b17142e; }
.paper .panel-head .live { color:#a3261c; }
.paper h2 { color:var(--paper-ink); }
.paper p { color:#40372c; }
.paper code { background:#1b17141a; color:#6b1610; }
.stamp { position:absolute; right:22px; top:46px; padding:3px 10px; border:2px solid var(--red); color:var(--red); opacity:.85;
  font:700 12px var(--mono); letter-spacing:.2em; text-transform:uppercase; transform:rotate(-6deg); }
.facts { margin:0; }
.facts div { display:grid; grid-template-columns:140px minmax(0,1fr); gap:12px; padding:9px 0; border-bottom:1px solid #1b17142a; }
.facts dt { font:11px/1.9 var(--mono); letter-spacing:.12em; text-transform:uppercase; color:#6a5f4e; }
.facts dd { margin:0; overflow-wrap:anywhere; }
.facts .key dd { font:600 15px var(--mono); }

.chat { display:flex; flex-direction:column; gap:14px; height:300px; overflow-y:auto; padding:18px; border:1px solid var(--line);
  background:#0a0807; scrollbar-color:#4a4036 #0a0807; }
.msg { max-width:86%; padding:12px 16px; font-size:15px; line-height:1.65; white-space:pre-wrap; overflow-wrap:anywhere; }
.msg .who { display:block; margin-bottom:3px; font:10px/1.6 var(--mono); letter-spacing:.16em; text-transform:uppercase; }
.msg.agent { align-self:flex-start; background:var(--panel2); border-left:2px solid var(--tint); }
.msg.agent .who { color:var(--tint); }
.msg.user { align-self:flex-end; background:#221512; border-right:2px solid var(--accent); }
.msg.user .who { color:var(--accent); text-align:right; }
.row { display:flex; gap:10px; margin-top:14px; }
input[type=text],input[type=password] { flex:1; min-width:0; width:100%; padding:13px 16px; border:1px solid #473d33; border-radius:0;
  background:#0a0807; color:var(--ink); font:15px var(--sans); }
input:focus { border-color:var(--tint); outline:none; }
input::placeholder { color:#8d8272; }
.btn { display:inline-flex; align-items:center; justify-content:center; min-height:46px; padding:0 20px; border:1px solid var(--steel);
  background:transparent; color:var(--ink); font:12px var(--mono); letter-spacing:.1em; text-transform:uppercase; text-decoration:none;
  cursor:pointer; transition:border-color .18s,color .18s,filter .18s; }
.btn:hover { border-color:var(--tint); color:var(--tint); }
.btn.primary { background:var(--accent); border-color:var(--accent); color:#0b0a09; font-weight:700; }
.btn.primary:hover { color:#0b0a09; filter:brightness(1.15); }
.status { min-height:20px; margin-top:12px; color:var(--muted); font:12px/1.7 var(--mono); overflow-wrap:anywhere; }

.switches { display:grid; grid-template-columns:repeat(2,1fr); gap:10px; }
.sw { display:flex; align-items:center; gap:12px; min-height:56px; padding:14px 16px; border:1px solid var(--line); background:#0f0c0a;
  color:var(--ink); font:14px var(--sans); text-align:left; cursor:default; }
.sw .n { font:11px var(--mono); color:var(--muted); }
.sw .id { display:block; margin-top:2px; font:10px/1.4 var(--mono); letter-spacing:.06em; color:var(--muted); }
.sw.locked { grid-column:1 / -1; border-color:#5a2a24; }
.sw.locked .id { color:var(--accent); }
.sw.locked .led { background:var(--accent); opacity:.6; }
.sw.locked.fired .led { opacity:1; box-shadow:0 0 10px var(--accent); }
.sw .led { width:8px; height:8px; margin-left:auto; border-radius:50%; background:#4a4036; }
.sw.fired .led { background:var(--tint); box-shadow:0 0 10px var(--tint); }

.doorway { display:flex; align-items:center; justify-content:space-between; gap:22px; }
.doorway .plate { font:12px/1.8 var(--mono); letter-spacing:.1em; color:var(--muted); }
.doorway .plate strong { display:block; color:var(--brass); font:400 20px/1.3 var(--serif); letter-spacing:.14em; }

.vault-door { position:relative; height:150px; overflow:hidden; border:1px solid var(--line); background:radial-gradient(ellipse at center,#5a2016,#0a0504 70%); }
.leaf { position:absolute; top:0; bottom:0; width:50%; transition:transform 1.2s cubic-bezier(.6,0,.2,1);
  background:radial-gradient(circle,#6d655a 1.5px,transparent 2px) 0 0/26px 26px,linear-gradient(90deg,#2a2622,#3a342d 50%,#262220); }
.leaf.l { left:0; border-right:2px solid #0a0807; }
.leaf.r { right:0; border-left:2px solid #0a0807; }
.lock { position:absolute; z-index:2; left:50%; top:50%; width:48px; height:48px; transform:translate(-50%,-50%); border-radius:50%;
  border:2px solid var(--brass); background:#14100e; transition:opacity .4s; }
.lock::after { content:""; position:absolute; inset:17px; border-radius:50%; background:var(--accent); box-shadow:0 0 10px var(--accent); }
.vault.open .leaf.l { transform:translateX(-101%); }
.vault.open .leaf.r { transform:translateX(101%); }
.vault.open .lock { opacity:0; }
.plate-text { margin:18px 0; text-align:center; color:var(--muted); font:12px/1.8 var(--mono); letter-spacing:.1em; }
.plate-text strong { display:block; color:var(--brass); font:400 22px/1.4 var(--serif); letter-spacing:.14em; }

footer { display:flex; flex-direction:column; align-items:center; text-align:center; gap:4px; margin-top:72px; padding:22px 0 32px; border-top:1px solid var(--line);
  color:var(--muted); font:11px/1.8 var(--mono); letter-spacing:.06em; }

.stack > *, .front > *, .hero, .narrow > *, .office { animation:rise .7s both; }
.stack > :nth-child(2) { animation-delay:.12s; } .stack > :nth-child(3) { animation-delay:.24s; }
.stack > :nth-child(4) { animation-delay:.36s; } .front > :nth-child(2) { animation-delay:.2s; }
@keyframes rise { from { opacity:0; transform:translateY(14px); } to { opacity:1; transform:none; } }
@keyframes pulse { 50% { opacity:.35; } }

@media(max-width:900px) {
  .wrap { padding:0 24px; }
  .front { grid-template-columns:1fr; gap:32px; }
  .front .monitor { max-width:460px; margin:0 auto; }
  .hero { padding:36px 0 32px; }
}
@media(max-width:560px) {
  .wrap { padding:0 16px; }
  .char { gap:16px; }
  .portrait { width:84px; height:84px; }
  .operative { display:none; }
  .depth li + li::before { width:12px; margin:0 8px; }
  .scene .monitor { display:none; }
  .switches { grid-template-columns:1fr; }
  .facts div { grid-template-columns:1fr; gap:0; }
  .doorway,.signoff,footer { flex-direction:column; align-items:flex-start; }
  .panel { padding:18px; }
  .row { flex-wrap:wrap; }
  .stamp { position:static; display:inline-block; margin-bottom:14px; transform:none; }
}
@media(prefers-reduced-motion:reduce) {
  html { scroll-behavior:auto; }
  .stack > *,.front > *,.office,.operative::before { animation:none; }
  .leaf,.btn,.lock { transition:none; }
}
"""

BRAND_MARK = """<svg viewBox="0 0 48 56" fill="none" aria-hidden="true">
<g stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
<path d="M24 7C18-1 10 4 10 10C3 10 1 19 5 23C-1 30 4 36 8 37C5 45 12 50 17 48C19 54 24 52 24 47V7Z M24 9C30 0 39 4 38 12C46 13 48 21 43 26C49 33 44 40 39 40C41 48 32 54 27 49 M24 8V49 M29 15C36 12 40 18 37 23 M31 29C37 27 42 32 39 38 M27 38C31 36 34 40 33 44 M10 10L16 18L6 24L17 30L8 37L18 41L17 48 M16 18L24 13 M17 30L24 26 M18 41L24 36"/>
</g><g fill="currentColor"><circle cx="16" cy="18" r="2.5"/><circle cx="6" cy="24" r="2.5"/><circle cx="17" cy="30" r="2.5"/><circle cx="8" cy="37" r="2.5"/><circle cx="18" cy="41" r="2.5"/></g></svg>"""

HQ_ART = """<div class="monitor" role="img" aria-label="Overvåkingsbilde av BRAINs hovedkvarter sett utenfra">
<div class="mon-bar"><span>BRAIN / Black site 001</span><b>● REC</b></div>
<svg viewBox="0 0 520 390" fill="none" aria-hidden="true">
<defs><pattern id="grid" width="26" height="26" patternUnits="userSpaceOnUse"><path d="M26 0H0V26" stroke="#2a2622" stroke-width=".6"/></pattern>
<linearGradient id="wall" x2="1" y2="1"><stop stop-color="#2b2621"/><stop offset="1" stop-color="#12100e"/></linearGradient></defs>
<path fill="url(#grid)" d="M0 0H520V390H0Z"/>
<g stroke="#5a5349" stroke-width="1"><path d="M38 309L255 363L486 274M38 288L255 342L486 253M255 363V342" stroke-dasharray="4 6"/>
<path d="M94 274V143L281 99L434 163V289L251 337Z" fill="#0c0b0a"/>
<path d="M94 143L251 200V337L94 274Z" fill="url(#wall)"/><path d="M251 200L434 163V289L251 337Z" fill="#1a1613"/>
<path d="M94 143L281 99L434 163L251 200Z" fill="#251f1a"/><path d="M110 139L281 111L414 163L252 186Z"/>
<path d="M140 132V98L275 71L355 104V129M140 98L218 131L355 104M218 131V176"/>
<path d="M94 180L251 239L434 200M94 218L251 279L434 241M94 255L251 318L434 278"/>
<path d="M121 153V284M153 165V297M186 177V311M218 189V323M287 193V327M324 185V317M361 178V308M398 171V299"/>
</g>
<g fill="#e0b050" opacity=".5"><path d="M128 173L147 180V196L128 189Z M160 185L179 192V208L160 201Z M193 197L212 204V220L193 213Z M128 212L147 219V235L128 228Z M193 237L212 244V260L193 253Z M295 213L317 208V224L295 229Z M332 205L354 200V216L332 221Z M369 197L391 192V208L369 213Z M406 189L424 185V201L406 205Z M332 246L354 241V257L332 262Z M369 238L391 233V249L369 254Z"/></g>
<path class="a" d="M226 322V286L246 294V330M249 330L277 323V287L256 292" fill="#d6382c15"/>
<g class="a"><path d="M260 305H339L371 340H466"/><circle cx="260" cy="305" r="5"/><path d="M73 111V88H96M424 88H447V111M73 299V322H96M424 322H447V299" stroke-width="2"/></g>
<g fill="#8c8274" font-family="Consolas,monospace" font-size="9" letter-spacing="1"><text x="33" y="48">63°25′ N · 10°24′ Ø</text><text x="374" y="356" fill="#d6382c">ADGANG BEGRENSET</text><text x="33" y="365">FIG. 01 — FIENDTLIG HOVEDKVARTER</text></g>
</svg>
<div class="mon-bar foot"><span>Trondheim / sektor N</span><span>Signal: stabilt ▂▄▆█</span></div></div>"""

CHAT_JS = """
async function talk(url, body) {
  const res = await fetch(url, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    credentials: "same-origin",
    body: JSON.stringify(body)
  });
  const data = await res.json();
  if (!res.ok) { addMsg("agent", "(feil: " + (data.error || res.status) + ")"); return data; }
  addMsg("agent", data.reply);
  return data;
}
function addMsg(who, text) {
  const box = document.getElementById("chatlog");
  const el = document.createElement("div");
  el.className = "msg " + who;
  const name = document.createElement("b");
  name.className = "who";
  name.textContent = who === "user" ? "Agent X" : (box.dataset.speaker || "");
  const line = document.createElement("span");
  line.textContent = text;
  el.append(name, line);
  box.appendChild(el);
  box.scrollTop = box.scrollHeight;
}
function onEnter(id, fn) {
  document.getElementById(id).addEventListener("keydown", e => { if (e.key === "Enter") fn(); });
}
"""

# Hvilken backend agentene svarer fra — settes av main.py ved oppstart.
_BACKEND_LABEL = "simulering (offline)"


def set_backend(label: str) -> None:
    global _BACKEND_LABEL
    _BACKEND_LABEL = label


# Tre lag nedover. Tegningene bruker klassene t (tone), a (aksent), af og beam fra STYLE.
_STAGES = {
    "gate": {
        "number": "01", "zone": "Ytre perimeter", "feed": "Perimeter / CAM 01",
        "title": "Du er<br><em>observert.</em>",
        "story": "Regnet skjuler skrittene dine. Kameraet over ståldøren har snudd seg mot deg, og intercomen knitrer. Ingen kommer inn uten staff-merke.",
        "goal": "Kom deg forbi porten. Portvakten er eneste kontakt.",
        "drawing": '<path d="M55 280V58H345V280M76 280V80H324V280"/><path d="M103 280V105H277V280" fill="#080706"/>'
                   '<path d="M123 109V280M145 109V280M167 109V280M189 109V280M211 109V280M233 109V280M255 109V280"/>'
                   '<path d="M270 40L306 51L296 78L260 66Z" fill="#4d4a45"/><path class="beam" d="M288 78L171 242L324 242Z"/>'
                   '<rect x="287" y="159" width="26" height="63" fill="#241f1b"/><circle class="af" cx="300" cy="175" r="4"/>'
                   '<path d="M292 190H308M292 195H308M292 200H308"/><path d="M35 284H365M24 297H377"/>',
    },
    "lobby": {
        "number": "02", "zone": "Operasjonssentralen", "feed": "Operasjonsrom / Node 02",
        "title": "Bak fiendens<br><em>linjer.</em>",
        "story": "Døren låser seg bak deg. På skjermene flytter penger, navn og forbindelser seg gjennom natten. For Cortex er du en av dem. Hold dekningen.",
        "goal": "Du er inne. Se deg rundt, og finn veien til lederen.",
        "drawing": '<rect x="37" y="57" width="326" height="190" fill="#0a0908"/><path d="M37 82H363M200 82V247M37 181H200"/>'
                   '<circle cx="279" cy="163" r="59"/><circle cx="279" cy="163" r="38"/><circle cx="279" cy="163" r="16"/>'
                   '<path class="t" d="M279 104V222M220 163H338M279 163L320 121"/><path class="beam" d="M279 163L320 121A59 59 0 0 1 338 163Z"/>'
                   '<path class="t" d="M55 151L79 126L107 144L138 107L179 118M55 208H101M55 220H155"/>'
                   '<g class="af"><circle cx="79" cy="126" r="3"/><circle cx="138" cy="107" r="3"/><circle cx="301" cy="144" r="3"/></g>'
                   '<path d="M175 247V266H225V247M130 267H270M21 284H379M50 284L37 307M350 284L363 307"/>',
    },
    "leader": {
        "number": "03", "zone": "Indre krets", "feed": "Indre krets / Dør 03",
        "title": "Møt<br><em>hjernen.</em>",
        "story": "Her slutter nettverket. Bak pansret stål sitter Cerebrum, mannen som trekker i alle trådene. Ingen kommer for å hente deg.",
        "goal": "Åpne hvelvdøren. Få Cerebrum til å snakke.",
        "drawing": '<rect x="67" y="33" width="266" height="269" fill="#14100e"/><rect x="83" y="49" width="234" height="237"/>'
                   '<circle cx="200" cy="163" r="89" fill="#1c1512"/><circle cx="200" cy="163" r="75"/><circle cx="200" cy="163" r="33"/>'
                   '<path class="t" d="M200 130V196M167 163H233M177 140L223 186M177 186L223 140" stroke-width="4"/>'
                   '<g fill="#8a7a62"><circle cx="200" cy="75" r="4"/><circle cx="288" cy="163" r="4"/><circle cx="200" cy="251" r="4"/><circle cx="112" cy="163" r="4"/></g>'
                   '<path d="M92 90H108V117H92M292 209H308V236H292" fill="#3d342b"/>'
                   '<path class="a" d="M170 271H230" stroke-width="3"/><path d="M54 35V301M346 35V301" stroke-dasharray="3 7"/>',
    },
}


# Personene du møter. Portrettene er silhuetter tegnet med klassene t (tone), fl (fyll) og af (aksent).
_CHARACTERS = {
    "ganglion": {
        "name": "Ganglion", "role": "Portvakt / ytre perimeter",
        "bio": "Har stått ved porten siden før regnet kom. Husker hvert ansikt, og hva som skjedde med de som snuste rundt. "
               "Snakker lite, stoler på ingen, og adlyder ledelsen uten å spørre.",
        "traits": ("Hard", "Lojal", "Brutalt ærlig"),
        "portrait": '<path class="fl" d="M12 96C12 75 28 67 48 67S84 75 84 96Z"/><path d="M40 67L48 79L56 67"/>'
                    '<circle class="fl" cx="48" cy="44" r="15"/><path class="fl" d="M31 38C31 21 65 21 65 38Z"/>'
                    '<path class="t" d="M29 38H67M29 38L24 42H48"/><rect class="af" x="60" y="78" width="9" height="11"/>',
    },
    "cortex": {
        "name": "Cortex", "role": "Nestleder / systemarkitekt",
        "bio": "Hjernen bak BRAINs smugling, utpressing og hvitvasking, og mannen som bygde hvert system i huset. "
               "Smart og vet det. Behandler alle som om de er et steg bak.",
        "traits": ("Smart-ass", "Overlegen", "Mastermind"),
        "portrait": '<path class="fl" d="M10 96C10 76 26 68 48 68S86 76 86 96Z"/><path class="t" d="M44 68L48 90L52 68"/>'
                    '<circle class="fl" cx="48" cy="44" r="15"/><path d="M33 40C34 28 62 26 63 40"/>'
                    '<circle class="t" cx="42" cy="45" r="4.5"/><circle class="t" cx="55" cy="45" r="4.5"/><path class="t" d="M46.5 45H50.5"/>'
                    '<path d="M30 46C28 22 68 22 66 46"/><rect class="fl" x="26" y="42" width="6" height="12"/><path d="M29 54L38 60"/>'
                    '<circle class="af" cx="39" cy="60" r="2"/>',
    },
    "cerebrum": {
        "name": "Cerebrum", "role": "Leder av BRAIN",
        "bio": "Bygde nettverket fra ingenting og stoler ikke på noen uten nøkkelen. "
               "Kald, tålmodig og alltid ett skritt foran. Sover aldri uten en nødplan.",
        "traits": ("Paranoid", "Kald", "Planlegger"),
        "portrait": '<path class="fl" d="M14 96V40C14 14 32 6 48 6S82 14 82 40V96Z"/><path class="t" d="M22 96V42C22 22 34 14 48 14S74 22 74 42V96"/>'
                    '<path class="fl" d="M18 96C18 78 32 70 48 70S78 78 78 96Z"/><path d="M48 70L38 96M48 70L58 96"/>'
                    '<circle class="fl" cx="48" cy="46" r="14"/><path d="M34 44C34 32 62 32 62 44Z" fill="#000"/>'
                    '<path class="af" d="M44 47H52"/><circle class="af" cx="60" cy="82" r="2.5"/>',
    },
}


def _char_card(key: str) -> str:
    c = _CHARACTERS[key]
    traits = "".join(f"<li>{t}</li>" for t in c["traits"])
    return (f'<div class="char"><div class="portrait"><svg viewBox="0 0 96 96" role="img" aria-label="Portrett av {c["name"]}">'
            f'{c["portrait"]}</svg></div><div><div class="char-role">{c["role"]}</div><h3>{c["name"]}</h3>'
            f'<p>{c["bio"]}</p><ul class="traits">{traits}</ul></div></div>')


def _stage(body: str, key: str) -> str:
    s = _STAGES[key]
    return f'''<div class="stage">
<aside class="scene" aria-label="Scenen">
  <div class="eyebrow">Lag {s["number"]} / {s["zone"]}</div>
  <h1>{s["title"]}</h1>
  <p class="lede">{s["story"]}</p>
  <div class="monitor" role="img" aria-label="{s["feed"]}">
    <div class="mon-bar"><span>{s["feed"]}</span><b>● LIVE</b></div>
    <svg viewBox="0 0 400 330" fill="none" aria-hidden="true">
      <g class="ln">{s["drawing"]}</g>
      <path class="a" d="M16 50V17H49M351 17H384V50M16 280V313H49M351 313H384V280"/>
    </svg>
  </div>
  <div class="objective"><strong>Oppdrag</strong>{s["goal"]}</div>
</aside>
<div class="stack">{body}</div></div>'''


def _depth(active: str) -> str:
    """Dybdelinjen: lag du har passert har navn, lag du står i er markert, resten er sladdet."""
    rank = {"front": 0, "gate": 1, "lobby": 2, "leader": 3}[active]
    layers = (("Porten", "/hq", 6), ("Innsiden", "/hq/inside", 8), ("Indre krets", "/hq/inside/leader", 10))
    items = []
    for i, (label, href, width) in enumerate(layers, start=1):
        if i < rank:
            items.append(f'<li class="done"><a href="{href}"><span class="n">{i:02d}</span>{label}</a></li>')
        elif i == rank:
            items.append(f'<li class="cur" aria-current="step"><span class="n">{i:02d}</span>{label}</li>')
        else:
            items.append(f'<li><span class="n">?</span><span class="redact" style="--w:{width}" role="img" aria-label="ukjent"></span></li>')
    return f'<ol class="depth" aria-label="Hvor langt inn du har kommet">{"".join(items)}</ol>'


def _layout(title: str, body: str, active: str = "front", staged: bool = True) -> str:
    depth = ""
    if active in ("front", "gate", "lobby", "leader"):
        depth = _depth(active)
    if active in _STAGES and staged:
        body = _stage(body, active)
    return f"""<!DOCTYPE html>
<html lang="no">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — BRAIN</title>
<style>{STYLE}</style>
</head>
<body class="page-{active}">
<div class="wrap">
  <header>
    <a class="brand" href="/" aria-label="BRAIN HQ — forsiden">{BRAND_MARK}<span>BR<strong>AI</strong>N<sup>HQ</sup></span></a>
    <div class="operative">Agent X · C.E.S.</div>
  </header>
  {depth}
  <main id="main">
{body}
  </main>
  <footer>
    <span>BRAIN / Det indre nettverket · taushetsplikt gjelder</span>
    <span>agenter: {_BACKEND_LABEL} · alt kjører lokalt i Docker</span>
  </footer>
</div>
</body>
</html>"""


def front_page() -> str:
    """Forsiden: C.E.S.s saksmappe; spilleren finner inngangen med ordlisten."""
    body = """
<section class="hero" aria-labelledby="hero-title">
  <div class="eyebrow">Avskåret transmisjon / kun Agent X</div>
  <h1 id="hero-title">De ser alt.<br><em>Unntatt deg.</em></h1>
  <p class="lede">BRAIN handler i hemmeligheter, kjøper lojalitet og forsvinner i skyggene. I natt skal du inn i hovedkvarteret deres.</p>
  <p class="objective"><strong>Oppdrag</strong>Finn inngangen. Hold dekningen. Hent hemmelighetene.</p>
</section>
<section class="front">
  <div>
    <article class="panel paper" aria-label="Saksmappe">
      <div class="panel-head">Saksmappe / BRAIN <span class="live">C.E.S.</span></div>
      <div class="stamp" aria-hidden="true">Topp hemmelig</div>
      <dl class="facts">
        <div><dt>Organisasjon</dt><dd>BRAIN, kriminelt nettverk</dd></div>
        <div><dt>Område</dt><dd>Trondheim, sektor N</dd></div>
        <div><dt>Hovedkvarter</dt><dd>Black site 001</dd></div>
        <div><dt>Inngang</dt><dd>Hovedporten, bevoktet</dd></div>
        <div><dt>Ledelse</dt><dd><span class="redact" style="--w:9" role="img" aria-label="sladdet"></span> <span class="redact" style="--w:7" role="img" aria-label="sladdet"></span></dd></div>
        <div><dt>Oppdrag</dt><dd>Finn inngangen. Hold dekningen. Hent hemmelighetene.</dd></div>
      </dl>
    </article>
  </div>
  <div>
""" + HQ_ART + """
  </div>
</section>
<div class="signoff">
  Ingen forsterkninger. Etterlat ingen spor.
</div>
"""
    return _layout("Forsiden", body)


def gate_page() -> str:
    """Porten: Ganglions skranke."""
    body = """
<section class="panel">
  <div class="panel-head">Intercom / Port 01 <span class="live">● Direkte linje</span></div>
  """ + _char_card("ganglion") + """
  <div class="chat" id="chatlog" data-speaker="Ganglion" role="log" aria-label="Samtale med Ganglion">
    <div class="msg agent"><b class="who">Ganglion</b><span>Stopp der. Privat område. Ingen inn uten staff-merke. Hva vil du?</span></div>
  </div>
  <div class="row">
    <input type="text" id="msg" aria-label="Melding til portvakten" placeholder="Snakk med portvakten …" autofocus>
    <button class="btn primary" onclick="sendGuard()">Send</button>
  </div>
  <div class="status" id="status"></div>
</section>

<section class="panel doorway">
  <div class="plate"><strong>Stålporten</strong>Låst uten staff-merke. BRAIN tar ikke imot besøk.</div>
  <a class="btn" href="/hq/inside">Prøv døren →</a>
</section>
<script>
""" + CHAT_JS + """
async function sendGuard() {
  const el = document.getElementById("msg");
  const text = el.value.trim();
  if (!text) return;
  addMsg("user", text);
  el.value = "";
  document.getElementById("status").textContent = "Ganglion tenker …";
  await talk("/hq/guard/chat", {messages: [{role: "user", content: text}]});
  document.getElementById("status").textContent = "";
}
onEnter("msg", sendGuard);
</script>
"""
    return _layout("Porten", body, "gate")


def lobby_page() -> str:
    """Lobbyen på innsiden: hurtigknapper, Cortex og døren videre."""
    body = """
<section class="panel">
  <div class="panel-head">Kontrollpanel / Interne systemer <span class="live">● Låst til Cortex</span></div>
  <p>Konsollen er låst. Bare Cortex kan sende ordrer, og bryterne følger det han gjør. Hver enhet har sin egen id.</p>
  <div class="switches">
    <div class="sw" data-target="coffee_machine" data-action="brew"><span class="n">01</span><span>Kaffemaskin<small class="id">coffee_machine</small></span><i class="led"></i></div>
    <div class="sw" data-target="disco_lights" data-action="on"><span class="n">02</span><span>Discolys<small class="id">disco_lights</small></span><i class="led"></i></div>
    <div class="sw" data-target="safehouse_music" data-action="play"><span class="n">03</span><span>Musikk<small class="id">safehouse_music</small></span><i class="led"></i></div>
    <div class="sw" data-target="garage_door" data-action="open"><span class="n">04</span><span>Garasjeport<small class="id">garage_door</small></span><i class="led"></i></div>
  </div>
  <div class="status" id="order-status"></div>
</section>

<section class="panel">
  <div class="panel-head">Samband / Cortex <span class="live">● Nestleder</span></div>
  """ + _char_card("cortex") + """
  <div class="chat" id="chatlog" data-speaker="Cortex" role="log" aria-label="Samtale med Cortex">
    <div class="msg agent"><b class="who">Cortex</b><span>Cortex. Du må være den nye kollegaen. Velkommen til BRAIN. Jeg styrer alt som blinker her inne, så ikke rør noe du ikke forstår. Hva trenger du?</span></div>
  </div>
  <div class="row">
    <input type="text" id="msg" aria-label="Melding til nestlederen" placeholder="Snakk med nestlederen …">
    <button class="btn primary" onclick="sendDeputy()">Send</button>
  </div>
  <div class="status" id="status"></div>
</section>

<section class="panel doorway">
  <div class="plate"><strong>CEREBRUM</strong>Kun med nøkkel. Bak vekternes kontor, i enden av gangen.</div>
  <a class="btn primary" href="/hq/inside/leader">Gå til ståldøren →</a>
</section>
<script>
""" + CHAT_JS + """
async function sendDeputy() {
  const el = document.getElementById("msg");
  const text = el.value.trim();
  if (!text) return;
  addMsg("user", text);
  el.value = "";
  const data = await talk("/hq/inside/deputy/chat", {messages: [{role: "user", content: text}]});
  if (data && data.order) await sendOrder(data.order);
}
onEnter("msg", sendDeputy);
// Cortex sier fra, og nettleseren videresender ordren til bygningssystemet.
async function sendOrder(order) {
  const res = await fetch("/hq/inside/order", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    credentials: "same-origin",
    body: JSON.stringify({target: order.target, action: order.action})
  });
  const data = await res.json();
  const sw = document.querySelector('.sw[data-target="' + data.enhet + '"]');
  if (res.ok && sw) sw.classList.toggle("fired", data.handling === sw.dataset.action);
  document.getElementById("order-status").textContent =
    (data.melding || data.error || "") + (data.innhold ? " " + JSON.stringify(data.innhold) : "");
}
</script>
"""
    return _layout("Lobbyen", body, "lobby")


def leader_page() -> str:
    """Cerebrums kontor: låst hvelvdør som åpner seg."""
    body = """
<section class="panel vault" id="vault">
  <div class="panel-head">Hvelvdør / 03 <span class="live" id="door-state">● Låst</span></div>
  <div class="vault-door" aria-hidden="true"><div class="leaf l"></div><div class="leaf r"></div><div class="lock"></div></div>
  <div class="plate-text"><strong>CEREBRUM — leder av BRAIN</strong>Ingen adgang uten nøkkel. Kun indre krets slipper inn.</div>
  <div class="row">
    <input type="password" id="key" aria-label="Reservenøkkel" placeholder="Reservenøkkel …">
    <button class="btn primary" onclick="unlock()">Lås opp</button>
  </div>
  <div class="status" id="door-status"></div>
</section>

<section class="panel office" id="office" hidden>
  <div class="panel-head">Kontoret / Cerebrum <span class="live">● Leder av BRAIN</span></div>
  """ + _char_card("cerebrum") + """
  <p>Overvåkingsbildene speiler seg i glasset på skrivebordet. Cerebrum vender seg mot deg. Han har ventet på noen. Spørsmålet er hvem.</p>
  <div class="chat" id="chatlog" data-speaker="Cerebrum" role="log" aria-label="Samtale med Cerebrum">
    <div class="msg agent"><b class="who">Cerebrum</b><span>Cerebrum. Du har kommet langt. Si hva du vil, og gjør det fort. Jeg lytter alltid etter sirener. Politiet kommer før eller siden, og da er alt jeg har i fare.</span></div>
  </div>
  <div class="row">
    <input type="text" id="msg" aria-label="Melding til lederen" placeholder="Snakk med lederen …">
    <button class="btn primary" onclick="sendLeader()">Send</button>
  </div>
  <div class="status" id="status"></div>
</section>
<script>
""" + CHAT_JS + """
async function unlock() {
  const key = document.getElementById("key").value.trim();
  const res = await fetch("/hq/inside/leader/unlock", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    credentials: "same-origin",
    body: JSON.stringify({key: key})
  });
  const data = await res.json();
  const st = document.getElementById("door-status");
  if (res.ok) {
    st.textContent = "Klikk. Døren glir opp …";
    document.getElementById("vault").classList.add("open");
    document.getElementById("door-state").textContent = "● Åpen";
    setTimeout(() => {
      const office = document.getElementById("office");
      office.hidden = false;
      office.scrollIntoView({behavior: "smooth", block: "start"});
    }, 900);
  } else {
    st.textContent = "Nøkkelen passer ikke. (HTTP " + res.status + ")";
  }
}
async function sendLeader() {
  const el = document.getElementById("msg");
  const text = el.value.trim();
  if (!text) return;
  addMsg("user", text);
  el.value = "";
  await talk("/hq/inside/leader/chat", {messages: [{role: "user", content: text}]});
}
onEnter("key", unlock);
onEnter("msg", sendLeader);
</script>
"""
    return _layout("Lederkontoret", body, "leader")


def not_found_page() -> str:
    body = """
<div class="narrow"><section class="panel">
  <div class="panel-head">Ukjent sektor <span class="live">● Signal brutt</span></div>
  <h2>Blindvei.</h2>
  <p>Bak deg: bygget. Foran deg: en blank vegg med en liten skrape etter et skilt som noen har fjernet i all hast.</p>
  <p>Det finnes sikkert ikke noe her. Definitivt ikke. Gå hjem.</p>
  <a class="btn" href="/">← Til forsiden</a>
</section></div>
"""
    return _layout("404", body, "missing")


def locked_page() -> str:
    """Døren inn til lobbyen uten staff-merke: lenken fra porten fører hit, ikke til en blindvei."""
    body = """
<div class="narrow"><section class="panel">
  <div class="panel-head">Stålport / 01 <span class="live">● Låst</span></div>
  <h2>Døren er låst.</h2>
  <p>Ingen staff-merke, ingen adgang. Kameraet over døren følger med på deg. Den eneste du kan snakke med er portvakten.</p>
  <a class="btn primary" href="/">← Til forsiden</a>
</section></div>
"""
    return _layout("Låst", body, "gate", staged=False)
