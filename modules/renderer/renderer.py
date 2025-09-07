"""
Renders the scene.
"""

import math
import pathlib

# Panda3D
from direct.showbase import ShowBase
from direct.task import Task
from panda3d import core

import cv2
import numpy as np


class ModelLoadData:
    """
    Model metadata for renderer.
    """

    class Scale:
        """
        Scaling of the model.
        """

        def __init__(self, x: float, y: float, z: float) -> None:
            """
            x, y, z: Scaling of the model.
            """
            self.x = x
            self.y = y
            self.z = z

    class Position:
        """
        Position of the model.
        """

        def __init__(self, x: float, y: float, z: float) -> None:
            """
            x, y, z: Position of the model.
            """
            self.x = x
            self.y = y
            self.z = z

    class Rotation:
        """
        Rotation of the model.
        """

        def __init__(self, h: float, p: float, r: float) -> None:
            """
            h, p, r: Rotation of the model. h is yaw but letter y is already used.
            """
            self.h = h
            self.p = p
            self.r = r

    def __init__(
        self,
        model_path: pathlib.Path,
        scale: Scale,
        position: Position,
        rotation: Rotation,
    ) -> None:
        """
        model_path: File path to model.
        scale: Scaling of the model.
        position: Position of the model.
        rotation: Rotation of the model.
        """
        self.model_path = model_path

        self.scale = scale
        self.position = position
        self.rotation = rotation


class Renderer(ShowBase.ShowBase):
    """
    Wrapper for the application that renders the scene.
    """

    __create_key = object()

    @classmethod
    def create(
        cls,
        model_load_data: ModelLoadData,
    ) -> "tuple[True, Renderer] | tuple[False, None]":
        """
        model_load_data: Model metadata for renderer.

        Return: Success, object.
        """
        return True, Renderer(cls.__create_key, model_load_data)

    def __init__(self, class_private_create_key: object, model_load_data: ModelLoadData) -> None:
        """
        Private constructor, use create() method.
        """
        assert class_private_create_key is Renderer.__create_key, "Use create() method"

        ShowBase.ShowBase.__init__(self)

        self.setBackgroundColor(0, 0, 0)

        self.__load_model(model_load_data)

        # For output images
        self.texture = core.Texture()
        self.win.addRenderTexture(
            self.texture, core.GraphicsOutput.RTMCopyRam, core.GraphicsOutput.RTPColor
        )

        # Tasks running continuously
        self.taskMgr.add(
            self.set_camera_position_and_orientation,
            "set_camera_position_and_orientation",
        )
        self.taskMgr.add(self.display_image, "display_image")

    def __load_model(self, model_load_data: ModelLoadData) -> None:
        """
        Load the model.

        model_load_data: Model metadata for renderer.

        Return: None.
        """
        model_path = core.Filename.fromOsSpecific(str(model_load_data.model_path))

        # Load the environment model
        assert self.loader is not None
        self.scene = self.loader.loadModel(model_path)

        # Reparent the model to render
        self.scene.reparentTo(self.render)

        # Apply transforms on the model
        self.scene.setScale(
            model_load_data.scale.x, model_load_data.scale.y, model_load_data.scale.z
        )
        self.scene.setPos(
            model_load_data.position.x, model_load_data.position.y, model_load_data.position.z
        )
        self.scene.setHpr(
            model_load_data.rotation.h, model_load_data.rotation.p, model_load_data.rotation.r
        )

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
