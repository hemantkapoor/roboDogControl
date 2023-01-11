import socket
from commandlist import *
import time
from utilities import *
from _thread import *
from zmqServer import *

#host = '127.0.0.1'
host = ''
port = 10223
ThreadCount = 0

class Server():

    def __init__(self,):
        pass

    def client_handler(self, connection):
        connection.send(str.encode('You are now connected to the replay server... Type BYE to stop'))
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
        elif preamble.function == REQ_MOVEMENT:
            self.handleMovement(connection, data)

    def handleCpuStatSunction(self, connection, preamble):
        print("Handling CPU Stat")
        cpuInfo = CpuInformation()
        cpuInfo.preamble.source = ROBOT_SOURCE
        cpuInfo.preamble.target = preamble.source
        cpuInfo.preamble.function = RESP_CPU_STATUS_FUNC
        cpuInfo.cpuTemp = get_cpu_tempfunc()
        cpuInfo.cpuRAM = int(get_ram_info())
        dataToSend = bytearray(cpuInfo)
        connection.send(dataToSend)

    def handleMovement(self, connection, data):
        print("Handling Movement command")
        mov = ControlMovementCMD.from_buffer(data)
        print("Body part = " + str(mov.bodyPart))
        print("Direction = " + str(mov.direction))
        print("Action = " + str(mov.action))
        print("Speed = " + str(mov.speed))



if __name__ == '__main__':
    testServer = Server()
    testServer.start_server(host, port)
    testServer = zmqServer()
    while True:
        time.sleep(0.1)