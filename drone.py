import cv2

from droneconnection import DroneConnection
from droneposition import DronePosition


class Drone:
    def __init__(self, droneConnection: DroneConnection, dronePosition: DronePosition):
        self.droneConnection: DroneConnection = droneConnection
        self.dronePosition: DronePosition = dronePosition
        self.sendedpackages: list = []

    def sendUDPPackage(self, takeoff=False):
        """
        sends a command to the drone.
        :param takeoff:
        :return:
        """
        if takeoff:
            print("supposed to fly!!")
        pos = self.dronePosition.getHexValues()
        package = self.__buildPackage(pos["throttle"], pos["turn"], pos["sideways"], pos["forward"], takeoff)
        self.sendedpackages.append(package)
        self.droneConnection.send_udp_packet(bytes.fromhex(package))

    def getDronePosition(self) -> DronePosition:
        return self.dronePosition

    def __buildPackage(self, throttle, turn, sideways, forward, takeoff=False):
        """
        builds a package to be sent via the udp connection.
        :param throttle:
        :param turn:
        :param sideways:
        :param forward:
        :param takeoff:
        """
        if takeoff:
            takeoff = "01"
        else:
            takeoff = "00"
        package = f"66 ff {sideways} {forward} {throttle} {turn} {takeoff} 02 ff ff 00 00 00 00 00 00 00 00 02 99"
        return package

    def getVideo(self) -> cv2.VideoCapture:
        """
        gets the video capture via the drone connection
        :return: videocapture.
        """
        return self.droneConnection.connect_video()


if __name__ == "__main__":
    drone = Drone(None, None)
    print(drone.buildPackage(80, 80, 80, 80, True))
