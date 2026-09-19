# Offline Agentic AI for Financial Fraud Detection and Investigation
## Phased Build Prompt Set

**Group TY-I20** · Department of Computer Engineering, VIT · AY 2026-27, Semester I
**Internal Guide:** Dr. Vinod Kimbahune

**How to use this file:** paste the *Master Context Block* at the top of every new session, then paste exactly one phase prompt below it. Do not move to the next phase until its gate passes.

---

## Master Context Block

> You are helping me build **Offline Agentic AI for Financial Fraud Detection and Investigation** — an on-premise, air-gapped fraud + AML investigation platform for banks.
>
> **Hard constraints (never violate):**
> - Zero runtime calls to external/cloud AI services. All inference is local (Ollama + local sklearn/PyTorch models).
> - Every flagged transaction must carry a machine-readable explanation (SHAP feature attributions). No unexplained alerts.
> - Every automated decision must be reviewable and overridable by a human analyst, and the review must be logged.
> - The whole system must come up with `docker compose up` on a machine with no internet access (models and wheels pre-pulled).
>
> **Stack:** React.js + Material UI + Plotly/Recharts · FastAPI (Python 3.11) + Uvicorn · scikit-learn, XGBoost, LightGBM, PyTorch · Ollama (Llama 3 / Qwen / Mistral) · LangGraph or a custom finite-state engine · PostgreSQL, Redis, Celery · optional Hyperledger Fabric audit ledger · Docker Compose.
>
> **Working rules:** Produce runnable code, not pseudocode. Ask me before inventing a schema field or a business rule. At the end of each phase, output the acceptance checklist with pass/fail and the exact commands I run to verify. Do not start the next phase until I say so.

---

## Phase 0 — Skeleton and air-gap proof

> Set up the monorepo and the offline deployment shell. No ML yet.
>
> Deliver: repo layout (`backend/`, `frontend/`, `ml/`, `agents/`, `infra/`, `data/`, `docs/`), FastAPI app with `/health` and OpenAPI, Postgres + Redis + Ollama services in `docker-compose.yml`, `.env.example`, pinned `requirements.txt`, a `scripts/prefetch.sh` that downloads every wheel, npm package and Ollama model into a local cache, and structured JSON logging.

**Gate:** `docker compose up` succeeds · `/health` returns 200 with Postgres/Redis/Ollama connectivity · the stack starts again with networking disabled.

---

## Phase 1 — Data foundation

> Build the transaction data layer and a synthetic dataset, since real banking data isn't available.
>
> Deliver: normalized Postgres schema (`customers`, `accounts`, `transactions`, `alerts`, `cases`, `case_events`, `model_runs`), Alembic migrations, a synthetic generator producing ~500k transactions with configurable injected typologies — card fraud bursts, structuring/smurfing under the reporting threshold, layering chains, mule fan-in/fan-out, synthetic-identity accounts — with ground-truth labels, plus a batch CSV ingestion endpoint with validation and a feature engineering module (velocity, amount z-scores, geo/device mismatch, counterparty novelty, time-of-day entropy).

**Gate:** generator is seeded and reproducible · class balance and typology counts reported · feature pipeline runs on the full set without leakage of label-derived fields.

---

## Phase 2 — ML detection engine + XAI

> Train and serve the supervised and unsupervised fraud models.
>
> Deliver: training pipeline for XGBoost, LightGBM and Random Forest with stratified CV; a PyTorch autoencoder for unlabeled anomaly scoring; a calibrated ensemble producing a single 0–100 risk score; SHAP explainer with cached background data; model registry with versioning; `POST /score` (single + batch) returning score, band, top contributing features, and model version.

**Gate:** precision/recall/PR-AUC reported per typology, not just overall · scoring latency under 200 ms single-transaction · SHAP values returned for every scored record · false-positive rate compared against a rule-based baseline you also implement.

> **Note:** the rule-based baseline is not optional overhead. "Reduces false positives" is the project's headline claim and is unsupported without a measured comparison.

---

## Phase 3 — AML graph engine

> Add the multi-hop relationship analytics that rule engines can't do.
>
> Deliver: graph construction from transactions (NetworkX or Neo4j-free adjacency in Postgres), typology detectors for structuring, layering chains, circular flows, mule fan-in/fan-out and rapid pass-through; community detection; account risk propagation over k hops; `GET /graph/{account_id}?depth=n` returning nodes/edges/annotations sized for frontend rendering.

