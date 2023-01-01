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

    def pathTo(self, other):
        visited = []
        currentPath = [self]
        while currentPath[-1] != other:
            currentNode = currentPath[-1]
            if currentNode not in visited:
                visited.append(currentNode)
            foundNeighbor = None
            for neighbor in currentNode.connectedNodes():
                if neighbor in visited:
                    continue
                if foundNeighbor is None or neighbor is other:
                    foundNeighbor = neighbor
            if foundNeighbor is None:
                if currentNode is self:
                    raise Exception("Not connected")
                else:
                    currentPath.pop()
            else:
                currentPath.append(foundNeighbor)
        
        return currentPath

    def __repr__(self):
        classname = ".".join([self.__class__.__module__, self.__class__.__name__])
        selfid = hex(id(self))
        return "<{} object {} at {}>".format(classname, self.name, selfid)
