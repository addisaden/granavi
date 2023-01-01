class Node:
    def __init__(self, name, description=None):
        self.name = name
        self.description = description
        self.__connectedNodes__ = []

    def connect(self, other):
        if type(other) is not Node:
            raise ValueError("Wrong type of " + str(other) + ". Must be a granavi.Node")
        self.__connectedNodes__.append(other)

    def isConnected(self, other):
        return (other in self.__connectedNodes__)

    def connectedNodes(self):
        return self.__connectedNodes__
