import time

from drone import Drone
from dronecontroller import DroneController
from droneposition import DronePosition
from droneconnection import DroneConnection


class Main:
    """
    binds the GUI and the drone to run the application
    """
    def __init__(self, video: bool):
        self.video = video
        self.running = False
        self.drone: Drone = None
        self.controller: DroneController = None
        self.init(video)

    def init(self, video: bool):
        self.init_drone()
        self.init_gui(video)
        self.bind()

    def init_drone(self):
        """
        creates the drone, initializes connection etc.
        """
        dronePosition = DronePosition()
        droneConnection = DroneConnection("192.168.100.1", 4646, 19798)
        self.drone = Drone(droneConnection, dronePosition)

    def init_gui(self, video=True):
        """
        initializes the GUI for the drone controller.
        """
        self.controller = DroneController()
        if self.drone is not None and video:
            self.controller.initvid(self.drone.getVideo())

    def send_command(self):
        """
        send a command to the drone.
        """
        analog_keys = self.controller.getJoyStickValues()
        self.drone.getDronePosition().setSideways((analog_keys[2] + 1) * 127.5)
        self.drone.getDronePosition().setThrottle(255 - (analog_keys[1] + 1) * 127.5)
        self.drone.getDronePosition().setTurn((analog_keys[0] + 1) * 127.5)
        self.drone.getDronePosition().setForward(255 - (analog_keys[3] + 1) * 127.5)
        self.drone.sendUDPPackage(False)
        
    def bind(self):
        """
        binds the keys of the ps4 controller to the function.
        """
        self.controller.bind_button("triangle", lambda: self.drone.sendUDPPackage(takeoff=True))
        self.controller.bind_button("x", self.drone.getDronePosition().reset)
        self.controller.bind_button("circle", self.quit)

    def quit(self):
        """
        quit the application
        """
        self.controller.quit()
        self.running = False

    def mainloop(self):
        """
        runs the application.
        """
        self.running = True
        starttime = time.time()
        counter = 0
        while self.running:
            counter += 1
            self.controller.update()
            if not self.video:
                time.sleep(0.03)
            if counter % 2 == 0:
                self.send_command()
        endtime = time.time()
        print(f"ran for {int(endtime - starttime)} seconds and sent a command {int(counter / 2)} times.\n"
              f"on average {int(counter/2)/ int((endtime - starttime))} times a second.")
    # sending a command too often a second will result in the drone not bëing able to keep up with the sended packages.
        # i am aiming for about max 20 times a second.


if __name__ == "__main__":
    m = Main(video=True)
    m.mainloop()
