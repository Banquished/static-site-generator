import unittest
from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_neq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.PLAIN)
        self.assertNotEqual(node, node2)

    def test_url_none(self):
        n = TextNode("This is an URL node", TextType.LINK)
        n2 = TextNode("This is an URL node", TextType.LINK, None)
        self.assertEqual(n, n2)

    def test_neq_url(self):
        n = TextNode("This is an URL node", TextType.LINK, "https://Boot.dev")
        n2 = TextNode("This is an URL node", TextType.LINK, "https://example.com")
        self.assertNotEqual(n, n2)
        
if __name__ == "__main__":
    unittest.main()
