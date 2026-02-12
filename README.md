# NORTH Jupyter tool

This directory contains the NORTH tool configuration and Docker image for a Jupyter-based tool in the NOMAD NORTH (NOMAD Oasis Remote Tools Hub) environment. The  [Dockerfile](https://github.com/FAIRmat-NFDI/cookiecutter-nomad-plugin/blob/main/%7B%7Bcookiecutter.plugin_name%7D%7D/py_sources/src/north_tools/%7B%7Bcookiecutter.north_tool_name%7D%7D/Dockerfile)  an be used as a basis to define custom Jupyter NORTH tools.

## Quick start

The `jupyter_north_tool` NORTH tool provides a containerized JupyterLab environment for interactive analysis with the `nomad-north-jupyter` plugin.

## Building and testing

Build the Docker image locally:

```bash
docker build -f src/nomad_north_jupyter/north_tools/jupyter_north_tool/Dockerfile \
    -t ghcr.io/fairmat-nfdi/nomad-north-jupyter:latest .
```

Test the image:

```bash
docker run -p 8888:8888 ghcr.io/fairmat-nfdi/nomad-north-jupyter:latest
```

Access JupyterLab at `http://localhost:8888`.

## Using `nomad-north-jupyter` as a base image

This image is designed to be used as a base for custom NOMAD NORTH Jupyter tools. When extending this image in your plugin's Dockerfile, keep the following in mind:

### Package management

Both `uv` and `pip` are available as package managers in the image. Both install and uninstall packages in the Conda environment, so you can use either one of them to manage your Python dependencies.

**Example using uv:**
```dockerfile
RUN uv pip install numpy pandas scipy
```

**Example using pip:**
```dockerfile
RUN pip install --no-cache-dir matplotlib seaborn
```

### Port and user configuration

Like other Jupyter notebook images, port `8888` is exposed for JupyterLab access. The default user is `${NB_USER}` (usually `jovyan`), and you should switch to this user when installing packages or copying files to ensure proper permissions.

### Fixing permissions

After customizing the base image (e.g., installing additional packages or adding files), you may need to fix file permissions to avoid permission issues when running the container. Add the following lines at the end of your Dockerfile after all customizations:

```dockerfile
COPY --chown=${NB_USER}:${NB_GID} . ${HOME}/${PLUGIN_NAME}
RUN fix-permissions "/home/${NB_USER}" \
    && fix-permissions "${CONDA_DIR}"
```

**Complete example Dockerfile:**
```dockerfile
ARG IMAGE_TAG=latest
FROM ghcr.io/fairmat-nfdi/nomad-north-jupyter:${IMAGE_TAG}

USER root

# Install system dependencies (if needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    graphviz \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER ${NB_USER}

# Install Python packages
RUN uv pip install numpy pandas matplotlib

# Copy your plugin files
COPY --chown=${NB_USER}:${NB_GID} . ${HOME}/${PLUGIN_NAME}

# Fix permissions
RUN fix-permissions "/home/${NB_USER}" \
    && fix-permissions "${CONDA_DIR}"
```

## Documentation

For comprehensive documentation on creating and managing NORTH tools, including detailed information on topics such as:

- Entry point configuration and `NORTHTool` API
- Docker image structure and best practices
- Dependency management

See the [NOMAD NORTH Tools documentation](https://fairmat-nfdi.github.io/nomad-docs/howto/plugins/types/north_tools.html).