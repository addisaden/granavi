import unittest
from context import granavi

class NodeTest(unittest.TestCase):
    def test_example(self):
        self.assertEqual(770 + 7, 777)

    def test_create_node(self):
        name_of_node = "Example"
        description_of_node = "This is an example node"
        example_node = granavi.Node(name_of_node, description=description_of_node)
        example_node_2 = granavi.Node(name_of_node)
        self.assertEqual(example_node.name, name_of_node)
        self.assertEqual(example_node.description, description_of_node)
        self.assertEqual(example_node_2.name, name_of_node)
        self.assertEqual(example_node_2.description, None)

    def test_connect_2_nodes(self):
        node_1 = granavi.Node("Hello")
        node_2 = granavi.Node("World")
        node_1.connect(node_2)
        for wrongNode in ["hallo", 13, 3.3, ["node", 1]]:
            with self.assertRaises(ValueError):
                node_1.connect(wrongNode)
        self.assertTrue(node_1.isConnected(node_2))
        self.assertTrue(node_2 in node_1.connectedNodes())

    def test_route_simple(self):
        node_1 = granavi.Node("1")
        node_2 = granavi.Node("2")
        node_3 = granavi.Node("3")
        node_1.connect(node_2)
        node_2.connect(node_3)
        self.assertEqual(node_1.pathTo(node_3), [node_1, node_2, node_3])
        node_1.connect(node_3)
        self.assertEqual(node_1.pathTo(node_3), [node_1, node_3])

    def test_shortest_path(self):
        nodes = [granavi.Node(str(i)) for i in range(8)]
        # 0-1-2-3-7
        # |\-4---/|
        # \-5-6---/
        for a, b in [[0,1],[1,2],[2,3],[3,7],[0,4],[4,7],[0,5],[5,6],[6,7]]:
            nodes[a].connect(nodes[b])
        self.assertEqual(nodes[0].pathTo(nodes[7]), [nodes[0], nodes[4], nodes[7]])

    def test_repr_string(self):
        node_1 = granavi.Node("nodeName")
        node_1_repr = node_1.__repr__()
        self.assertTrue(node_1_repr.find("nodeName") > -1)
        self.assertTrue(node_1_repr.find(hex(id(node_1))) > -1)
        self.assertTrue(node_1_repr.find(".".join([node_1.__class__.__module__, node_1.__class__.__name__])) > -1)

    def test_disconnect(self):
        node_1 = granavi.Node("1")
        node_2 = granavi.Node("2")
        node_1.connect(node_2)
        self.assertTrue(node_1.isConnected(node_2))
        node_1.disconnect(node_2)
        self.assertFalse(node_1.isConnected(node_2))

    def test_bidirectional_connections(self):
        node_1 = granavi.Node("1")
        node_2 = granavi.Node("2")
        node_1.connect(node_2, bidirect=True)
        self.assertTrue(node_1.isConnected(node_2))
        self.assertTrue(node_2.isConnected(node_1))

    def test_node_name_and_description_is_string(self):
        for n, d in [["name", 13], [13, "hi"]]:
            with self.assertRaises(ValueError):
                cur = granavi.Node(n, d)

    def test_search(self):
        node_1 = granavi.Node("1")
        node_2 = granavi.Node("xyz hallo")
        node_3 = granavi.Node("2", "xyz welt xyz")

        node_1.connect(node_2)
        node_2.connect(node_3)

        self.assertEqual(node_1.search("hallo"), [node_2])
        self.assertEqual(node_1.search("welt"), [node_3])
        self.assertEqual(node_1.search(lambda n: n.name.find("hallo") > -1), [node_2])

    def test_subclass(self):
        node_1 = granavi.Node("1")
        class TestNode(granavi.Node):
            pass
        node_2 = TestNode("hallo")
        node_1.connect(node_2)
        self.assertEqual(node_1.pathTo(node_2), [node_1, node_2])
