import unittest

from textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_eq_without_url(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_eq_with_url(self):
        node = TextNode("This is a text node", "bold", 'https://www.dummy.de')
        node2 = TextNode("This is a text node", "bold", 'https://www.dummy.de')
        self.assertEqual(node, node2)

    def test_neq_text_property_diff(self):
        node = TextNode('blblblba', 'bold')
        node2 = TextNode('blblblba', 'italic')
        self.assertNotEqual(node, node2)



if __name__ == "__main__":
    unittest.main()
