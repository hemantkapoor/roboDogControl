
import struct
from ctypes import *

ROBOT_SOURCE = 0x00
GUI_SOURCE = 0x01
INTERNAL_SOURCE = 0xFE

#Important Functions
REQ_CPU_STATUS_FUNC = 0
RESP_CPU_STATUS_FUNC = 1
RESP_CAMERA_STATUS_FUNC = 2
REQ_MOVEMENT = 3
RESP_MOVEMENT = 4

STOP = 0
FORWARD = 1
BACKWARD = 2
LEFT = 3
RIGHT = 4



class CommandHeader(Structure):
    _fields_ = [
        ("preamble", c_uint8),
        ("source", c_uint8),
        ("target", c_uint8),
        ("function", c_uint8),
        ("length", c_uint32) ]

    def __init__(self):
        self.preamble = 0xFA
        self.source = GUI_SOURCE
        self.target = 0x00
        self.length = 0x00
        self.function = 0x00


class CpuInformation(Structure):
    _fields_ = [
        ("preamble", CommandHeader),
        ("cpuTemp", c_float),
        ("cpuRAM", c_uint32)]

    def __init__(self):
        self.preamble = CommandHeader()
        self.preamble.function = REQ_CPU_STATUS_FUNC
        self.cpuTemp = 10.0
        self.cpuRAM = 0

class CameraStatus(Structure):
    _fields_ = [
        ("preamble", CommandHeader),
        ("status", c_uint8)]

    def __init__(self):
        self.preamble = CommandHeader()
        self.preamble.source = INTERNAL_SOURCE
        self.preamble.function = RESP_CAMERA_STATUS_FUNC
        self.status = 0


'''
F - Forward
B - Backward
L - Left
R - Right
S - Stop 
'''
class ControlMovementCMD(Structure):
    _fields_ = [
        ("preamble", CommandHeader),
        ("movement", c_uint8)]

    def __init__(self):
        self.preamble = CommandHeader()
        self.preamble.source = GUI_SOURCE
        self.preamble.function = REQ_MOVEMENT
        self.movement = STOP
