import numpy as np
from copy import deepcopy


class UserPair():
    def __init__(self, uId, code, cdma):
        self.uId = uId
        self.code = code
        self.cdma = cdma

    def send(self, data):
        print("Sender_%s, send: %s" % (self.uId, np.reshape(data, (1, -1))))
        d = self.encode(data)
        self.cdma.signalCombine(d)

    def encode(self, data):
        return np.dot(data, np.reshape(self.cdma.Walsh[self.uId], (1, -1)))

    def decode(self, data):
        for i, d in enumerate(data):
            data[i] = data[i] * np.reshape(self.cdma.Walsh[self.uId], (1, -1))
        d = np.reshape(np.sum(data, axis=1)/8, (1, -1)).astype(int)
        print("Receiver_%s, receive: %s" % (self.uId, d))
        return d

    def receive(self):
        d = deepcopy(self.cdma.channel)
        self.decode(d)


class CDMA():

    def __init__(self, numberOfUser):
        if numberOfUser > 8:
            raise ValueError("Too much users!")
        self.Walsh = [-1, -1, -1, -1, -1, -1, -1, -1,
                      -1, 1, -1, 1, -1, 1, -1, 1,
                      -1, -1, 1, 1, -1, -1, 1, 1,
                      -1, 1, 1, -1, -1, 1, 1, -1,
                      -1, -1, -1, -1, 1, 1, 1, 1,
                      -1, 1, -1, 1, 1, -1, 1, -1,
                      -1, -1, 1, 1, 1, 1, -1, -1,
                      -1, 1, 1, -1, 1, -1, -1, 1]
        self.Walsh = np.reshape(self.Walsh, (8, 8))
        self.numberOfUser = numberOfUser
        self.channel = np.zeros((4, 8), "i")
        self.userPairs = []
        self.createUser()

    def createUser(self):
        for i in range(self.numberOfUser):
            u = UserPair(uId=i, code=self.Walsh[i], cdma=self)
            self.userPairs.append(u)

    def run(self):
        # send
        for u in self.userPairs:
            a = np.zeros(1)
            a = np.reshape(np.array([1, 0, 0, 1], "i"), (-1, 1))
            u.send(a)
        print("---------- Sending Through Channel -----------")
        print("---------------- Channel State ---------------")
        print (self.channel)
        print("--------------- Start Receive ----------------")
        # receive
        for u in self.userPairs:
            u.receive()

    def signalCombine(self, data):
        self.channel = self.channel + data


if __name__ == "__main__":
    numberOfUser = 8
    myCDMA = CDMA(numberOfUser)
    myCDMA.run()
