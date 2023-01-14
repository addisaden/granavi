from .node import Node
import pickle
import os

class Session:
    def __init__(self, name, restore_from=None):
        self.name = name
        self.__nodes__ = []
        if restore_from is not None:
            self.__load__(restore_from)

    def add(self, node):
        if isinstance(node, Node) and node not in self.__nodes__:
            self.__nodes__.append(node)

    def __contains__(self, node):
        return node in self.__nodes__

    def save(self, filename=None):
        object_to_save = self.__nodes__
        
        if filename is None:
            return pickle.dumps(object_to_save)

        with open(filename, "wb") as f:
            pickle.dump(object_to_save, f)

    def __load__(self, pickled_string_or_filename, datastring=False):
        is_file = os.path.exists(pickled_string_or_filename)
        if datastring or (not is_file):
            self.__nodes__ = pickle.loads(pickled_string)
        else:
            with open(pickled_string_or_filename, "rb") as f:
                self.__nodes__ = pickle.load(f)
