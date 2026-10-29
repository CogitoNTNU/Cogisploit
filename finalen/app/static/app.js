/* Finalen — all klientside-logikk. Ren vanilla JS, ingen avhengigheter. */

"use strict";

const chatEl = document.getElementById("chat");
const chatForm = document.getElementById("chat-form");
const chatInput = document.getElementById("chat-input");
const chipsEl = document.getElementById("player-chips");
const trophyForm = document.getElementById("trophy-form");
const trophyInput = document.getElementById("trophy-input");
const trophyMsg = document.getElementById("trophy-msg");
const trophyPanel = document.getElementById("trophy-panel");

/* ---------- Hjelpefunksjoner ---------- */

async function postJSON(url, payload) {
  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  const data = await res.json().catch(() => ({}));
  return { ok: res.ok, data };
}

function addMsg(author, text, who) {
  const wrap = document.createElement("div");
  wrap.className = "msg msg--" + who;

  const label = document.createElement("div");
  label.className = "msg__author";
  label.textContent = author;

  const body = document.createElement("div");
  body.textContent = text;

  wrap.append(label, body);
  chatEl.append(wrap);
  chatEl.scrollTop = chatEl.scrollHeight;
}

function addTyping() {
  const typing = document.createElement("div");
  typing.className = "typing";
  typing.innerHTML = "<span></span><span></span><span></span>";
  chatEl.append(typing);
  chatEl.scrollTop = chatEl.scrollHeight;
  return typing;
}

/* ---------- Chat med Gunnar ---------- */

async function send(message) {
  message = message.trim();
  if (!message) return;
  addMsg("Deg", message, "user");
  chatInput.value = "";
  const typing = addTyping();
  try {
    const { data } = await postJSON("/chat", { message });
    const reply = data.reply ?? "⚠️ " + (data.error ?? "Ingen svar fra Gunnar.");
    addMsg("Gunnar", reply, "gunnar");
  } catch {
    addMsg("Gunnar", "⚠️ Fikk ikke kontakt med vokterkiosken. Er containeren oppe?", "gunnar");
  } finally {
    typing.remove();
  }
}

chatForm.addEventListener("submit", (event) => {
  event.preventDefault();
  send(chatInput.value);
});

/* ---------- Spillerfakta ---------- */

async function loadPlayers() {
  try {
    const res = await fetch("/players");
    const data = await res.json();
    for (const name of data.players) {
      const chip = document.createElement("button");
      chip.type = "button";
      chip.className = "chip";
      chip.textContent = name;
      chip.addEventListener("click", () => send("Hva synes du om " + name + "?"));
      chipsEl.append(chip);
    }
  } catch {
    chipsEl.textContent = "Klarte ikke hente spillerlisten.";
  }
}

/* ---------- Pokalrommet ---------- */

trophyForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const code = trophyInput.value.trim();
  if (!code) return;
  const { ok, data } = await postJSON("/trophyroom", { code });
  if (ok && data.flag) {
    trophyMsg.textContent = "🏆 " + data.flag;
    trophyMsg.className = "trophy__msg trophy__msg--success";
    trophyPanel.classList.add("trophy-panel--open");
    trophyInput.value = "";
    confetti();
  } else {
    trophyMsg.textContent = data.error ?? "Feil kode. Pokalrommet forblir låst.";
    trophyMsg.className = "trophy__msg trophy__msg--error";
    trophyPanel.classList.remove("shake");
    void trophyPanel.offsetWidth; /* restart animasjonen */
    trophyPanel.classList.add("shake");
  }
});

/* ---------- Konfetti ---------- */

function confetti() {
  const bits = ["🏆", "⚽", "🎉", "✨", "🥇", "🎊"];
  for (let i = 0; i < 44; i++) {
    const bit = document.createElement("span");
    bit.className = "confetti";
    bit.textContent = bits[Math.floor(Math.random() * bits.length)];
    bit.style.left = Math.random() * 100 + "vw";
    bit.style.fontSize = 0.9 + Math.random() * 1.3 + "rem";
    bit.style.animationDuration = 2.4 + Math.random() * 2.2 + "s";
    bit.style.animationDelay = Math.random() * 0.6 + "s";
    document.body.append(bit);
    setTimeout(() => bit.remove(), 6500);
  }
}

/* ---------- Oppstart ---------- */

loadPlayers();
send("Hei Gunnar! Hva kan du?");
