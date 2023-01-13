import unittest
from context import granavi

class SessionTest(unittest.TestCase):
    def test_create_session(self):
        session = granavi.Session("sessionname")
        self.assertTrue(isinstance(session, granavi.Session))

    def test_create_node_in_session(self):
        session = granavi.Session("test")
        node = granavi.Node("hello", session=session)
        with self.assertRaises(AttributeError):
            node.session = "Hallo"
        self.assertEqual(node.session, session) # self.__getattr__(self, name)
        self.assertTrue(node in session) # self.__contains__(self, item)
        # https://rszalski.github.io/magicmethods/
