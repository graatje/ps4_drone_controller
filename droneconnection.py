import socket
import cv2

from data import Data
import time


class DroneConnection:
    def __init__(self, ip: str, tcpport: int, udp_port: int):
        self.connect_tcp(ip, tcpport)
        self.tcp_socket = None
        self.udp_socket = None
        self.connect_tcp(ip, tcpport)
        self.connect_udp(ip, udp_port)
        
    def connect_tcp(self, ip: str, tcpport: int):
        """

        :param ip: the ip address of the drone.
        :param tcpport:
        """
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_socket.connect((ip, tcpport))
        print(self.tcp_socket.recv(512))
        self.tcp_socket.send(Data.CLIENTSEND1)
        self.tcp_socket.send(Data.CLIENTSEND2)
        print(self.tcp_socket.recv(512))
        print(self.tcp_socket.recv(512))

    def connect_video(self) -> cv2.VideoCapture:
        """
        creating a video capture.
        :return: cv2.VideoCapture
        """
        self.tcp_socket.send(Data.VIDCLIENT1)
        print(self.tcp_socket.recv(512))
        # creating the socket for the video connection.
        cap = cv2.VideoCapture("rtsp://192.168.100.1:7070/H264VideoSMS")
        return cap

    def connect_udp(self, ip: str, udp_port: int):
        """
        initialize the command stream to the drone.
        :param ip:
        :param udp_port:
        """
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_socket.connect((ip, udp_port))
        print("connected with UDP.")
        print(time.time())
        for i in range(200):
            time.sleep(0.003)
            self.udp_socket.send(Data.NORMAL_DATA)
        print("Drone started!")

    def send_udp_packet(self, flightdata: bytes):
        """
        send data to the udp socket.
        :param flightdata
        """
        self.udp_socket.send(flightdata)


if __name__ == "__main__":
    d = DroneConnection("192.168.100.1", 4646, 19798)
    
    
