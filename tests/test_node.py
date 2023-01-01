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

    def test_repr_string(self):
        node_1 = granavi.Node("nodeName")
        node_1_repr = node_1.__repr__()
        self.assertTrue(node_1_repr.find("nodeName") > -1)
        self.assertTrue(node_1_repr.find(hex(id(node_1))) > -1)
        self.assertTrue(node_1_repr.find(".".join([node_1.__class__.__module__, node_1.__class__.__name__])) > -1)
