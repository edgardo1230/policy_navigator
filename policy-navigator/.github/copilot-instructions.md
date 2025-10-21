# Copilot Instructions for policy-navigator

This guide enables AI coding agents to be productive in the `policy-navigator` codebase. It summarizes architecture, workflows, and conventions unique to this project.

## Architecture Overview
- **Agent-centric design:** Core logic lives in `app/agent.py` and `app/agent_engine_app.py`. Utilities are in `app/utils/`.
- **Streamlit UI:** Local testing and prototyping use Streamlit, launched via `make playground`.
- **Infrastructure-as-Code:** All GCP resources and CI/CD are managed via Terraform in `deployment/terraform/`.
- **Notebook-driven prototyping:** Use `notebooks/` for evaluation and experimentation.
- **Testing:** Tests are split into `unit/`, `integration/`, and `load_test/` under `tests/`.

## Developer Workflows
- **Install dependencies:** Use `make install` (uses `uv` for Python package management).
- **Run locally:** `make playground` launches the Streamlit interface.
- **Deploy backend:** `make backend` deploys the agent to Agent Engine (GCP).
- **Run tests:** `make test` for unit/integration, see `tests/load_test/README.md` for load testing with Locust.
- **Linting:** `make lint` runs codespell, ruff, and mypy.
- **Setup dev infra:** `make setup-dev-env` provisions GCP resources via Terraform.
- **Jupyter:** `uv run jupyter lab` launches notebooks.

## Project Conventions
- **Dependency management:** Only use `uv` for Python packages. Do not use `pip` or `conda` directly.
- **Terraform structure:** Main configs in `deployment/terraform/`, environment-specific overrides in `deployment/terraform/dev/`.
- **Auth tokens:** For load tests, use `gcloud auth print-access-token` and export as `_AUTH_TOKEN`.
- **Results:** Load test results are saved as CSV/HTML in `tests/load_test/.results/`.
- **Makefile is canonical:** Always check the Makefile for supported commands and workflow automation.

## Integration Points
- **Google Cloud Platform:** All deployment and CI/CD are GCP-centric. Requires `gcloud` and Terraform.
- **Agent Engine:** Backend deployment targets Agent Engine (see `make backend`).
- **Locust:** Load testing uses Locust, isolated in its own virtual environment.

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
- `app/agent.py`, `app/agent_engine_app.py`: Main agent logic
- `app/utils/`: Utility modules
- `deployment/terraform/`: Infrastructure configs
- `tests/`: All test types
- `Makefile`: Workflow automation
- `notebooks/`: Prototyping and evaluation

---
If any section is unclear or missing, please provide feedback for improvement.