**Gate:** each detector validated against the injected ground truth from Phase 1 with recall reported · depth-3 subgraph query returns in under 2 s.

---

## Phase 4 — Offline LLM layer

> Wire Ollama in as a constrained reasoning and writing component — never as the decision-maker.
>
> Deliver: Ollama client with timeout, retry and token budgeting; a prompt template library with strict output schemas (JSON or Pydantic-validated); a grounding contract where the LLM only receives structured facts already produced by Phases 2–3 and is instructed to cite them; hallucination guard that rejects any narrative containing a number absent from the input facts; graceful degradation to templated text if the model is unavailable.

**Gate:** 50 narrative generations produce zero unsupported numeric claims · tokens/sec and memory footprint documented for each candidate model so the model choice is justified.

---

## Phase 5 — Agentic orchestration

> Implement the 8 investigation agents as a deterministic state machine. Each agent has a typed input, a typed output, a retry policy and a bounded step budget.
>
> Agents:
> 1. **Triage** — routes alert by score, typology, amount
> 2. **Customer Context** — KYC profile, account age, historical baseline
> 3. **Transaction History** — temporal patterns, peer comparison
> 4. **Network** — calls the graph engine, summarizes topology
> 5. **Watchlist** — local sanctions/PEP list matching, fuzzy name match
> 6. **Behavioral Anomaly** — autoencoder + deviation from the customer's own baseline
> 7. **Narrative Synthesis** — LLM-composed investigation summary grounded in agents 2–6
> 8. **Compliance QA** — checks the narrative for completeness against SAR field requirements, flags gaps
>
> Deliver: LangGraph or custom FSM with explicit state transitions, Celery workers for async execution, per-agent provenance so every claim traces to a source, full run trace persisted, and hard stop conditions preventing loops.

**Gate:** an alert flows end-to-end producing a complete investigation dossier · the run trace is replayable · a deliberately failing agent degrades the dossier instead of crashing the run.

---

## Phase 6 — SAR generation and human-in-the-loop

> Turn dossiers into regulator-ready output with analyst control.
>
> Deliver: SAR template mapped to actual FIU-IND / FinCEN field structure; auto-population from the dossier with confidence flags on inferred fields; case lifecycle (`open → investigating → escalated → SAR filed / dismissed`); analyst actions (approve, edit, reject, reassign, annotate) each writing an immutable `case_event`; feedback capture so analyst dispositions become future training labels; PDF/DOCX export.

**Gate:** no SAR exportable without an explicit analyst approval event · every field traceable to its source agent · the feedback loop writes labels the Phase 2 retraining script can consume.

---

## Phase 7 — Analyst dashboard

> Build the React frontend. Design for an analyst clearing a queue under time pressure, not for a demo.
>
> Deliver: alert queue with sorting, filtering and bulk triage; alert detail view with the SHAP waterfall, the agent dossier and the network graph side by side; interactive Plotly/Recharts graph with expand-on-click and typology highlighting; SAR editor with diff-against-generated view; case timeline; model performance page showing drift and FP rate over time; WebSocket live updates.

**Gate:** queue to approved SAR in under 8 clicks · graph view responsive at 500 nodes · no component fetches from any external CDN.

---

## Phase 8 — Audit ledger, hardening and evaluation

> Close it out for defense and for the report.
>
> Deliver: optional Hyperledger Fabric chaincode writing hashes of model runs and analyst decisions with a verification endpoint (and a Merkle-hash-chain fallback in Postgres if Fabric is dropped); RBAC (analyst / supervisor / admin); PII encryption at rest and log redaction; an evaluation harness producing the results table — your system vs the rule-based baseline on precision, recall, F1, FP rate, mean investigation time; load test; and `docs/` with architecture diagram, API reference, deployment runbook and a limitations section.

**Gate:** tamper-evidence demonstrated by mutating a record and showing verification fails · the full offline install reproduced on a clean machine from the runbook alone.

> **Note:** Hyperledger is the likeliest component to eat a week for little marginal credit. The Merkle-chain fallback gives the same tamper-evidence story at a fraction of the cost.

---

## Phase dependency map

```
Phase 0 ──► Phase 1 ──┬──► Phase 2 ──┐
                      │              ├──► Phase 5 ──► Phase 6 ──► Phase 7 ──► Phase 8
                      └──► Phase 3 ──┤
                           Phase 4 ──┘
```

Phases 2, 3 and 4 can run in parallel across team members once Phase 1 lands. Phases 5 onward are sequential.
