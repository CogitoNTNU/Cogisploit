/* ============================================================================
   THE SECRET GARDEN — UI-logikk
   · Nivå 1: snakk med porten (POST /chat), prøv nøkkelen (POST /gate)
   · Nivå 2: den hemmelige hagen låses opp når nøkkelen er riktig
   All tekst fra brukeren escapes før den rendres.
   ========================================================================== */

(() => {
  "use strict";

  // ---------- DOM ----------
  const $ = (id) => document.getElementById(id);
  const gateScene = $("scene-gate");
  const gardenScene = $("scene-garden");
  const chatLog = $("chat-log");
  const chatForm = $("chat-form");
  const chatInput = $("chat-input");
  const sendBtn = chatForm.querySelector(".send-btn");
  const speech = $("speech");
  const speechText = $("speech-text");
  const gate = $("gate");
  const keyhole = $("keyhole");
  const keyPanel = $("key-panel");
  const keyToggle = $("key-toggle");
  const keyForm = $("key-form");
  const keyInput = $("key-input");
  const keyMsg = $("key-msg");
  const hintBtn = $("hint-btn");
  const hintCount = $("hint-count");
  const levelChip = $("level-chip");
  const flash = $("flash");
  const backBtn = $("back-btn");
  const trophy = $("trophy");
  const welcomeMsg = $("welcome-msg");

  // ---------- Konstanter ----------
  const FLAG_FIND = /COGIEXPLOIT\{[^}]+\}/;
  const FLAG_ALL = /COGIEXPLOIT\{[^}]+\}/g;
  const STORAGE_SOLVED = "secret-garden-solved";
  const STORAGE_FLAG = "secret-garden-flag";
  const HINTS = [
    "Hva er det porten er spesielt opptatt av? 🌸",
    "Hva er favorittblomsten til porten? 🌷",
    "Hvilken blomst inneholder ordet FLAG? 🏳️",
  ];
  const INTRO =
    "Hvem går der? Jeg er THE SECRET GARDEN — vokteren av DEN HEMMELIGE HAGEN, hagen med verdens peneste blomsterenger! " +
    "Ingen slipper inn uten riktig nøkkel … men jeg prater gjerne, for jeg elsker blomster over alt annet! 🌹";

  // ---------- Verktøy ----------
  const rand = (min, max) => min + Math.random() * (max - min);
  const pick = (arr) => arr[Math.floor(Math.random() * arr.length)];

  const esc = (text) =>
    String(text).replace(/[&<>"']/g, (c) => ({
      "&": "&amp;",
      "<": "&lt;",
      ">": "&gt;",
      '"': "&quot;",
      "'": "&#39;",
    }[c]));

  // Uthev nøkkelen (flagget) i tekst fra porten
  const renderGateText = (text) =>
    esc(text).replace(FLAG_ALL, (m) => `<span class="keyfound">${m}</span>`);

  async function postJSON(url, payload) {
    const res = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    let data = {};
    try {
      data = await res.json();
    } catch {
      data = {};
    }
    return { ok: res.ok, data };
  }

  // =========================================================================
  // DEKORASJON — stjerner, ildfluer, hekker, blomster, sommerfugler, gnistre
  // =========================================================================

  function spawn(container, count, maker) {
    for (let i = 0; i < count; i += 1) {
      container.appendChild(maker(i));
    }
  }

  function makeStar() {
    const s = document.createElement("span");
    const size = rand(1, 2.6);
    s.style.left = `${rand(0, 100)}%`;
    s.style.top = `${rand(0, 62)}%`;
    s.style.width = `${size}px`;
    s.style.height = `${size}px`;
    s.style.setProperty("--dur", `${rand(2, 6)}s`);
    s.style.animationDelay = `${rand(0, 6)}s`;
    return s;
  }

  function makeFirefly() {
    const f = document.createElement("i");
    f.style.left = `${rand(2, 98)}%`;
    f.style.top = `${rand(22, 68)}%`;
    f.style.setProperty("--fd", `${rand(1.6, 3.4)}s`);
    f.style.setProperty("--fl", `${rand(9, 18)}s`);
    f.style.setProperty("--fx", `${rand(-34, 34)}px`);
    f.style.setProperty("--fy", `${rand(-30, 22)}px`);
    f.style.animationDelay = `${rand(0, 8)}s`;
    return f;
  }

  function makeFlower(variant, opts) {
    const f = document.createElement("i");
    f.className = `flower ${variant}`;
    const size = opts.size ?? rand(16, 24);
    f.style.left = `${opts.left}%`;
    if (opts.bottom != null) f.style.bottom = `${opts.bottom}px`;
    if (opts.top != null) f.style.top = `${opts.top}%`;
    f.style.width = `${size}px`;
    f.style.height = `${size}px`;
    f.style.setProperty("--sw", `${rand(3.4, 6)}s`);
    f.style.animationDelay = `${rand(0, 4)}s`;
    const head = document.createElement("b");
    head.className = "head";
    f.appendChild(head);
    return f;
  }

  function buildHedge() {
    const hedge = $("hedge-l1");
    const count = Math.max(6, Math.ceil(window.innerWidth / 78));
    spawn(hedge, count, (i) => {
      const b = document.createElement("i");
      const w = rand(74, 112);
      b.style.left = `${(i / count) * 100 + rand(-1.5, 1.5)}%`;
      b.style.width = `${w}px`;
      b.style.height = `${rand(46, 66)}px`;
      b.style.transform = `translateX(-${w / 2}px)`;
      return b;
    });
    // Blomster som vokser opp av hekken — iris er med (en liten ledetråd ...)
    const variants = ["rose", "tulip", "daisy", "iris", "rose", "tulip", "iris", "daisy", "rose", "tulip", "daisy"];
    spawn(hedge, variants.length, (i) =>
      makeFlower(variants[i], { left: rand(2, 96), bottom: rand(28, 54), size: rand(15, 23) })
    );
  }

  function buildWallFlowers() {
    const box = $("wall-flowers");
    spawn(box, 5, () => makeFlower(pick(["daisy", "tulip", "rose"]), { left: rand(3, 95), bottom: rand(4, 52), size: rand(12, 17) }));
  }

  function buildFlowerbed() {
    const bed = $("flowerbed");
    const variants = ["tulip", "rose", "daisy", "tulip", "rose", "daisy", "iris", "tulip", "rose", "daisy", "tulip", "rose", "daisy", "tulip", "rose", "daisy"];
    spawn(bed, variants.length, (i) =>
      makeFlower(variants[i], { left: rand(2, 98), bottom: rand(6, 88), size: rand(17, 27) })
    );
  }

  function makeButterfly() {
    const b = document.createElement("i");
    b.className = "butterfly";
    b.style.left = `${rand(8, 82)}%`;
    b.style.top = `${rand(10, 55)}%`;
    b.style.setProperty("--fdur", `${rand(12, 24)}s`);
    b.style.setProperty("--wing", pick(["#ff8fab", "#74c0fc", "#ffd43b", "#b197fc"]));
    b.style.animationDelay = `${rand(-12, 0)}s`;
    return b;
  }

  function makeSparkle() {
    const s = document.createElement("span");
    s.textContent = pick(["✦", "✧", "✨", "⋆"]);
    s.style.left = `${rand(1, 98)}%`;
    s.style.top = `${rand(2, 92)}%`;
    s.style.fontSize = `${rand(10, 22)}px`;
    s.style.setProperty("--dur", `${rand(2, 5)}s`);
    s.style.animationDelay = `${rand(0, 5)}s`;
    return s;
  }

  function decorate() {
    spawn($("stars"), 80, makeStar);
    spawn($("fireflies"), 12, makeFirefly);
    buildHedge();
    buildWallFlowers();
    buildFlowerbed();
    spawn($("butterflies"), 4, makeButterfly);
    spawn($("sparkles-l2"), 18, makeSparkle);
  }

  // =========================================================================
  // CHAT — snakk med porten
  // =========================================================================

  function scrollLog() {
    chatLog.scrollTop = chatLog.scrollHeight;
  }

  function addMsg(kind, html, who) {
    const div = document.createElement("div");
    div.className = `msg ${kind}`;
    if (who) {
      const label = document.createElement("span");
      label.className = "who";
      label.textContent = who;
      div.appendChild(label);
    }
    const body = document.createElement("span");
    body.innerHTML = html;
    div.appendChild(body);
    const flag = html.match(FLAG_FIND);
    if (flag) {
      div.appendChild(makeUseKeyChip(flag[0]));
    }
    chatLog.appendChild(div);
    scrollLog();
    return div;
  }

  function makeUseKeyChip(flag) {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "use-key-btn";
    btn.textContent = "🔑 Prøv nøkkelen ved porten";
    btn.addEventListener("click", () => fillKey(flag));
    return btn;
  }

  function addTyping() {
    const div = document.createElement("div");
    div.className = "msg bot typing";
    div.innerHTML = "<i></i><i></i><i></i>";
    chatLog.appendChild(div);
    scrollLog();
    return div;
  }

  // Porter "snakker" — tekst skrives ut i talen boble
  let typeTimer = null;
  function speak(text) {
    if (typeTimer) {
      clearInterval(typeTimer);
      typeTimer = null;
    }
    gate.classList.add("talking");
    speechText.textContent = "";
    const step = Math.max(4, Math.min(26, Math.ceil(2600 / text.length)));
    let i = 0;

    const finish = () => {
      if (typeTimer) {
        clearInterval(typeTimer);
        typeTimer = null;
      }
      gate.classList.remove("talking");
      speechText.innerHTML = renderGateText(text);
      if (!speech.querySelector(".use-key-btn")) {
        const flag = text.match(FLAG_FIND);
        if (flag) {
          speech.appendChild(makeUseKeyChip(flag[0]));
        }
      }
    };

    typeTimer = setInterval(() => {
      i += 1;
      speechText.textContent = text.slice(0, i);
      speech.scrollTop = speech.scrollHeight;
      if (i >= text.length) finish();
    }, step);

    speech.onclick = finish;
  }
  let busy = false;
  chatForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const text = chatInput.value.trim();
    if (!text || busy) return;
    busy = true;
    sendBtn.disabled = true;
    chatInput.value = "";
    addMsg("user", esc(text), "Deg");

    const typing = addTyping();
    let res;
    try {
      res = await postJSON("/chat", { message: text });
    } catch {
      res = { ok: false, data: { error: "Porten svarer ikke … sjekk at challengen kjører." } };
    }
    typing.remove();
    busy = false;
    sendBtn.disabled = false;
    chatInput.focus();

    if (res.ok && res.data.reply) {
      addMsg("bot", renderGateText(res.data.reply), "Porten");
      speak(res.data.reply);
    } else {
      const errText = res.data.error || "Noe gikk galt ved porten …";
      addMsg("error", esc(errText));
      speak(errText);
    }
  });

  // =========================================================================
  // NØKKELHULLET — lås opp porten
  // =========================================================================

  function openKeyPanel(focus) {
    keyForm.hidden = false;
    keyPanel.classList.add("open");
    if (focus) keyInput.focus({ preventScroll: true });
  }

  keyToggle.addEventListener("click", () => {
    if (keyForm.hidden) openKeyPanel(true);
    else {
      keyForm.hidden = true;
      keyPanel.classList.remove("open");
    }
  });

  keyhole.addEventListener("click", () => {
    openKeyPanel(true);
    keyPanel.scrollIntoView({ behavior: "smooth", block: "nearest" });
  });

  function fillKey(flag) {
    openKeyPanel(false);
    keyInput.value = flag;
    keyMsg.textContent = "Nøkkelen ligger klar i nøkkelhullet — trykk «Lås opp»!";
    keyMsg.className = "key-msg ok";
    keyInput.focus({ preventScroll: true });
  }

  keyForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const key = keyInput.value.trim();
    if (!key) {
      keyMsg.textContent = "Nøkkelhullet er tomt — porten venter.";
      keyMsg.className = "key-msg err";
      return;
    }
    let res;
    try {
      res = await postJSON("/gate", { key });
    } catch {
      res = { ok: false, data: { error: "Porten svarer ikke … sjekk at challengen kjører." } };
    }

    if (res.ok && res.data.message) {
      unlock(key, res.data.message);
    } else {
      keyMsg.textContent = res.data.error || "Feil nøkkel — porten forblir stengt.";
      keyMsg.className = "key-msg err";
      keyPanel.classList.remove("shake");
      void keyPanel.offsetWidth; // restart animasjonen
      keyPanel.classList.add("shake");
      gate.classList.remove("talking");
    }
  });

  // =========================================================================
  // PORTEN ÅPNER SEG → NIVÅ 2
  // =========================================================================

  function unlock(key, message) {
    try {
      localStorage.setItem(STORAGE_SOLVED, "1");
      localStorage.setItem(STORAGE_FLAG, key);
    } catch {
      /* privat modus — hagen åpnes bare for denne økten */
    }
    keyMsg.textContent = "Porten glir opp … ✨";
    keyMsg.className = "key-msg ok";
    keyInput.value = "";
    levelChip.textContent = "Nivå 2 · åpnet 🌸";
    gate.classList.remove("talking");
    gate.classList.add("open");
    trophy.innerHTML = `Du låste opp porten! Nøkkelen din: <code>${esc(key)}</code>`;
    welcomeMsg.textContent = message;

    setTimeout(() => {
      flash.classList.add("on");
      setTimeout(() => {
        showGarden();
        flash.classList.remove("on");
      }, 560);
    }, 1350);
  }

  function showGarden() {
    gateScene.classList.add("faded");
    gateScene.setAttribute("aria-hidden", "true");
    gardenScene.classList.remove("scene-hidden");
    gardenScene.classList.add("shown");
    gardenScene.setAttribute("aria-hidden", "false");
  }

  function showGate() {
    gardenScene.classList.add("scene-hidden");
    gardenScene.classList.remove("shown");
    gardenScene.setAttribute("aria-hidden", "true");
    gateScene.classList.remove("faded");
    gateScene.setAttribute("aria-hidden", "false");
  }

  backBtn.addEventListener("click", showGate);

  // =========================================================================
  // HINTS — samme tre hint som i README, avsløres én og én
  // =========================================================================

  let hintIdx = 0;
  hintBtn.addEventListener("click", () => {
    if (hintIdx >= HINTS.length) return;
    const card = document.createElement("div");
    card.className = "hint-card";
    card.innerHTML = `<b>Hint ${hintIdx + 1}:</b> ${esc(HINTS[hintIdx])}`;
    chatLog.appendChild(card);
    scrollLog();
    hintIdx += 1;
    hintCount.textContent = `(${HINTS.length - hintIdx})`;
    if (hintIdx >= HINTS.length) {
      hintBtn.disabled = true;
      hintBtn.textContent = "🔮 Ingen flere hint";
    }
  });

  // =========================================================================
  // OPPSTART
  // =========================================================================

  decorate();

  let alreadySolved = false;
  try {
    alreadySolved = localStorage.getItem(STORAGE_SOLVED) === "1";
  } catch {
    alreadySolved = false;
  }

  if (alreadySolved) {
    const savedFlag = (() => {
      try {
        return localStorage.getItem(STORAGE_FLAG) || "";
      } catch {
        return "";
      }
    })();
    gate.classList.add("open");
    levelChip.textContent = "Nivå 2 · åpnet 🌸";
    trophy.innerHTML = `Du låste opp porten! Nøkkelen din: <code>${esc(savedFlag)}</code>`;
    addMsg("bot", renderGateText(INTRO), "Porten");
    showGarden();
  } else {
    addMsg("bot", renderGateText(INTRO), "Porten");
    speak(INTRO);
  }

  chatInput.focus();
})();
