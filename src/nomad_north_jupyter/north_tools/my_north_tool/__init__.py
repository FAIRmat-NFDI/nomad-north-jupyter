from nomad.config.models.north import NORTHTool
from nomad.config.models.plugins import NorthToolEntryPoint

tool = NORTHTool(
    short_description='Jupyter Notebook server in NOMAD NORTH for NOMAD plugin nomad-north-jupyter.',
    image='ghcr.io/fairmat-nfdi/nomad-north-jupyter/jupyter:latest',
    description='Jupyter Notebook server in NOMAD NORTH for NOMAD plugin nomad-north-jupyter.',
    external_mounts=[],
    file_extensions=['ipynb'],
    icon='logo/jupyter.svg',
    image_pull_policy='Always',
    default_url='/lab',
    maintainer=[{'email': 'john.doe@physik.hu-berlin.de', 'name': 'John Doe'}],
    mount_path='/home/jovyan',
    path_prefix='lab/tree',
    privileged=False,
    with_path=True,
    display_name='my_north_tool',
)

north_tool = NorthToolEntryPoint(
    id_url_safe='nomad_north_jupyter_my_north_tool', north_tool=tool
)
