import unittest

from split_delimiter import split_nodes_delimiter
from textnode import TextNode, TextType


class TestSplitDelimiter(unittest.TestCase):
    def test_split_code(self) -> None:
        node = TextNode("This is text with a `code block` word", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.PLAIN),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.PLAIN),
            ],
        )

    def test_split_bold(self) -> None:
        node = TextNode("This is **bold** text", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(
            new_nodes,
            [
                TextNode("This is ", TextType.PLAIN),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.PLAIN),
            ],
        )

    def test_split_italic(self) -> None:
        node = TextNode("This is _italic_ text", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)

        self.assertEqual(
            new_nodes,
            [
                TextNode("This is ", TextType.PLAIN),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text", TextType.PLAIN),
            ],
        )

    def test_split_multiple_sections(self) -> None:
        node = TextNode("This has `one` and `two` code blocks", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(
            new_nodes,
            [
                TextNode("This has ", TextType.PLAIN),
                TextNode("one", TextType.CODE),
                TextNode(" and ", TextType.PLAIN),
                TextNode("two", TextType.CODE),
                TextNode(" code blocks", TextType.PLAIN),
            ],
        )

    def test_non_plain_node_is_unchanged(self) -> None:
        node = TextNode("already bold", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(new_nodes, [node])

    def test_unmatched_delimiter_raises(self) -> None:
        node = TextNode("This has `unclosed code", TextType.PLAIN)

        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)
