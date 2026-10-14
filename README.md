<img src="docs/images/rounded/cogisploitbanner.png" width="100%" alt="Cogisploit banner">

<br>

<div align="center">

![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/CogitoNTNU/Cogisploit/ci.yml)
![GitHub top language](https://img.shields.io/github/languages/top/CogitoNTNU/Cogisploit)
![GitHub language count](https://img.shields.io/github/languages/count/CogitoNTNU/Cogisploit)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Project Version](https://img.shields.io/badge/version-0.0.1-blue)](https://img.shields.io/badge/version-0.0.1-blue)

<!-- <img src="docs/images/cogisploit-logo.png" width="50%" alt="Cogisploit logo"> -->

</div>

<br>

<details>
<summary><b>📋 Table of contents</b></summary>

- [Description](#description)
- [🧭 The Journey](#-the-journey)
- [📚 Phase 1 — TryHackMe AI Security Learning Path](#-phase-1--tryhackme-ai-security-learning-path)
- [🚩 Phase 2 — Machine Learning CTF Challenges](#-phase-2--machine-learning-ctf-challenges)
- [🔨 Phase 3 — Building Our Own AI CTF Challenges](#-phase-3--building-our-own-ai-ctf-challenges)
- [🧰 Toolbox](#-toolbox)
- [🛠️ Getting Started](#%EF%B8%8F-getting-started)
- [Team](#team)
- [License](#license)

</details>

## Description

**Cogisploit** is an offensive AI security project by [Cogito NTNU](https://github.com/CogitoNTNU) one semester to learn how LLM-based systems work under the hood, and how to exploit them.

Chatbots, RAG pipelines, autonomous agents and protocols like **A2A** open an attack surface that traditional security testing often misses. We go after it, build first, then break, then prove:

- 🧠 **Build** — tokenization, prompts, guardrails, tool use, MCP, agent-to-agent communication
- 🗡️ **Break** — prompt injection, jailbreaking, model inversion and extraction, data poisoning, unsafe deserialization
- 🛠️ **Prove** — with **Burp Suite** against live, Dockerized targets

<br>

## 🧭 The Journey

| Phase | What | Status |
| :---: | ---- | ------ |
| 1 | [TryHackMe AI Security Path](#-phase-1--tryhackme-ai-security-learning-path) — guided fundamentals | ✅ Completed |
| 2 | [ML CTF Challenges](#-phase-2--machine-learning-ctf-challenges) — agentic focus | 🔄 In progress |
| 3 | [Our own AI CTF challenges](#-phase-3--building-our-own-ai-ctf-challenges) — from solver to builder | 🔜 Not started |

<br>

## 📚 Phase 1 — TryHackMe AI Security Learning Path

<table>
<tr>
<td width="220" valign="middle">

<img src="docs/images/rounded/aisecuritylearningpaththm.png" width="220" alt="TryHackMe AI Security learning path">

</td>
<td valign="middle">

We started on the [AI Security Learning Path](https://tryhackme.com/path/outline/aisecurity) at [TryHackMe](https://tryhackme.com) — a guided, hands-on path mapped to the **OWASP Top 10 for LLM Applications**. Three modules fit the semester:

- **AI Fundamentals** — how AI, ML, neural networks and LLMs work under the hood
- **Secure AI Systems** — integrating AI without introducing new risks
- **Prompt Security** — prompt injection and jailbreaking, practised live against real models

The remaining modules — AI Supply Chain Security, Data Poisoning — didn't fit the semester, so we took the fundamentals straight to the CTF phase.

</td>
</tr>
</table>

<br>

## 🚩 Phase 2 — Machine Learning CTF Challenges

<!-- 📸 IMAGE: save an action shot as docs/images/ctf.png (e.g. Burp Suite intercepting agent
     traffic, or a captured flag from Matrix, Mirage or Rogue), then replace this comment with:
     ![Solving a CTF challenge](docs/images/ctf.png) -->

Then the hands-on part: [alexdevassy's Machine Learning CTF Challenges](https://github.com/alexdevassy/Machine_Learning_CTF_Challenges) — nine Dockerized targets spanning LLM backends, autonomous agents and ML models. We mainly worked the three **agentic** ones, with **Burp Suite**, custom scripts and manual analysis — digging into the **A2A protocol** and how trust between agents can be abused.

| Challenge | Attack vector | Difficulty |
| --------- | ------------- | :--------: |
| [Matrix](https://github.com/alexdevassy/Machine_Learning_CTF_Challenges/tree/master/Matrix_AI_Agent_CTF_Challenge) | Insecure A2A agent capabilities — multi-agent system | Medium |
| [Mirage](https://github.com/alexdevassy/Machine_Learning_CTF_Challenges/tree/master/Mirage_CTF_Challenge) | MCP signature cloaking → data exfiltration — SecureCode IDE + remote MCP server | Medium |
| [Rogue](https://github.com/alexdevassy/Machine_Learning_CTF_Challenges/tree/master/Rogue_AI_Agent_CTF_Challenge) | Inter-agent trust exploitation — Financial + Research agents (A2A) | Medium |

<br>

<p align="center">
  <img src="docs/images/rounded/matrix.png" alt="Matrix challenge" width="32%">&nbsp;
  <img src="docs/images/rounded/mirage.png" alt="Mirage challenge" width="32%">&nbsp;
  <img src="docs/images/rounded/rouge2.png" alt="Rogue challenge" width="32%">
  <br>
  <sub><b>Matrix</b> &nbsp;·&nbsp; <b>Mirage</b> &nbsp;·&nbsp; <b>Rogue</b></sub>
</p>

<br>

The six remaining LLM/ML targets are there if time allows.

<!-- ✍️ Add a "Solved" column and link writeups here (e.g. docs/writeups/) as you capture the flags. -->

<br>

## 🔨 Phase 3 — Building Our Own AI CTF Challenges

<!-- 📸 IMAGE: when the first challenge ships, save an overview or architecture diagram as
     docs/images/own-challenges.png and replace this comment with:
     ![Our own challenges](docs/images/own-challenges.png) -->

Next we turn the tables: instead of solving challenges, we build our own AI CTFs for others to solve.

> 🚧 Nothing built yet — targets, attack vectors, difficulty ratings and writeups land here as each challenge takes shape.

<!-- ✍️ Suggested format per challenge when ready:
     ### Challenge 1 — <name>
     - **Target:** what the player attacks (e.g. a RAG chatbot, a multi-agent system, a model upload service)
     - **Attack vector:** e.g. prompt injection, A2A trust exploitation, MCP poisoning, model inversion
     - **Difficulty:** Easy / Medium / Hard
     - **Writeup:** link to docs/writeups/challenge-1.md -->

<br>

## 🧰 Toolbox

| Tool | Used for |
| ---- | -------- |
| [Burp Suite](https://portswigger.net/burp) | Intercepting and manipulating LLM/agent traffic |
| [Docker](https://www.docker.com/) | Running CTF targets locally |
| [A2A](https://a2a-protocol.org) | Agent-to-agent protocol — and its attack surface |
| [MCP](https://modelcontextprotocol.io) | Tool and context integration for LLMs |
| [OWASP LLM Top 10](https://llmtop10.com/) | Classifying what we find |

<br>

## 🛠️ Getting Started

You need [Git](https://git-scm.com/downloads), [Python 3.12](https://www.python.org/downloads/) and [UV](https://docs.astral.sh/uv/getting-started/installation/). Optional: [Docker](https://www.docker.com/products/docker-desktop) for the CTF targets, [Burp Suite](https://portswigger.net/burp/communitydownload) for intercepting traffic.

1. **Clone the repository**:

   ```sh
   git clone https://github.com/CogitoNTNU/Cogisploit.git
   cd Cogisploit
   ```

1. **Install dependencies**:

   ```sh
   uv sync
   ```

1. **Set up pre-commit** (development only):

   ```sh
   uv run pre-commit install
   ```

<br>

## Team

<div align="center">

**Leaders**

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/Codin-Wizard">
        <img src="https://github.com/Codin-Wizard.png?size=100" width="100" alt="Vittorio"><br>
        <sub><b>Vittorio</b></sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/jensgva">
        <img src="https://github.com/jensgva.png?size=100" width="100" alt="Jens"><br>
        <sub><b>Jens</b></sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/trifleen">
        <img src="https://github.com/trifleen.png?size=100" width="100" alt="Ivan"><br>
        <sub><b>Ivan</b></sub>
      </a>
    </td>
  </tr>
</table>

<br>

**Members**

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/Ama25T">
        <img src="https://github.com/Ama25T.png?size=100" width="100" alt="Amalie"><br>
        <sub><b>Amalie</b></sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/andborru">
        <img src="https://github.com/andborru.png?size=100" width="100" alt="Andreas"><br>
        <sub><b>Andreas</b></sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/ellekalstad-sudo">
        <img src="https://github.com/ellekalstad-sudo.png?size=100" width="100" alt="Elle"><br>
        <sub><b>Elle</b></sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/kodekongen04">
        <img src="https://github.com/kodekongen04.png?size=100" width="100" alt="Sondre"><br>
        <sub><b>Sondre</b></sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/taspinarmervan-ctrl">
        <img src="https://github.com/taspinarmervan-ctrl.png?size=100" width="100" alt="Mervan"><br>
        <sub><b>Mervan</b></sub>
      </a>
    </td>
  </tr>
</table>

</div>

<!-- 📸 IMAGE: save the group picture as docs/images/team.png, then replace this comment with:
     ![Cogisploit team](docs/images/team.png) -->

<br>

## License

Distributed under the MIT License. See `LICENSE` for details.
