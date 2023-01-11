import zmq
import time
import base64
import threading
from camera_opencv import Camera

IPinver = '192.168.0.229'
#IPinver = '127.0.0.1'
class zmqServer():
    def __init__(self, theCam = None):
        self.context = zmq.Context()
        self.footage_socket = self.context.socket(zmq.PUB)
        self.footage_socket.setsockopt(zmq.CONFLATE, 1)
        print(IPinver)
        # self.footage_socket.connect('tcp://%s:5555' % IPinver)
        self.footage_socket.bind("tcp://*:4233")
        #self.footage_socket.connect('tcp://*')
        if theCam is not None:
            self.cam = theCam
        else:
            self.cam = Camera()

        fps_threading = threading.Thread(target=self.controlThread)         #Define a thread for FPV and OpenCV
        fps_threading.setDaemon(True)                             #'True' means it is a front thread,it would close when the mainloop() closes
        fps_threading.start()

    def controlThread(self):
        while True:
            frame = self.cam.get_frame()
            print(type(frame))
            jpg_as_text = base64.b64encode(frame)
            self.footage_socket.send(jpg_as_text)
            # self.footage_socket.send_string("Hello")

if __name__ == '__main__':
    cam = Camera()
    testServer = zmqServer(cam)
    while True:
        time.sleep(0.1)
