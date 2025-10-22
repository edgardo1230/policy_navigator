
# Copilot Instructions for policy-navigator

This guide enables AI coding agents to be productive in the `policy-navigator` codebase. It summarizes architecture, workflows, and conventions unique to this project.

## Architecture Overview
- **Agent-centric design:** Core logic is in `app/agent.py` (agent/tool definitions, environment config) and `app/agent_engine_app.py` (deployment, logging, feedback, tracing). Utilities are in `app/utils/`.
- **Streamlit UI:** Local prototyping uses Streamlit, launched via `make playground` (runs `adk web`).
- **Infrastructure-as-Code:** All GCP resources and CI/CD are managed via Terraform in `deployment/terraform/` (main configs) and `deployment/terraform/dev/` (env overrides).
- **Notebook-driven prototyping:** Use `notebooks/` for evaluation and experimentation; launch with `uv run jupyter lab`.
- **Testing:** Tests are split into `unit/`, `integration/`, and `load_test/` under `tests/`. Load tests use Locust and require a separate venv.

## Developer Workflows
- **Install dependencies:** Use `make install` (uses `uv` for Python package management; do not use `pip` or `conda`).
- **Run locally:** `make playground` launches the Streamlit interface for agent testing.
- **Deploy backend:** `make backend` deploys the agent to Agent Engine (GCP Vertex AI). Exports requirements with `uv export` and runs `app/agent_engine_app.py`.
- **Run tests:** `make test` for unit/integration; see `tests/load_test/README.md` for load testing with Locust. Results are saved in `tests/load_test/.results/`.
- **Linting:** `make lint` runs codespell, ruff, and mypy.
- **Setup dev infra:** `make setup-dev-env` provisions GCP resources via Terraform.
- **Jupyter:** `uv run jupyter lab` launches notebooks for prototyping.

## Project Conventions
- **Dependency management:** Use only `uv` for Python packages. All dependencies are managed in `pyproject.toml` and `requirements.txt` (auto-generated). Never use `pip` or `conda` directly.
- **Environment variables:** All config is loaded from `.env` via `dotenv` in `app/agent.py`. Key variables: `GOOGLE_CLOUD_PROJECT`, `LOCATION`, `COLLECTION_ID`, and app IDs for each engine.
- **Instructions for agents:** See `app/instructions.py` for canonical agent prompt and behavioral rules.
- **Makefile is canonical:** Always check the Makefile for supported commands and workflow automation.

## Integration Points
- **Google Cloud Platform:** All deployment and CI/CD are GCP-centric. Requires `gcloud` and Terraform. Backend targets Vertex AI Agent Engine.
- **Agent Engine:** Backend deployment targets Agent Engine (see `make backend`).
- **Locust:** Load testing uses Locust, isolated in its own virtual environment. See `tests/load_test/README.md` for details.
- **OpenTelemetry/Cloud Logging:** Observability is handled via OpenTelemetry, Cloud Trace, and Logging (see `app/utils/tracing.py`).

## Examples
- To run a load test:
  ```bash
  gcloud config set project <your-dev-project-id>
  make backend
  python3 -m venv .locust_env && source .locust_env/bin/activate && pip install locust==2.31.1
  export _AUTH_TOKEN=$(gcloud auth print-access-token -q)
  locust -f tests/load_test/load_test.py --headless -t 30s -u 5 -r 2 --csv=tests/load_test/.results/results --html=tests/load_test/.results/report.html
  ```

## Key Files & Directories
- `app/agent.py`, `app/agent_engine_app.py`: Main agent and deployment logic
- `app/instructions.py`: Canonical agent instructions
- `app/utils/`: Utility modules (deployment, GCS, tracing, typing)
- `deployment/terraform/`: Infrastructure configs (main and env-specific)
- `tests/`: All test types (unit, integration, load)
- `Makefile`: Workflow automation and canonical commands
- `notebooks/`: Prototyping and evaluation

---
If any section is unclear, incomplete, or missing, please provide feedback for improvement.