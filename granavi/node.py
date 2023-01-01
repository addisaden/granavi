class Node:
    def __init__(self, name, description=None):
        self.name = name
        self.description = description
        if not isinstance(name, type("")):
            raise ValueError("name is not a string")
        if not isinstance(description, type("")) and not isinstance(description, type(None)):
            raise ValueError("description is not a string")
        self.__connectedNodes__ = []

    def connect(self, other, bidirect=False):
        if not isinstance(other, Node):
            raise ValueError("Wrong type of " + str(other) + ". Must be a granavi.Node")
        if other not in self.__connectedNodes__:
            self.__connectedNodes__.append(other)
        if bidirect:
            other.connect(self)

    def disconnect(self, other):
        self.__connectedNodes__.remove(other)

    def isConnected(self, other):
        return (other in self.__connectedNodes__)

    def connectedNodes(self):
        return self.__connectedNodes__

    def __walkall__(self):
        visited = []
        walkthese = [self]
        firstRun = True
        while len(walkthese) > 0:
            currentNode = walkthese.pop()
            if currentNode not in visited:
                visited.append(currentNode)
                for neighbor in currentNode.connectedNodes():
                    if neighbor in visited:
                        continue
                    walkthese.append(neighbor)
            yield(currentNode)

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

    def search(self, searchTerm):
        result = []
        for currentNode in self.__walkall__():
            found = False
            if isinstance(searchTerm, str):
                if currentNode.name.find(searchTerm) > -1:
                    found = True
                if currentNode.description is not None:
                    if currentNode.description.find(searchTerm) > -1:
                        found = True
            elif isinstance(searchTerm, type(lambda i: i)):
                if searchTerm(currentNode) == True:
                    found = True
            if found and currentNode not in result:
                result.append(currentNode)

        return result

    def __repr__(self):
        classname = ".".join([self.__class__.__module__, self.__class__.__name__])
        selfid = hex(id(self))
        return "<{} object {} at {}>".format(classname, self.name, selfid)
