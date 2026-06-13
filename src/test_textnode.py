import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self) -> None:
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_neq(self) -> None:
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.PLAIN)
        self.assertNotEqual(node, node2)

    def test_url_none(self) -> None:
        n = TextNode("This is an URL node", TextType.LINK)
        n2 = TextNode("This is an URL node", TextType.LINK)
        self.assertEqual(n, n2)

    def test_neq_url(self) -> None:
        n = TextNode("This is an URL node", TextType.LINK, "https://Boot.dev")
        n2 = TextNode("This is an URL node", TextType.LINK, "https://example.com")
        self.assertNotEqual(n, n2)


class TestTextNodeToHTML(unittest.TestCase):
    def test_text(self) -> None:
        help_node = TextNode("This is a text node", TextType.PLAIN)
        html_node = text_node_to_html_node(help_node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self) -> None:
        help_node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(help_node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")

    def test_italic(self) -> None:
        help_node = TextNode("This is an italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(help_node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic node")


if __name__ == "__main__":
    unittest.main()
