# Project Intern: Autonomous Local Chief of Staff

**Intern** is a locally hosted, highly autonomous AI agent designed to act as a hyper-personalized Chief of Staff. It operates entirely on local hardware, processing sensitive daily data streams (calendar, financial, medical, and search history) to generate actionable micro-movements and life-management insights.

Because this agent handles highly sensitive personal data, the architecture is built on a foundation of **absolute zero-trust security, bare-metal isolation, and hard API throttles.**

## 🛡️ Core Security Architecture

This is not a standard API wrapper. The Intern is physically and logically boxed in:

1. **Hypervisor Isolation (Proxmox KVM):** The agent runs inside an isolated Ubuntu KVM virtual machine. No shared kernels. 
2. **Network Micro-Segmentation (SDN):** The VM sits on a host-only Virtual Network (VNet). The default egress policy is `DROP`. The agent can only reach explicitly whitelisted endpoints (e.g., SMTP/IMAP).
3. **Zero-Trust Access:** No open router ports. Remote access is handled exclusively via a Tailscale SSH tunnel installed *inside* the VM.
4. **Ephemeral Code Execution:** The agent dynamically writes Python to solve tasks. This code is NEVER executed on the host OS. It is trapped inside a disposable, unprivileged Alpine Docker container (`Dockerfile.burner`) that is destroyed the moment the code finishes running.
5. **The Kill Switch:** A LiteLLM Proxy sits between the agent and the local inference engine, enforcing strict Tokens-Per-Minute (TPM) and Requests-Per-Minute (RPM) limits to prevent infinite logic loops and hardware meltdowns.

## 🧠 Memory & State Management

The Intern uses a multi-tiered memory architecture designed to survive model switches and context-window compaction:

* **The Boot Sequence (`AGENTS.md`):** Loaded immediately upon instantiation. Forces the agent to read its constraints, ingest daily data, and review past mistakes before responding to the user.
* **The Handover State (`memory/YYYY-MM-DD.md`):** Append-only daily logs used to preserve context across long sessions.
* **The Operations Manual (`LEARNINGS.md`):** A strict record of the agent's past failures and the rules it generated to never repeat them.
* **Long-Term Storage (`agent_memory.h5`):** Powered by EdgeHDF5, this provides lightning-fast, zero-daemon Hybrid Search (Vector + BM25) for recalling exact variables, names, and concepts from past sessions.

## 📥 The Secure Data Ingest Pipeline

To analyze life data without exposing it to cloud APIs, we use a secure "Drop Box" methodology.

The agent has NO ability to scrape the user's personal devices. Instead, automated, encrypted cron jobs on the user's primary devices push daily text streams (JSON/CSV/TXT) through the Tailscale tunnel directly into the `workspace/ingest/` directory.

During the Boot Sequence, the Intern parses:
* `calendar_events.json`
* `search_history_72h.txt`
* `financial_alerts.csv`
* `health_wellness_log.txt`

It synthesizes this data into an actionable Boot Report, identifying scheduling conflicts, financial anomalies, and actionable steps toward the user's overarching goals, then deletes the ingest files to maintain a clean state.

## 🛠️ Tech Stack
* **Framework:** `smolagents` (CodeAgent)
* **Local Inference:** `Ollama` (Qwen 2.5 Coder 7B)
* **API Gateway:** `LiteLLM Proxy`
* **Execution Sandbox:** `Docker` (Python Alpine)
* **Vector Backend:** `EdgeHDF5`

## 🚀 Getting Started
*(Setup instructions for provisioning the Proxmox KVM, configuring the Proxmox SDN firewall, and launching the systemd services are detailed in `/docs/project_intern_adr.md`)*
