"""
Program entry.
"""

import math
import pathlib

from modules.renderer import renderer


def main() -> int:
    """
    Main function.
    """
    # Rotate the model so that it is in the NED coordinate system
    model_load_data = renderer.ModelLoadData(
        pathlib.Path("models/uw_e56710/uw_e56710.obj"),
        renderer.ModelLoadData.Scale(1, 1, 1),
        renderer.ModelLoadData.Rotation(math.degrees(math.pi / 2), math.degrees(-math.pi / 2), 0),
        renderer.ModelLoadData.Position(7, 53, -11),
    )
    result, r = renderer.Renderer.create(model_load_data)
    if not result:
        return -1

    # Get Pylance to stop complaining
    assert r is not None

    r.run()

    return 0


if __name__ == "__main__":
    result_main = main()
    if result_main != 0:
        print(f"ERROR: Status code: {result_main}")

    print("Done!")
