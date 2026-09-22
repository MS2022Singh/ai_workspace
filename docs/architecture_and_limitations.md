# AI Workspace Core: Architecture & Documentation

## 1. What Was Done
We engineered a secure, modular, event-driven runtime environment for multi-agent AI collaboration. The system comprises:
* **Event Bus:** An internal state machine managing task lifecycles (IDLE, PLANNING, EXECUTING, etc.).
* **Permission Engine:** A granular security layer restricting agent capabilities across 7 risk classes (e.g., READ, WRITE, SYSTEM).
* **Multi-Agent Orchestrator:** A coordinator that delegates tasks to specialized AI profiles based on authorized permissions.
* **Tool Registry & Sandbox:** A secure execution wrapper for running isolated code and tools.
* **Project Memory:** A persistent JSON-based governance tracker for requirements, decisions, progress, and issues.
* **Dashboard UI:** A FastAPI backend and HTML/JS frontend to monitor the workspace state in real-time.

## 2. Why It Was Done
To provide a strictly governed, isolated environment where AI agents can safely execute code, manage files, and track complex project lifecycles without hallucinating state or overstepping system permissions. 

## 3. Important Decisions
* **Event-Driven Decoupling:** Chosen to ensure agents and tools operate asynchronously without blocking the main runtime thread.
* **Default-Deny Permissions:** High-risk actions (DELETE, SYSTEM, FINANCIAL) are structurally blocked unless explicit user authorization is passed through the Orchestrator.
* **JSON State Persistence:** Selected for lightweight, human-readable state tracking without the overhead of a relational database during the core prototyping phase.
* **Subprocess Sandboxing:** Utilized native Python `subprocess` modules for initial isolation, paving the way for future Docker containerization.

## 4. Testing & Verification
* **Module Testing:** Each core component (Event Bus, Permission Engine, Orchestrator) was unit-tested via PowerShell Python execution checks.
* **Integration Testing:** `main.py` validated the end-to-end flow from planning to isolated sandbox execution (verifying the local Python version).
* **UI Verification:** FastAPI endpoints were tested via `uvicorn`, successfully serving the React-style HTML dashboard and live API polling.

## 5. Current Limitations
* **Sandbox Isolation:** Currently relies on local OS subprocess execution. True isolation requires migrating `sandbox_runner.py` to target Docker daemons.
* **Concurrency:** The JSON-based `ProjectMemory` lacks file-locking mechanisms for high-concurrency writes (e.g., if dozens of agents write to memory simultaneously). Future upgrades should migrate this to SQLite.
* **Agent Intelligence:** The current Orchestrator registers agent profiles but requires integration with an LLM inference API (like Gemini or OpenAI) to autonomously generate the plans it executes.
