# NORTH Jupyter tool

This `nomad-north-jupyter` is a NOMAD plugin and can be used along with other NOMAD plugins, in [nomad-distro-dev](https://github.com/FAIRmat-NFDI/nomad-distro-dev), [nomad-distro-template](https://github.com/FAIRmat-NFDI/nomad-distro-template), and in NOMAD production instance. Adding it in plugin orchestration will make the `jupyter_north_tool` available in the NORTH tools registry of the NOMAD Oasis environment.

The plugin contains the NORTH tool configuration and Docker image for a Jupyter-based tool in the NOMAD NORTH (NOMAD Oasis Remote Tools Hub) environment. The [nomad-north-jupyter image](https://github.com/FAIRmat-NFDI/nomad-north-jupyter/pkgs/container/nomad-north-jupyter) from this plugin provides the default base image for [Dockerfile](https://github.com/FAIRmat-NFDI/cookiecutter-nomad-plugin/blob/main/%7B%7Bcookiecutter.plugin_name%7D%7D/py_sources/src/north_tools/%7B%7Bcookiecutter.north_tool_name%7D%7D/Dockerfile) be used as a basis to define custom Jupyter NORTH tools.


## Quick start

The `jupyter_north_tool` NORTH tool provides a containerized JupyterLab environment for interactive analysis with the `nomad-north-jupyter` plugin.

**In the following sections, we will cover:**
1. [Building and testing the Docker image locally](#building-and-testing)
1. [Using `nomad-north-jupyter` as a base image for custom NORTH tools](#using-nomad-north-jupyter-as-a-base-image-for-custom-north-tools)
   - [Package management](#package-management)
   - [Port and user configuration](#port-and-user-configuration)
   - [Fixing permissions](#fixing-permissions)
1. [Adding `nomad-north-jupyter` plugin to NOMAD](#adding-nomad-north-jupyter-plugin-to-nomad)
   - [Adding `nomad-north-jupyter` plugin in your NOMAD Oasis](#adding-nomad-north-jupyter-plugin-in-your-nomad-oasis)
   - [Adding `nomad-north-jupyter` plugin in your local NOMAD installation](#adding-nomad-north-jupyter-plugin-in-your-local-nomad-installation)
1. [Adding `nomad-north-jupyter` image in a NOMAD Oasis (alternative)](#adding-nomad-north-jupyter-image-in-a-nomad-oasis)
1. [Reconfigure existing NORTH tool entry point](#reconfigure-existing-north-tool-entry-point)
1. [Documentation](#documentation)
1. [Main contributors](#main-contributors)

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

## Using `nomad-north-jupyter` as a base image for custom NORTH tools

This image is designed to be used as a base for custom NOMAD NORTH Jupyter tools. When extending this image in your plugin's Dockerfile created from [cookiecutter-nomad-plugin](https://github.com/FAIRmat-NFDI/cookiecutter-nomad-plugin/), keep the following in mind:

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

## Adding `nomad-north-jupyter` plugin to NOMAD

Currently, NOMAD has two distinct flavors that are relevant depending on your role as an user:

### Adding `nomad-north-jupyter` plugin in your NOMAD Oasis

Read the [NOMAD plugin documentation](https://nomad-lab.eu/prod/v1/staging/docs/howto/oasis/plugins_install.html) for all details on how to deploy the plugin on your NOMAD instance.

### Adding `nomad-north-jupyter` plugin in your local NOMAD installation

We now recommend using the dedicated [`nomad-distro-dev`](https://github.com/FAIRmat-NFDI/nomad-distro-dev) repository to simplify the process. Please refer to that repository for detailed instructions.

## Adding `nomad-north-jupyter` image in a NOMAD Oasis

> [!WARNING]
> We strongly recommend integrating `nomad-north-jupyter` into NOMAD as a plugin. The following approach is only recommended if you have an existing NOMAD Oasis instance that you do not want to rebuild, but still want to add the Jupyter image to the running `north` service.

If you cannot use the plugin approach, you can add the `nomad-north-jupyter` image to your NORTH service by editing the `nomad.yaml` file in a [nomad-distro-template](https://github.com/FAIRmat-NFDI/nomad-distro-template) instance. Define the corresponding NORTH tool in `nomad.yaml` as shown below (see the full NORTH tool configuration in the [NOMAD documentation](https://nomad-lab.eu/prod/v1/docs/reference/config.html)):

```yaml
# Not a recommended way
north:
  jupyterhub_crypt_key: "978bfb2e13a8448a253c629d8dd84ffsd587f30e635b753153960930cad9d36d"
  tools:
    options:
      jupyter:
        image: ghcr.io/fairmat-nfdi/nomad-north-jupyter:latest
        description: "### **Jupyter Notebook**: The Classic Notebook Interface"
        file_extensions:
          - ipynb
        icon: jupyter_logo.svg
        image_pull_policy: Always
        maintainer:
          - email: fairmat@physik.hu-berlin.de
            name: NOMAD Authors
        mount_path: /home/jovyan
        path_prefix: lab/tree
        privileged: false
        short_description: ""
        with_path: true
```

> [!NOTE]
>  We strongly recommand integration of the Jupyter NORTH tool via the [`NorthToolEntryPoint`](https://nomad-lab.eu/prod/v1/docs/howto/plugins/types/north_tools.html#north-tool-entry-point), i.e., by installing `nomad-north-jupyter` into a deployment.

## Reconfigure existing NORTH tool entry point
The image shipped with `nomad-north-jupyter` is a generic Jupyter container that may be too simplistic for your use case. In that case, you can change to a different image to use in the container. A [`NORTHTool`](https://nomad-lab.eu/prod/v1/docs/reference/config.html#northtool) entry point can be reconfigured via the `nomad.yaml` configuration file of your NOMAD Oasis instance (you can learn more about this reconfiguration and the [merge strategy](https://nomad-lab.eu/prod/v1/docs/reference/config.html#merging-rules) in the NOMAD docs). Hence, If you have the `nomad-north-jupyter` plugin installed, you can do so by adjusting the entry point configuration in your `nomad.yaml` file:

```yaml
plugins:
  entry_points:
    options:
      nomad_north_jupyter.north_tools.jupyter_north_tool:north_tool_entry_point:
        north_tool:
          image: ghcr.io/fairmat-nfdi/nomad-north-jupyter:<another_tag>
          display_name: "Renamed Jupyter"
```

## Documentation

For comprehensive documentation on creating and managing NORTH tools, including detailed information on topics such as:

- Entry point configuration and `NORTHTool` API
- Docker image structure and best practices
- Dependency management

See the [NOMAD NORTH Tools documentation](https://fairmat-nfdi.github.io/nomad-docs/howto/plugins/types/north_tools.html).

> [!NOTE]
> This `nomad` plugin was generated with `Cookiecutter` along with `@nomad`'s [`cookiecutter-nomad-plugin`](https://github.com/FAIRmat-NFDI/cookiecutter-nomad-plugin) template.

## Main contributors

| Name          | E-mail                                                            |
| ------------- | ----------------------------------------------------------------- |
| NOMAD Authors | [fairmat@physik.hu-berlin.de](mailto:fairmat@physik.hu-berlin.de)