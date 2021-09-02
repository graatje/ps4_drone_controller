import binascii
import datetime
def createDateTimeJson():
    now = datetime.datetime.now()
    somedict = {"YEAR":now.year, "MONTH": now.month, "DAY": now.day, "HOUR": now.hour, "MINUTE":now.minute, "SECOND": now.second}
    return str(somedict).replace("'", '"').replace(" ", "")

def string_to_binarystring(string):
    return string.encode("ascii")


class Data:
    # udp data
    NORMAL_DATA = binascii.unhexlify("660a808002800002ffff00000000000000000299")

    # tcp data
    CLIENTSEND1 = b'{"CMD":80,"PARAM":{"Type":16,"W":1280,"H":720}}'
    CLIENTSEND2 = b'{"CMD":80,"PARAM":{"Type":18,"W":4096,"H":3072}}'
    SERVERSEND1 = b'{ "CMD": 0, "PARAM": { "FirmWare": "1.0.13", "platform": "A7-2K-2966-2-16-1-2-00020003-1-1-1-1-1-1-2-0", "pinp_X": 60, "pinp_Y": 6, "cur_csi": 0 }, "RESULT": 0 }\x00'
    SERVERSEND2 = b'{ "CMD": 80, "PARAM": -1, "RESULT": 0 }\x00'
    SERVERSEND3 = b'{ "CMD": 80, "PARAM": -1, "RESULT": 0 }\x00'

    # video initialize data
    VIDCLIENT1 = b'{"CMD":29,"PARAM":' + createDateTimeJson().encode("ascii") + b'}'
    VIDCLIENT2 = b'DESCRIBE rtsp://192.168.100.1:7070/H264VideoSMS RTSP/1.0\r\nCSeq: 2\r\nUser-Agent: nobody (LIVE555 Streaming Media v2017.06.04)\r\nAccept: application/sdp\r\n\r\n'
    VIDCLIENT3 = b'SETUP rtsp://192.168.100.1:7070/H264VideoSMS/track1 RTSP/1.0\r\nCSeq: 3\r\nUser-Agent: nobody (LIVE555 Streaming Media v2017.06.04)\r\nTransport: RTP/AVP/TCP;unicast;interleaved=0-1\r\n\r\n'

    def VIDCLIENT4(session):
        return b'PLAY rtsp://192.168.100.1:7070/H264VideoSMS/ RTSP/1.0\r\nCSeq: 4\r\nUser-Agent: nobody (LIVE555 Streaming Media v2017.06.04)\r\nSession: ' + session.encode() + b'\r\nRange: npt=0.000-\r\n\r\n'
