class Node:
    def __init__(self, name, description=None, session=None):
        self.name = name
        self.__session = session
        if self.__session is not None:
            session.add(self)
        self.description = description
        if not isinstance(name, type("")):
            raise ValueError("name is not a string")
        if not isinstance(description, type("")) and not isinstance(description, type(None)):
            raise ValueError("description is not a string")
        self.__connectedNodes__ = []

    def __getattr__(self, name):
        if name == "session":
            return self.__session
        return super().__getattr__(name)

    def __setattr__(self, name, value):
        if name == "session":
            raise AttributeError("Can't set session again")
        return super().__setattr__(name, value)

    def connect(self, other, bidirect=False):
        if not isinstance(other, Node):
            raise ValueError("Wrong type of " + str(other) + ". Must be a granavi.Node")
        if self.session is not None:
            if self.session != other.session:
                raise AttributeError("Nodes are not in the same session:", self.session.name)
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

    def __walkall__(self, only=None):
        visited = []
        walkthese = [self]
        firstRun = True
        if only is not None:
            for nodeclass in only:
                if not issubclass(nodeclass, Node):
                    raise ValueError("Only contains classes which are not a subclass of Node: " + str(nodeclass))

        while len(walkthese) > 0:
            currentNode = walkthese.pop()
            currentNodeFound = False
            if only is not None:
                for nodeclass in only:
                    if isinstance(currentNode, nodeclass):
                        currentNodeFound = True
                
            if currentNode not in visited:
                visited.append(currentNode)
                for neighbor in currentNode.connectedNodes():
                    if neighbor in visited:
                        continue
                    walkthese.append(neighbor)

            if only is None or currentNodeFound:
                yield(currentNode)

    def pathTo(self, other, only=None):
        nodelist = {}
        connected = []
        other_id = id(other)

        if only is not None:
            foundOther = False
            for nodeclass in only:
                if not issubclass(nodeclass, Node):
                    raise ValueError("Only contains classes which are not a subclass of Node: " + str(nodeclass))
                if isinstance(other, nodeclass):
                    foundOther = True
            if not foundOther:
                raise ValueError("Other is not a subclass of only")

        if not isinstance(other, Node):
            raise ValueError("Other is not a instance of class Node or subclass: " + str(type(other)))

        for current_node in self.__walkall__():
            current_node_id = id(current_node)
            nodelist[current_node_id] = current_node
            for neighbor in current_node.connectedNodes():
                neighbor_id = id(neighbor)
                neighborIsSubclass = False
                if only is not None:
                    for nodeclass in only:
                        if isinstance(neighbor, nodeclass):
                            neighborIsSubclass = True
                if only is None or neighborIsSubclass:
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

    def search(self, searchTerm, only=None):
        result = []
        for currentNode in self.__walkall__(only=only):
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
