# Project Folder Structure Guide

This guide describes the recommended folder structure for your Playwright + pytest + Allure + GCS automation project. Use this as a reference for further development and scaling.

## Root Directory
```
project-root/
├── .env                   # Environment variables
├── .env.example           # Example env file
├── .pytest_cache/         # Pytest cache (auto-generated)
├── Dockerfile             # Container setup
├── POM_README.md          # Page Object Model documentation
├── __pycache__/           # Python cache (auto-generated)
├── allure-results/        # Allure raw results (auto-generated)
├── config/                # Environment and settings files
│   ├── __init__.py
│   ├── __pycache__/
│   ├── env.py
│   └── settings.py
├── conftest.py            # Pytest configuration and hooks
├── core/                  # Core utilities and test infrastructure
│   ├── playwright/
│   │   ├── __pycache__/
│   │   ├── auth.py
│   │   ├── browser.py
│   │   ├── context.py
│   │   └── failures.py
│   └── utils/
│       ├── __pycache__/
│       └── gcs_uploader.py
├── docker-compose.yml     # Docker Compose setup
├── docs/                  # Documentation and guides
│   ├── ALLURE_REPORT_UPLOAD.md
│   ├── FOLDER_STRUCTURE.md
│   ├── GCS_QUICKSTART.md
│   ├── GCS_SETUP.md
│   └── LOCAL_CLEANUP.md
├── fixtures/              # Test data and pytest fixtures
│   ├── __init__.py
│   ├── __pycache__/
│   ├── page_fixtures.py
│   └── test_data.py
├── flows/                 # Business flows (multi-page scenarios)
│   ├── __init__.py
│   ├── __pycache__/
│   └── login_flow.py
├── pages/                 # Page Object Model classes
│   ├── __init__.py
│   ├── __pycache__/
│   ├── base_page.py
│   ├── login_page.py
│   └── otp_page.py
├── pytest.ini             # Pytest configuration
├── requirements.txt       # Python dependencies
├── screenshots/           # Screenshots storage
│   ├── .DS_Store
│   └── failures/
├── scripts/               # Helper scripts and API endpoints
│   ├── __pycache__/
│   ├── create_storage_state.py
│   ├── generate_and_upload_report.sh
│   ├── test_gcs_connection.py
│   ├── test_login.py
│   ├── test_runner_api.py
│   └── upload_allure_report.py
├── tests/                 # Test files organized by feature
│   ├── __pycache__/
│   └── login/
│       ├── __pycache__/
│       └── test_login.py
├── venv/                  # Python virtual environment
├── videos/                # Video recordings
│   ├── 606971af853a856b769c85bc139e0066.webm
│   └── 6a06d2cd253445f00098a98ff84edb85.webm
```

## Folder Purpose
- **config/**: Centralized environment and settings management.
- **core/**: Core utilities, browser setup, and reusable infrastructure.
- **docs/**: Project documentation, setup guides, and workflow explanations.
- **flows/**: High-level business flows combining multiple page objects.
- **fixtures/**: Pytest fixtures and test data for easy reuse.
- **pages/**: Page Object Model classes for UI abstraction.
- **scripts/**: Helper scripts, FastAPI endpoints, and automation tools.
- **tests/**: Actual test files, organized by feature or type.
- **screenshots/**: Stores screenshots, with a subfolder for failures.
- **videos/**: Stores video recordings of test runs.
- **allure-results/**: Raw Allure results (do not commit).
- **venv/**: Python virtual environment (do not commit).

## Best Practices
- Keep test data and fixtures separate for maintainability.
- Use Page Object Model for all UI interactions.
- Organize tests by feature or flow for scalability.
- Store documentation and setup guides in `docs/` for team reference.
- Use scripts for automation, report generation, and cloud uploads.
- Do not commit `allure-results/` or `allure-report/` to version control.

- Add new flows to `flows/` and new page objects to `pages/`.
- Add new test files under `tests/` in feature-specific folders.
- Extend `scripts/` for new automation or API endpoints.
- Update `docs/` with new guides as your workflow evolves.
- Use `screenshots/` and `videos/` for artifact management and debugging.

---

Feel free to customize this structure as your project grows!
