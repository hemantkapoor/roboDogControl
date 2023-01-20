from evdev import InputDevice, categorize, ecodes
import threading
import time
import Control
from commandlist import *


class Stadia():

    def __init__(self, controller=None):
        self._controller = controller
        self._gamepad = InputDevice('/dev/input/event0')
        _gamePadthreading = threading.Thread(target=self.gamepadThread)  # Define a thread for FPV and OpenCV
        _gamePadthreading.setDaemon(True)  # 'True' means it is a front thread,it would close when the mainloop() closes
        _gamePadthreading.start()
        self._requestedAction = IDLE
        self._performingAction = IDLE
        self._xAction = False
        self._yAction = False

        _gamePadthreading = threading.Thread(target=self.controlDoggy)  # Define a thread for FPV and OpenCV
        _gamePadthreading.setDaemon(True)  # 'True' means it is a front thread,it would close when the mainloop() closes
        _gamePadthreading.start()


    def gamepadThread(self):
        timeStamp = time.time()
        # while True:
        for ev in self._gamepad.read_loop():
            if ev is None:
                print("Nothing received Sleeping zzzzzz....")
                time.sleep(0.5)
                continue
            # if (time.time() - timeStamp) < 1:
            #     continue
            # timeStamp = time.time()

            absevent = categorize(ev)
            if ecodes.bytype[absevent.event.type][absevent.event.code] == 'ABS_X':
                # print(absevent.event.value)
                xAxis = int(absevent.event.value)
                if xAxis > 192:
                    print("Turn right")
                    self._xAction = True
                    self._requestedAction = RIGHT
                elif xAxis < 64:
                    print("Turn Left")
                    self._xAction = True
                    self._requestedAction = LEFT
                else:
                    self._xAction = False

            if ecodes.bytype[absevent.event.type][absevent.event.code] == 'ABS_Y':
                yAxis = int(absevent.event.value)
                if yAxis > 192:
                    print("Go Back")
                    self._requestedAction = BACKWARD
                    self._yAction = True
                elif yAxis < 64:
                    print("Go front")
                    self._requestedAction = FORWARD
                    self._yAction = True
                else:
                    self._yAction = False

            if (self._xAction == False) and (self._yAction == False):
                print("Stay Idle")
                self._requestedAction = IDLE

            if self._requestedAction == self._performingAction:
                continue
            else:
                self._performingAction = self._requestedAction
            # print("Sleeping zzzz...")
            # time.sleep(0.1)


    def controlDoggy(self):
        while True:
            if self._controller is None:
                time.sleep(1)
                if self._performingAction != IDLE:
                    print("Performing Action" + str(self._performingAction))
                continue
            if self._performingAction == RELAX:
                self._controller.relax_flag = True
                self._controller.relax(True)
            if self._performingAction == FORWARD:
                self._controller.forWard()
            if self._performingAction == BACKWARD:
                self._controller.backWard()
            if self._performingAction == LEFT:
                self._controller.turnLeft()
            if self._performingAction == RIGHT:
                self._controller.turnRight()
            if self._performingAction == IDLE:
                time.sleep(0.5)


if __name__ == '__main__':
    gamePad = Stadia()
    while True:
        time.sleep(0.5)


