# NOMAD NORTH Jupyter Plugin - AI Copilot Instructions

## Project Overview

`nomad-north-jupyter` is a NOMAD plugin that provides a containerized Jupyter-based NORTH tool. It's a template-generated plugin (via Cookiecutter) that extends NOMAD with remote compute capabilities, allowing users to interact with Jupyter notebooks in the NOMAD Oasis environment.

**Key Integration Point**: This plugin bridges NOMAD (scientific data infrastructure) with JupyterLab, exposing Jupyter notebooks as a remote tool within NOMAD's ecosystem.

## Architecture

### Component Layers

- **Entry Point Layer** (`src/nomad_north_jupyter/north_tools/my_north_tool/__init__.py`): Defines the `NORTHTool` configuration object using Pydantic models from `nomad.config.models`. This is the integration glue with NOMAD.
- **Docker Container** (`Dockerfile`): Self-contained JupyterLab environment with UV package manager for reproducible builds.
- **Plugin Structure** (`src/nomad_north_jupyter/`): Python package that NOMAD loads as an entry point.

### Data Flow

1. NOMAD Oasis loads this plugin via entry point discovery
2. Plugin exposes the `north_tool` object (Pydantic model) defining JupyterLab configuration
3. NOMAD instantiates the Docker container with specified parameters
4. Users access Jupyter at configured paths (`/lab`, with `path_prefix='lab/tree'`)

## File Reference Guide

| File/Dir                                                        | Purpose                                                                                     | Key Patterns                                                                  |
| --------------------------------------------------------------- | ------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| `src/nomad_north_jupyter/north_tools/my_north_tool/__init__.py` | **Critical**: Defines NORTHTool entry point; must validate against NOMAD's Pydantic models  | Immutable configuration object; no business logic                             |
| `src/nomad_north_jupyter/north_tools/my_north_tool/Dockerfile`  | **Critical**: JupyterLab runtime; uses UV for deterministic builds, base-notebook as parent | Multi-stage build; `UV_NO_CACHE=1` for reproducibility                        |
| `tests/north_tools/test_north_tools.py`                         | Validates Pydantic model schema compliance                                                  | Imports `north_tool` object; checks `id_url_safe` constraint                  |
| `pyproject.toml`                                                | Project metadata and dependencies                                                           | Supports Python 3.10-3.12; uses UV extra index for NOMAD packages from GitLab |
| `docs/`                                                         | MkDocs-generated documentation                                                              | Material theme; structured as tutorial/how-to/reference                       |

## Development Workflow

### Setup

```bash
python3.11 -m venv .pyenv && . .pyenv/bin/activate
pip install --upgrade pip && pip install uv
uv pip install -e '.[dev]'
```

### Testing

```bash
python -m pytest -sv tests                    # Run tests with verbose output
python -m pytest --cov=src tests              # Coverage report
```

### Code Quality

```bash
ruff check .                                   # Linting
ruff format . --check                          # Format check
ruff format .                                  # Auto-format
```

**Convention**: Ruff is configured in `pyproject.toml` with E, F, UP, I, PL rules (PEP8, Pyflakes, pyupgrade, isort, pylint). Auto-formatting applies on VSCode save via `.vscode/settings.json`.

### Documentation

```bash
uv pip install -r requirements_docs.txt
mkdocs serve                                   # Local docs at http://localhost:8000
```

### Docker Testing

```bash
docker build -f src/nomad_north_jupyter/north_tools/my_north_tool/Dockerfile \
    -t ghcr.io/fairmat-nfdi/nomad-north-jupyter:latest .
docker run -p 8888:8888 ghcr.io/fairmat-nfdi/nomad-north-jupyter:latest
```

## Critical Patterns

### NORTHTool Configuration Model

The `north_tool` object in `__init__.py` is a Pydantic model from NOMAD. Key properties:

- `id_url_safe='nomad_north_jupyter_my_north_tool'`: Must be unique and URL-safe; used by NOMAD registry
- `image='ghcr.io/fairmat-nfdi/nomad-north-jupyter/jupyter:latest'`: Docker image URI
- `file_extensions=['ipynb']`: Limits tool access to Jupyter notebooks
- `mount_path='/home/jovyan'`: Container mount point (Jupyter standard)
- `path_prefix='lab/tree'`: URL routing prefix within NOMAD

**Testing**: `test_north_tools.py` imports and validates; Pydantic schema errors bubble up immediately.

### Dockerfile Conventions

- **Multi-stage**: UV installation stage reduces final image size
- **Cache busting**: `UV_NO_CACHE=1` ensures reproducible builds (no cached wheels)
- **User context**: Runs as `${NB_USER}` (jovyan) for Jupyter security model
- **Node.js 24**: Required for JupyterLab >= 4.4.10 (explicit version management)

### Dependency Management

- **NOMAD packages**: Fetched from `https://gitlab.mpcdf.mpg.de/api/v4/projects/2187/packages/pypi/simple` (GitLab private package index)
- **Development split**: `:dev` includes linting/testing; `[north]` dependency group contains JupyterLab/ipywidgets
- **Python version**: 3.10–3.12 supported; 3.11 is development standard

## Integration Points

### External Dependencies

- **nomad-lab**: Core NOMAD package (develop branch); provides `nomad.config.models` for Pydantic schemas
- **jupyterlab**: JupyterLab runtime (base-notebook parent image includes it)
- **UV**: Fast Python package manager; configured for Conda integration

### Deployment Contexts

1. **NOMAD Oasis**: User's private NOMAD instance; plugin installed via deployment mechanism
2. **Local NOMAD development**: Use `nomad-distro-dev` repository (see README)

## Common Tasks

### Adding a New NORTH Tool

1. Create `src/nomad_north_jupyter/north_tools/your_tool_name/__init__.py`
2. Define `NORTHTool` and wrap in `NorthToolEntryPoint`
3. Add test in `tests/north_tools/test_north_tools.py`
4. Reference in documentation

### Modifying JupyterLab Environment

- **Packages**: Add to `[dependency-groups.north]` in `pyproject.toml`
- **System libraries**: Add to `apt-get install` in Dockerfile
- **Rebuild**: `docker build` with new tag; update `image` URI in `__init__.py`

### Updating Documentation

- Add `.md` files to `docs/` subdirectories (tutorial/how_to/explanation/reference)
- Navigation defined in `mkdocs.yml`; regenerates on `mkdocs serve`

## Version & Template Management

- **Generated from**: `@nomad`'s `cookiecutter-nomad-plugin` template
- **Update mechanism**: Use `cruft update` to sync with template changes
- **Version**: 0.1.0 (semantic versioning in `pyproject.toml`)
