"""
Renders the scene.
"""

import math

# Panda3D
from direct.showbase import ShowBase
from direct.task import Task
from panda3d import core

import cv2
import numpy as np


class Renderer(ShowBase.ShowBase):
    """
    Wrapper for the application that renders the scene.
    """

    def __init__(self) -> None:
        """
        Constructor.
        """
        ShowBase.ShowBase.__init__(self)

        # Load the environment model
        assert self.loader is not None
        self.scene = self.loader.loadModel("models/environment")

        # Reparent the model to render
        self.scene.reparentTo(self.render)

        # Apply scale and position transforms on the model
        self.scene.setScale(0.25, 0.25, 0.25)
        self.scene.setPos(-8, 42, 0)

        # For output images
        self.texture = core.Texture()
        self.win.addRenderTexture(
            self.texture, core.GraphicsOutput.RTMCopyRam, core.GraphicsOutput.RTPColor
        )

        self.taskMgr.add(
            self.set_camera_position_and_orientation,
            "set_camera_position_and_orientation",
        )
        self.taskMgr.add(self.display_image, "display_image")

    def set_camera_position_and_orientation(self, task: object) -> int:
        """
        Rotates the camera.

        task: Task metadata for renderer.
        """
        angle_degrees = task.time * 6.0
        angle_radians = math.radians(angle_degrees)

        self.camera.setPos(20 * math.sin(angle_radians), -20 * math.cos(angle_radians), 3)
        self.camera.setHpr(angle_degrees, 0, 0)

        return Task.cont

    def display_image(self, _: object) -> int:
        """
        Display the camera image in a new window.
        """
        if not self.texture.mightHaveRamImage():
            print("No image :(")
            return Task.cont

        width, height = self.win.size
        data = self.texture.getRamImage().getData()

        image = np.frombuffer(data, dtype=np.uint8)
        image = np.reshape(image, (height, width, 4))
        image = cv2.flip(image, 0)

        cv2.imshow("Camera", image)
        cv2.waitKey(1)

        return Task.cont
