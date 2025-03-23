"""
Program entry.
"""

from modules.renderer import renderer


if __name__ == "__main__":
    renderer = renderer.Renderer()
    renderer.run()
