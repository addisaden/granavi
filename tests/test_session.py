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

    def test_connect_mixed_nodes(self):
        session = granavi.Session("test")
        a = granavi.Node("a", session=session)
        b = granavi.Node("b", session=session)
        c = granavi.Node("c")
        a.connect(b)
        self.assertTrue(a.isConnected(b))
        with self.assertRaises(AttributeError):
            a.connect(c)
        self.assertFalse(a.isConnected(c))

    def test_session_bytestring(self):
        s1 = granavi.Session("s1")
        nodes = [granavi.Node(str(i), session=s1) for i in range(10)]
        data = s1.save()
        s2 = granavi.Session("s2", data)
        self.assertEqual(len(s2.__nodes__), len(nodes))
        for si, sn in enumerate(s1.__nodes__):
            self.assertEqual(s2.__nodes__[si].name, sn.name)

    def test_session_datafile(self):
        testfilename = "/tmp/granavitestfile.testnodes"
        s1 = granavi.Session("s1")
        nodes = [granavi.Node(str(i), session=s1) for i in range(10)]
        s1.save(testfilename)
        s2 = granavi.Session("s2", testfilename)
        self.assertEqual(len(s2.__nodes__), len(nodes))
        for si, sn in enumerate(s1.__nodes__):
            self.assertEqual(s2.__nodes__[si].name, sn.name)
        
