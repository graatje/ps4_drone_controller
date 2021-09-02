def getHexNumber(number):
    amount = str(hex(number).split("0x")[1])
    if len(amount) == 2:
        return amount
    elif len(amount) == 1:
        return "0" + amount
    else:
        raise ValueError("impossible")


class DronePosition:
    """
    this class handles forward, turn, sideways and throttle.
    """
    def __init__(self, flycorrection: float = 0.0):
        self.FLYCORRECTION: float = flycorrection
        self.turn = 127
        self.forward = 127
        self.sideways = 127
        self.throttle = 127

    def reset(self):
        """
        sets everything to the middle value, 127.
        """
        self.turn = 127
        self.forward = 127
        self.sideways = 127
        self.throttle = 127

    def adjustThrottle(self, val):
        newval = self.throttle - val
        if newval >= 0 and newval <= 255:
            self.throttle = newval

    def adjustSideways(self, val):
        newval = self.sideways + val
        if newval >= 0 and newval <= 255:
            self.sideways = newval
            
    def adjustForward(self, val):
        newval = self.forward - val
        if newval >= 0 and newval <= 255:
            self.forward = newval
            
    def adjustTurn(self, val):
        newval = self.turn + val
        if newval >= 0 and newval <= 255:
            self.turn = newval

    def setTurn(self, val):
        if val > 255:
            self.turn = 255
        elif val < 0:
            self.turn = 0
        else:
            self.turn = val

    def setForward(self, val):
        if val > 255:
            self.forward = 255
        elif val < 0:
            self.forward = 0
        else:
            self.forward = val

    def setSideways(self, val):
        if val > 255:
            self.sideways = 255
        elif val < 0:
            self.sideways = 0
        else:
            self.sideways = val

    def setThrottle(self, val):
        if val > 255:
            self.throttle = 255
        elif val < 0:
            self.throttle = 0
        else:
            self.throttle = val

    def getHexValues(self):
        return {"forward": getHexNumber(int(self.forward)),
                "throttle": getHexNumber(int(self.throttle)),
                "sideways": getHexNumber(int(self.sideways)),
                "turn": getHexNumber(int(self.turn))
                }

    def moveTowardsMiddle(self):
        """
        moves everything towards the middle.
        :return:
        """
        if self.forward > 127:
            self.forward -= self.FLYCORRECTION
        elif self.forward < 127:
            self.forward += self.FLYCORRECTION
        if self.throttle > 127:
            self.throttle -= self.FLYCORRECTION
        elif self.throttle < 127:
            self.throttle += self.FLYCORRECTION
        if self.sideways > 127:
            self.sideways -= self.FLYCORRECTION
        elif self.sideways < 127:
            self.sideways += self.FLYCORRECTION
        if self.turn > 127:
            self.turn -= self.FLYCORRECTION
        elif self.turn < 127:
            self.turn += self.FLYCORRECTION

    def __str__(self) -> str:
        """
        shows forward, throttle, sideways and turn.
        :return: string.
        """
        return "forward: " + str(self.forward) + \
               " throttle: " + str(self.throttle) + \
               " sideways: " + str(self.sideways) + \
               " turn: " + str(self.turn)

if __name__ == "__main__":
    pos = DronePosition(0.1)
    pos.forward = 0
    print(pos.getHexValues())