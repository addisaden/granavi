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
        nodelist = {}
        connected = []
        other_id = id(other)

        for current_node in self.__walkall__():
            current_node_id = id(current_node)
            nodelist[current_node_id] = current_node
            for neighbor in current_node.connectedNodes():
                neighbor_id = id(neighbor)
                connected.append([current_node_id, neighbor_id])

        weights = {}
        visited = []
        reversePath = [other_id]
        weights[other_id] = 0

        while len(reversePath) > 0:
            current_node = reversePath.pop()
            if current_node in visited:
                continue
            visited.append(current_node)
            
            for connection in filter(lambda n: n[1] == current_node, connected):
                if connection[0] not in weights.keys():
                    weights[connection[0]] = weights[connection[1]] + 1
                if connection[0] not in visited:
                    reversePath.append(connection[0])

        if id(self) not in weights.keys():
            raise Exception("Not connected")

        visited = []
        currentPath = [self]
        while currentPath[-1] != other:
            currentNode = currentPath[-1]
            currentNode_id = id(currentNode)
            smallestNode_id = currentNode_id
            smallestNode_value = weights[currentNode_id]
            for connection in connected:
                node_from = connection[0]
                if node_from != currentNode_id:
                    continue
                node_to = connection[1]
                if weights[node_to] < smallestNode_value:
                    smallestNode_id = node_to
                    smallestNode_value = weights[node_to]

            if smallestNode_id:
                currentPath.append(nodelist[smallestNode_id])
            else:
                if self == currentNode:
                    raise Exception("Not connected")
        
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
