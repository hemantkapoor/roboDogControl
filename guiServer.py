import socket
from commandlist import *
import time
from utilities import *
from _thread import *
import threading
from zmqServer import *
from Control import *
import Command
import Action
from itertools import groupby

#host = '127.0.0.1'
host = ''
port = 10223
ThreadCount = 0

class Server():

    def __init__(self):
        self.bodyControl = Control()
        self.actions = Action.Action(self.bodyControl)
        self.bodyControl.Thread_conditiona.start()
        self.cmd = Command.COMMAND()
        self.state = RELAX
        self.currentBodyAction = IDLE
        self.actionList = []

        _bodyActionthreading = threading.Thread(target=self.controlBodyThread)         #Define a thread for FPV and OpenCV
        _bodyActionthreading.setDaemon(True)                             #'True' means it is a front thread,it would close when the mainloop() closes
        _bodyActionthreading.start()
        pass

    def controlBodyThread(self):
        while True:
            if not self.actionList:
                time.sleep(0.5)
                self.currentBodyAction = IDLE
                continue

            #First delete and consecutive duplicates
            res = [i[0] for i in groupby(self.actionList)]
            self.actionList = res

            # To put logic of speed back
            #self.bodyControl.speed = int(mov.speed)
            self.bodyControl.relax_flag = False
            self.bodyControl.timeout = time.time()

            self.currentBodyAction = self.actionList.pop(0)
            if self.currentBodyAction == RELAX:
                self.bodyControl.relax_flag = True
                self.bodyControl.relax(True)
            elif self.currentBodyAction == FORWARD:
                self.bodyControl.forWard()
            elif self.currentBodyAction == BACKWARD:
                self.bodyControl.backWard()
            elif self.currentBodyAction == LEFT:
                self.bodyControl.turnLeft()
            elif self.currentBodyAction == RIGHT:
                self.bodyControl.turnRight()

            #




    def client_handler(self, connection):
        connection.send(str.encode('You are now connected to the doggy server'))
        self.state = RELAX
        while True:
            try:
                Recvdata = connection.recv(2048)
                data = bytearray(Recvdata)
                self.handleCommand(connection, data)
            except Exception as e:
                print(e)
                break
        connection.close()

    def accept_connections(self, ServerSocket):
        Client, address = ServerSocket.accept()
        print('Connected to: ' + address[0] + ':' + str(address[1]))
        start_new_thread(self.client_handler, (Client, ))

    def server_handler(self, ServerSocket):
        while True:
            self.accept_connections(ServerSocket)

    def start_server(self, host, port):
        ServerSocket = socket.socket()
        try:
            ServerSocket.bind((host, port))
        except socket.error as e:
            print(str(e))
        print(f'Server is listing on the port {port}...')
        ServerSocket.listen()
        start_new_thread(self.server_handler, (ServerSocket,))


    # ************** COMMAND HANDLERS IMPLEMENTED HERE
    def handleCommand(self, connection, data):
        preamble = CommandHeader.from_buffer(data)
        #cHECK IF cpu INFORMATION RECEIVED
        if preamble.function == REQ_CPU_STATUS_FUNC:
            self.handleCpuStatSunction(connection, preamble)
        if preamble.function == REQ_MOVEMENT:
            self.handleMovement(connection, data)
        if preamble.function == REQ_ACTION:
            self.handleActions(connection, data)

    def handleCpuStatSunction(self, connection, preamble):
        print("Handling CPU Stat")
        cpuInfo = CpuInformation()
        cpuInfo.preamble.source = ROBOT_SOURCE
        cpuInfo.preamble.target = preamble.source
        cpuInfo.preamble.function = RESP_CPU_STATUS_FUNC
        cpuInfo.cpuTemp = get_cpu_tempfunc()
        cpuInfo.cpuRAM = int(get_ram_info())
        # cpuInfo.movement =self.state
        cpuInfo.movement = self.currentBodyAction

        dataToSend = bytearray(cpuInfo)
        connection.send(dataToSend)
        print("Return from Handle Cpu Stat Len = " + str(sizeof(preamble)))
        return sizeof(preamble)

    def handleMovement(self, connection, data):
        print("Handling Movement command")
        print(self.bodyControl.move_count)
        if self.bodyControl.move_count > 120:
            self.state = RELAX
            return
        mov = ControlMovementCMD.from_buffer(data)
        print("Body part = " + str(mov.bodyPart))
        print("Direction = " + str(mov.direction))
        print("Action = " + str(mov.action))
        print("Speed = " + str(mov.speed))
        if mov.bodyPart == BODY_PART_LEGS:
            self.actionList.append(mov.direction)

        '''
            if mov.action == MOVEMENT_STOP:
                print("***** STOPPED RECEIVED *****")
                self.state = STOPPED
                #self.bodyControl.stop()
                #self.bodyControl.order = self.cmd.CMD_MOVE_STOP + "10\n"
            else:
                self.bodyControl.speed = int(mov.speed)
                self.bodyControl.relax_flag = False
                self.bodyControl.timeout = time.time()
                if mov.direction == RELAX:
                    print("Relaxu received")
                    self.state = RELAX
                    self.bodyControl.relax_flag = True
                    self.bodyControl.relax(True)
                elif mov.direction == FORWARD:
                    self.state = FORWARD
                    self.bodyControl.forWard()
                elif mov.direction == BACKWARD:
                    self.state = BACKWARD
                    self.bodyControl.backWard()
                elif mov.direction == LEFT:
                    self.state = LEFT
                    self.bodyControl.turnLeft()
                elif mov.direction == RIGHT:
                    self.state = RIGHT
                    self.bodyControl.turnRight()
            self.bodyControl.timeout = time.time()
        
        return sizeof(ControlMovementCMD())
        '''

    def handleActions(self, connection, data):
        print("Handling Actions command")
        action = ActionsCMD.from_buffer(data)
        if action.action == MOVEMENT_STOP:
            pass
        else:
            if action.actionType == ACTION_PUSH_UPS:
                print("Doing Push ups")
                self.actions.push_ups()
            elif action.actionType == ACTION_HELLO_ONE:
                self.actions.helloOne()
            elif action.actionType == ACTION_HELLO_TWO:
                self.actions.helloTwo()
            elif action.actionType == ACTION_HAND:
                self.actions.hand()
            elif action.actionType == ACTION_SWIM:
                self.actions.swim()
            elif action.actionType == ACTION_YOGA:
                self.actions.yoga()
        return sizeof(ActionsCMD())



if __name__ == '__main__':
    testServer = Server()
    testServer.start_server(host, port)
    testZmqServer = zmqServer()
    while True:
        time.sleep(0.1)