# 🔌 Railway Multi-Cloud Migration Engine

A production-grade, multi-service automation tool built to eliminate the manual friction of migrating legacy application architecture (from platforms like Heroku or Render) directly onto Railway.

[![Deploy on Railway](https://railway.com/button.svg)](https://railway.com)

---

## 🧠 The Core Problem It Solves

Moving an application to a new cloud ecosystem is often plagued by manual mistakes. Developers typically struggle with:
* Determining configuration settings for alternative runtime builders.
* Exposing database instances to the public internet due to complex networking constraints.
* Manually rewriting legacy platform variables to match a new system interface.

**This engine automates that entire lifecycle.** It scans a raw repository, identifies language stacks and internal database clients, programmatically links isolated dependencies within an internal mesh topology, and outputs a one-click operational infrastructure blueprint.

---

## 🏗️ System Architecture Flow

This application operates as a distributed multi-service setup entirely hosted on **Railway**:

```text
               ┌──────────────────────┐
               │    Next.js UI        │  (Public Endpoint w/ SSL)
               └──────────┬───────────┘
                          │
                          │ (Internal Mesh Network)
                          ▼
┌──────────────┐  ┌──────────────────────┐  ┌──────────────┐
│  PostgreSQL  │◄─┤   Python/FastAPI     ├─►│  Nixpacks    │
│  (DB Cache)  │  │   Analysis Engine    │  │  Build Spec  │
└──────────────┘  └──────────────────────┘  └──────────────┘
```

1. **Dashboard Interface (`frontend/`):** A minimalist, responsive Tailwind dashboard handling request streaming.
2. **Analysis Engine (`backend/`):** A FastAPI microservice that clones repositories to isolated ephemeral memory and runs static code parsing.
3. **Analytics Cache:** A secured PostgreSQL plugin isolated entirely from the public internet.

---

## 🌟 High-Leverage Platform Features Showcased

This project explicitly skips standard "Hello World" boilerplate concepts to prove deep architectural mastery of Railway's core infrastructure engine:

* **Nixpacks Compilation Logic:** Dynamically generates targeted `nixpacks.toml` configurations for non-Dockerized monorepo systems.
* **Private Mesh Networking:** Implements platform-level cross-service variable references (`${{ migration-backend.RAILWAY_PRIVATE_DOMAIN }}`) to eliminate open API endpoints.
* **One-Click Blueprint Packaging:** Built entirely on a root `template.json` layout, enabling full deployment duplication in a single click.

---

## 🚀 How to Run this Locally

### 1. Boot up the Backend Core Engine
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### 2. View the Dashboard UI
Simply open `frontend/index.html` in your browser, paste any public repository link, and click **"Analyze Stack"**.

---
*Built as a core engineering portfolio submission for the Railway Senior DevRel Application process.*
