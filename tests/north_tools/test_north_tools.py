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
from nomad_north_jupyter.north_tools.jupyter_north_tool import north_tool_entry_point


def test_importing_north_tool():
    assert (
        north_tool_entry_point.id_url_safe == 'nomad_north_jupyter_my_north_tool'
        or north_tool_entry_point.id == 'nomad-north-nomad-north-jupyter'
    ), 'NORTHtool entry point has incorrect id or id_url_safe'
