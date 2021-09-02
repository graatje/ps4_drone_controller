import cv2
import numpy
import pygame
import json, os

from pygame.event import Event
from pygame.surface import Surface


class DroneController:
    def __init__(self):
        self.joysticks: list = []
        self.running: bool = False
        self.cam: cv2.VideoCapture = None
        # button keys by https://github.com/ChristianD37/YoutubeTutorials/blob/master/PS4%20Controller/ps4_keys.json
        with open(os.path.join("ps4_keys.json"), 'r+') as file:
            self.BUTTON_KEYS = json.load(file)
        # 0: Left analog horizonal, 1: Left Analog Vertical, 2: Right Analog Horizontal
        # 3: Right Analog Vertical 4: Left Trigger, 5: Right Trigger
        self.eventbindings: dict = {}  # {ps4key as integer: event to be called on pressing that key}
        for value in list(self.BUTTON_KEYS.values()):
            self.eventbindings[value] = None
        self.analog_keys: dict = {0: 0, 1: 0, 2: 0, 3: 0, 4: -1, 5: -1}
        self.loadWindow()

    def loadWindow(self):
        pygame.init()
        DISPLAY_W, DISPLAY_H = 960, 570
        canvas = pygame.Surface((DISPLAY_W,DISPLAY_H))
        self.window = pygame.display.set_mode(((DISPLAY_W,DISPLAY_H)))
        self.running = True
        self.__initjoysticks()

    def initvid(self, camera: cv2.VideoCapture):
        """
        initializes the camera.
        :param camera: the camera to get the input from.
        """
        self.cam = camera
        self.cam.set(3, 640)
        self.cam.set(4, 480)

    def update(self):
        """
        updates the screen including camera frame if camera is present, handles events.
        """
        if not self.running:
            return
        for event in pygame.event.get():
            self.__handleEvent(event)
        if self.cam:
            frame = self.__getCamFrame()
            if frame is not None:
                self.window.blit(frame, (0, 0))
        pygame.display.update()

    def bind_button(self, key: str, event):
        """
        binds a ps4 key to an event.
        :param key: a ps4 key. see ps4_keys.json
        :param event: the function to be called on the pressing of the provided ps4 button.
        :raises: KeyError if the provided key is not present on the ps4 controller.
        """
        try:
            self.eventbindings[self.BUTTON_KEYS[key]] = event
        except KeyError:
            raise KeyError("invalid key provided! see ps4_keys.json")

    def getJoyStickValues(self) -> dict:
        """
        gets joystick values.
        0: Left analog horizontal,
        1: Left Analog Vertical,
        2: Right Analog Horizontal,
        3: Right Analog Vertical,
        4: Left Trigger,
        5: Right Trigger
        :return: dictionary with joystick values.
        """
        return self.analog_keys

    def __handleEvent(self, event: Event):
        """
        handles a pygame event.
        :param event:
        :return:
        """
        if event.type == pygame.QUIT:
            self.running = False

        # handle button presses.
        if event.type == pygame.JOYBUTTONDOWN:
            if self.eventbindings[event.button] is not None:
                self.eventbindings[event.button]()

        # handles joystick events
        if event.type == pygame.JOYAXISMOTION:
            self.analog_keys[event.axis] = event.value

    def quit(self):
        """
        releases camera if present, sets running to false.
        :return:
        """
        if self.cam:
            self.cam.release()
        self.running = False

    def __initjoysticks(self):
        """
        initializes the controllers.
        """
        for i in range(pygame.joystick.get_count()):
            self.joysticks.append(pygame.joystick.Joystick(i))
        for joystick in self.joysticks:
            joystick.init()

    def __getCamFrame(self) -> (Surface, None):
        """
        gets a frame from the camera.
        :return: pygame Surface or None
        """
        if self.cam is not None:
            try:
                _, frame = self.cam.read()
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = numpy.rot90(frame)
                frame = numpy.flipud(frame)
                frame = pygame.surfarray.make_surface(frame)
                return frame
            except cv2.error:
                return None
