from random import randint
import time

# check cross the line, if the result>0 => above the line, result<0 => below the line, result=0 => on the line
def crossLineUpCheck(x, y, w, h):
    result = y + ((220 * x) / w) - h
    return result

def crossLineDownCheck(x, y, w, h):
    result = y + (((200 * x) - 10000 - (h * w) + (50 * h))/(w - 50))
    return result

def crossUpLimitCheck(x, y, w, h):
    result = y + ((220 * x) / w) - (h - 20)
    return result

def crossDownLimitCheck(x, y, w, h):
    result = y + (((180 * x) - 18000 - (h * w) + (100 * h))/(w - 100))
    return result

def age_one(self):
    self.age += 1
    if self.age > self.max_age:
        self.done = True
    return True

class MyPerson:
    tracks = []

    def __init__(self, i, xi, yi, max_age):
        self.i = i
        self.x = xi
        self.y = yi
        self.tracks = []
        self.R = randint(0, 255)
        self.G = randint(0, 255)
        self.B = randint(0, 255)
        self.done = False
        self.state = '0'
        self.age = 0
        self.max_age = max_age
        self.dir = None

    def getRGB(self):
        return (self.R, self.G, self.B)

    def getTracks(self):
        return self.tracks

    def getId(self):
        return self.i

    def getState(self):
        return self.state

    def getDir(self):
        return self.dir

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def updateCoords(self, xn, yn):
        self.age = 0
        self.tracks.append([self.x, self.y])
        self.x = xn
        self.y = yn

    def setDone(self):
        self.done = True

    def timedOut(self):
        return self.done

    def going_UP(self, width, height):
        if len(self.tracks) >= 2:
            if self.state == '0':
                ### Tracking Cross the line
                #if self.tracks[-1][1] < mid_end and self.tracks[-2][1] >= mid_end:
                #print "x: ", self.tracks[-1][0], " y: ", self.tracks[-1][1], " width: ", width, " height: ", height, "value: ", crossLineUpCheck(self.tracks[-1][0], self.tracks[-1][1], width, height)
                if (crossUpLimitCheck(self.tracks[-1][0], self.tracks[-1][1], width, height) < 0
                    and crossUpLimitCheck(self.tracks[-2][0], self.tracks[-2][1], width, height) > 0):
                    state = '1'
                    self.dir = 'up'
                    return True
            else:
                return False
        else:
            return False

    def going_DOWN(self, width, height):
        if len(self.tracks) >=2:
            if self.state == '0':
                #if self.tracks[-1][1] > mid_start and self.tracks[-2][1] <= mid_start:
                print "x: ", self.tracks[-1][0], " y: ", self.tracks[-1][1], " width: ", width, " height: ", height, "value: ", crossDownLimitCheck(self.tracks[-1][0], self.tracks[-1][1], width, height)
                if(crossDownLimitCheck(self.tracks[-1][0], self.tracks[-1][1], width, height) > 0
                    and crossDownLimitCheck(self.tracks[-2][0], self.tracks[-2][1], width, height) < 0):
                    state = '1'
                    self.dir = 'down'
                    return True
            else:
                return False
        else:
            return False

    def age_one(self):
        self.age += 1
        if self.age > self.max_age:
            self.done = True
        return True
