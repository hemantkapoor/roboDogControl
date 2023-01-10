from commandlist import *
from observerBase import *
from gui import *


class CommandParser:
    registeredList = []

    @staticmethod
    def register(obj):
        CommandParser.registeredList.append(obj)

    @staticmethod
    def handleCommand(data):

        data = bytearray(data)
        print('data received')
        #first decode the preamble
        try:
            preamble = CommandHeader.from_buffer(data)
            #check if the source is present in the lsit
            for observer in CommandParser.registeredList:
                try:
                    print(observer)
                    # print('Targeted = ' + str(preamble.target))
                    # print('Observer = ' + str(observer.getSource()))
                    if observer.getSource() == preamble.target:
                        observer.handleFunction(data)
                        break
                except:
                    pass

        except:
            print('Something went wrong')
            pass

