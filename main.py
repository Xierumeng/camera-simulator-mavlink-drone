"""
Program entry.
"""

import math
import pathlib

from modules.renderer import renderer


if __name__ == "__main__":
    model_load_data = renderer.ModelLoadData(
        pathlib.Path("models/uw_e56710/uw_e56710.obj"),
        1,
        1,
        1,
        52,
        6,
        11,
        0,
        math.degrees(math.pi / 2),
        0,
    )
    result, r = renderer.Renderer.create(model_load_data)
    if not result:
        exit()

    # Get Pylance to stop complaining
    assert r is not None

    r.run()
