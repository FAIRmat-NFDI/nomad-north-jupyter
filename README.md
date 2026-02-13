# NORTH Jupyter tool

This `nomad-north-jupyter` is a NOMAD plugin and can be used along with other NOMAD plugins, in `[nomad-distro-dev](https://github.com/FAIRmat-NFDI/nomad-distro-dev)`, `[nomad-distro-template](https://github.com/FAIRmat-NFDI/nomad-distro-template)`, and in NOMAD production instance. Adding it in plugin orchestration will make the `jupyter_north_tool` available in the NORTH tools registry of the NOMAD Oasis environment. The tool provides a containerized Jupyter Notebook environment for interactive analysis.

The plugin contains the NORTH tool configuration and Docker image for a Jupyter-based tool in the NOMAD NORTH (NOMAD Oasis Remote Tools Hub) environment. The `[nomad-north-jupyter image](https://github.com/FAIRmat-NFDI/nomad-north-jupyter/pkgs/container/nomad-north-jupyter)` from this plugin provides the default base image for [Dockerfile](https://github.com/FAIRmat-NFDI/cookiecutter-nomad-plugin/blob/main/%7B%7Bcookiecutter.plugin_name%7D%7D/py_sources/src/north_tools/%7B%7Bcookiecutter.north_tool_name%7D%7D/Dockerfile) be used as a basis to define custom Jupyter NORTH tools.

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
## Adding this plugin to NOMAD

Currently, NOMAD has two distinct flavors that are relevant depending on your role as an user:

1. [A NOMAD Oasis](#adding-this-plugin-in-your-nomad-oasis): any user with a NOMAD Oasis instance.
2. [Local NOMAD installation and the source code of NOMAD](#adding-this-plugin-in-your-local-nomad-installation-and-the-source-code-of-nomad): internal developers.

### Adding this plugin in your NOMAD Oasis

Read the [NOMAD plugin documentation](https://nomad-lab.eu/prod/v1/staging/docs/howto/oasis/plugins_install.html) for all details on how to deploy the plugin on your NOMAD instance.

### Adding this plugin in your local NOMAD installation and the source code of NOMAD

We now recommend using the dedicated [`nomad-distro-dev`](https://github.com/FAIRmat-NFDI/nomad-distro-dev) repository to simplify the process. Please refer to that repository for detailed instructions.

## Documentation

For comprehensive documentation on creating and managing NORTH tools, including detailed information on topics such as:

- Entry point configuration and `NORTHTool` API
- Docker image structure and best practices
- Dependency management

See the [NOMAD NORTH Tools documentation](https://fairmat-nfdi.github.io/nomad-docs/howto/plugins/types/north_tools.html).