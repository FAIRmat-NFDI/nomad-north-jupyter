def test_importing_north_tool():
    # this will raise an exception if pydantic model validation fails for the north tool
    from nomad_north_jupyter.north_tools.my_north_tool import (
        north_tool,
    )

    assert (
        north_tool.id_url_safe == 'nomad_north_jupyter_my_north_tool'
        or north_tool.id == 'nomad-north-nomad-north-jupyter'
    ), 'NORTHtool entry point has incorrect id or id_url_safe'
