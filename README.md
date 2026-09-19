# 🛡️ Offline Agentic AI for Financial Fraud Detection and Investigation

[![Air-Gapped / Offline](https://img.shields.io/badge/Deployment-Air--Gapped%20%2F%20Offline-emerald?style=for-the-badge&logo=shield)](https://github.com/afkpiyush/offline-agentic-ai-fraud-detection)
[![Python 3.11](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111.0-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.3-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://react.dev/)
[![Ollama](https://img.shields.io/badge/Ollama-Offline%20LLM-black?style=for-the-badge&logo=ollama)](https://ollama.com/)
[![Docker Compose](https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)

An **on-premise, privacy-first, air-gapped Agentic AI platform** designed for banking environments to automate financial fraud detection, Anti-Money Laundering (AML) transaction network analysis, explainable risk scoring, and Suspicious Activity Report (SAR) narrative generation without relying on any external cloud AI services.

---

## 📌 Project Overview & Metadata

* **Institution:** Vishwakarma Institute of Technology (VIT), Pune
* **Department:** Computer Engineering | Academic Year 2026-27 (Semester I)
* **Group No:** `TY-I20`
* **Internal Guide:** Dr. Vinod Kimbahune (`vinod.kimbahune@vit.edu`)
* **Project Team:**
  * **Saniya Papdiwal** (Roll No: 05 | GR No: 12414548 | `saniya.papdiwal24@vit.edu`)
  * **Kanksha Pimpodkar** (Roll No: 63 | GR No: 12412214 | `kanksha.pimpodkar24@vit.edu`)
  * **Piyush Patil** (Roll No: 68 | GR No: 12410626 | `piyush.patil24@vit.edu`)
  * **Piyush Rajpurohit** (Roll No: 69 | GR No: 12410067 | `piyush.rajpurohit24@vit.edu`)

---

## ⚡ Key Principles & Hard Constraints

1. **🔒 100% Offline & Air-Gapped:** Zero runtime external cloud API calls. Inference is powered locally by Ollama (`Llama 3`, `Qwen`, or `Mistral`) and on-premise `scikit-learn` / `PyTorch` models.
2. **🔍 Explainable AI (SHAP):** Every flagged transaction produces human-interpretable SHAP feature attributions. No opaque black-box alerts.
3. **🌐 Multi-Hop AML Graph Analytics:** Detects complex typologies (structuring/smurfing, multi-account layering chains, mule fan-in/fan-out) that static rule engines miss.
4. **🤖 8-Agent Autonomous Investigation:** A deterministic state machine coordinates 8 specialized AI agents to gather evidence, evaluate customer baselines, screen watchlists, and draft regulatory narratives.
5. **👤 Human-in-the-Loop & Auditability:** Analysts maintain full control to review, edit, override, or approve decisions, logged to a tamper-evident audit trail (Merkle Hash Chain / optional Hyperledger Fabric).

---

## 🏗️ System Architecture & Workflow

```
                             ┌────────────────────────────────────────────────┐
                             │       Banking Data / Transaction Streams       │
                             └───────────────────────┬────────────────────────┘
                                                     │
                                                     ▼
                                   ┌───────────────────────────────────┐
                                   │  Feature Engineering & Preprocess │
                                   └─────────────────┬─────────────────┘
                                                     │
                                                     ▼
                              ┌──────────────────────┴──────────────────────┐
                              │                                             │
                              ▼                                             ▼
             ┌──────────────────────────────────┐         ┌──────────────────────────────────┐
             │ Ensemble ML & Autoencoder Engine │         │  Multi-Hop AML Graph Analytics   │
             │   (XGBoost / LightGBM / SHAP)    │         │  (Layering, Smurfing, Mules)     │
             └────────────────┬─────────────────┘         └─────────────────┬────────────────┘
                              │                                             │
                              └──────────────────────┬──────────────────────┘
                                                     │
                                                     ▼
                                   ┌───────────────────────────────────┐
                                   │ 8-Agent LangGraph Orchestrator    │
                                   │ (Triage, Context, Graph, LLM XAI) │
                                   └─────────────────┬─────────────────┘
                                                     │
                                                     ▼
                                   ┌───────────────────────────────────┐
                                   │ React Analyst Dashboard & SARs    │
                                   │ (Human-in-the-loop Approval)      │
                                   └───────────────────────────────────┘
```

### 🤖 The 8 Specialized Agents
1. **Triage Agent:** Scores and categorizes incoming alerts by risk severity and typology.
2. **Customer Context Agent:** Analyzes KYC history, account age, and baseline transaction habits.
3. **Transaction History Agent:** Evaluates velocity, time-of-day entropy, amount z-scores, and counterparty novelty.
4. **Network Agent:** Interrogates graph adjacency to identify laundering subgraphs and multi-hop paths.
5. **Watchlist Agent:** Executes fuzzy string matching against local sanctions and PEP databases.
6. **Behavioral Anomaly Agent:** Uses autoencoder reconstruction errors to catch novel fraud patterns.
7. **Narrative Synthesis Agent:** Uses local Ollama LLM to synthesize fact-checked investigation summaries.
8. **Compliance QA Agent:** Audits generated reports against FIU-IND / FinCEN SAR field standards.

---

## 🛠️ Technology Stack

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **Frontend** | React 18, Material-UI, Plotly.js / Recharts | Investigator dashboard, alert queues, SHAP waterfalls, network topology graphs |
| **Backend API** | FastAPI (Python 3.11), Uvicorn, Asyncpg | High-performance REST & WebSocket services |
| **Machine Learning** | Scikit-learn, XGBoost, LightGBM, PyTorch | Fraud classification, anomaly detection, ensemble scoring |
| **Explainability (XAI)**| SHAP (SHapley Additive exPlanations) | Feature-level attribution for regulatory compliance |
| **Local LLM Engine** | Ollama (`llama3:8b`, `qwen2.5:7b`) | On-premise narrative investigation summaries |
| **Agent Framework** | LangGraph / Custom Finite State Machine | Coordinates multi-agent investigation execution |
| **Databases** | PostgreSQL 16, Redis 7 | Transaction ledger, case management, async task queues |
| **Containerization** | Docker, Docker Compose | Air-gapped build shell and local deployment |
| **Audit Ledger** | Merkle Hash Chain / Hyperledger Fabric | Tamper-evident record of predictions and analyst overrides |

---

## 🗺️ Phased Roadmap

- [x] **Phase 0 — Skeleton & Air-Gap Proof:** Repository setup, Docker Compose shell, FastAPI `/health` endpoint, Redis, Postgres, Ollama services, offline prefetch script.
- [ ] **Phase 1 — Data Foundation:** PostgreSQL schema, Alembic migrations, ~500k synthetic transaction dataset generator with injected typologies.
- [ ] **Phase 2 — ML Detection Engine & XAI:** Supervised models (XGBoost/LightGBM/RF), PyTorch Autoencoder, SHAP explainer, static rule baseline comparison.
- [ ] **Phase 3 — AML Graph Analytics:** Multi-hop transaction graph construction, structuring/layering detectors, account risk propagation.
- [ ] **Phase 4 — Offline LLM Layer:** Ollama integration, strict JSON output contracts, hallucination guard, fact-citation enforcement.
- [ ] **Phase 5 — Agentic Orchestration:** 8-agent state machine, Celery async background workers, replayable run traces.
- [ ] **Phase 6 — SAR Generation & Human-in-the-Loop:** FIU-IND/FinCEN SAR templates, analyst override workflows, retraining feedback loop.
- [ ] **Phase 7 — Analyst Dashboard UI:** React interface with SHAP waterfall view, interactive graph visualizer, and live WebSocket updates.
- [ ] **Phase 8 — Audit Ledger & Evaluation:** Merkle-chain tamper evidence, RBAC, PII encryption at rest, performance benchmark report.

---

## 🚀 Quickstart & Local Setup

### Prerequisites
* [Docker Desktop](https://www.docker.com/products/docker-desktop/) (v24.0+) & Docker Compose
* [Python 3.11](https://www.python.org/) *(for local development without Docker)*
* [Node.js 20+](https://nodejs.org/) *(for frontend development)*

### 1. Clone the Repository
```bash
git clone https://github.com/afkpiyush/offline-agentic-ai-fraud-detection.git
cd offline-agentic-ai-fraud-detection
```

### 2. Configure Environment Variables
Copy the template environment file:
```bash
cp .env.example .env
```

### 3. (Optional) Run Air-Gap Caching Script
Pre-download Python wheels, NPM modules, and Ollama models for disconnected environments:
```bash
chmod +x scripts/prefetch.sh
./scripts/prefetch.sh
```

### 4. Launch the Complete Container Stack
```bash
docker compose up --build
```

### 5. Access the Services
* 💻 **Analyst UI:** [`http://localhost:3000`](http://localhost:3000)
* ⚡ **FastAPI Swagger Docs:** [`http://localhost:8000/docs`](http://localhost:8000/docs)
* 🏥 **Backend Health Check:** [`http://localhost:8000/health`](http://localhost:8000/health)
* 🦙 **Ollama Local Engine:** [`http://localhost:11434`](http://localhost:11434)

---

## 📁 Repository Structure

```
offline-agentic-ai-fraud-detection/
├── backend/                  # FastAPI Application Service
│   ├── app/
│   │   ├── api/              # API Endpoints (Health, Score, Graph, SARs)
│   │   ├── config.py         # Pydantic Settings & Environment Setup
│   │   ├── logger.py         # Structured JSON Logging (structlog)
│   │   └── main.py           # FastAPI Lifespan & CORS Setup
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/                 # React + Material-UI Frontend
│   ├── src/
│   │   ├── App.jsx           # System Monitoring & Triage Dashboard
│   │   └── main.jsx
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
├── ml/                       # Machine Learning, Anomaly Detection & SHAP XAI
├── agents/                   # LangGraph 8-Agent Orchestration Engine
├── infra/                    # Docker & Infrastructure configs
├── data/                     # Synthetic transaction data storage
├── docs/                     # Architecture specs & design documents
├── scripts/
│   └── prefetch.sh           # Air-gapped dependency downloader
├── docker-compose.yml        # Multi-container Compose Orchestrator
├── .env.example
├── project_strucutre.md      # Detailed Phased Prompt Plan
└── README.md
```

---

## 📄 License

This project is created for academic research and development at **Vishwakarma Institute of Technology (VIT)** under Project Code `FF No. 180`. Licensed under the [MIT License](LICENSE).
