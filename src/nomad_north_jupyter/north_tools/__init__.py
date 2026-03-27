#
# Copyright The NOMAD Authors.
#
# This file is part of NOMAD. See https://nomad-lab.eu for further info.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from nomad.config.models.north import NORTHTool
from nomad.config.models.plugins import NorthToolEntryPoint

jupyter_north_tool = NORTHTool(
    image='ghcr.io/fairmat-nfdi/nomad-north-jupyter:main',
    description="""### **Jupyter Notebook**: The Classic Notebook Interface

    The Jupyter Notebook is the original web application for creating and sharing
    computational documents. It offers a simple, streamlined, document-centric
    experience.""",
    short_description='Jupyter Notebook server.',
    external_mounts=[],
    file_extensions=['ipynb'],
    icon=(
        'https://raw.githubusercontent.com/FAIRmat-NFDI/'
        'nomad-north-jupyter/main/src/nomad_north_jupyter/'
        'north_tools/jupyter_north_tool/jupyter.svg'
    ),
    image_pull_policy='Always',
    default_url='/lab',
    maintainer=[{'email': 'fairmat@physik.hu-berlin.de', 'name': 'The NOMAD Authors'}],
    mount_path='/home/jovyan',
    path_prefix='lab/tree',
    privileged=False,
    with_path=True,
    display_name='Jupyter',
)
jupyter = NorthToolEntryPoint(id_url_safe='jupyter', north_tool=jupyter_north_tool)
