from abc import ABC, abstractmethod

class ObserverBase:

    @abstractmethod
    def getSource(self):
        pass

    @abstractmethod
    def handleFunction(self, data):
        print('Method Not implemented')
        raise NotImplementedError