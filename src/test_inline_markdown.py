import unittest

from inline_markdown import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)
from textnode import TextNode, TextType


class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_markdown_images(self) -> None:
        text = "Here is an image: ![alt text](https://example.com/image.png)"
        expected: list[tuple[str, str]] = [
            ("alt text", "https://example.com/image.png")
        ]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_extract_markdown_images_no_images(self) -> None:
        text = "This text has no images."
        expected: list[tuple[str, str]] = []
        self.assertEqual(extract_markdown_images(text), expected)


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_extract_markdown_links(self) -> None:
        text = "Here is a link: [example](https://example.com)"
        expected: list[tuple[str, str]] = [("example", "https://example.com")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_extract_markdown_links_no_links(self) -> None:
        text = "This text has no links."
        expected: list[tuple[str, str]] = []
        self.assertEqual(extract_markdown_links(text), expected)


class TestSplitNodesImage(unittest.TestCase):
    def test_split_single_image(self) -> None:
        node = TextNode(
            "This is text with an ![image](https://example.com/image.png)",
            TextType.PLAIN,
        )

        self.assertEqual(
            split_nodes_image([node]),
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://example.com/image.png"),
            ],
        )

    def test_split_multiple_images(self) -> None:
        node = TextNode(
            "Images: ![first](https://example.com/1.png) and ![second](https://example.com/2.png)",
            TextType.PLAIN,
        )

        self.assertEqual(
            split_nodes_image([node]),
            [
                TextNode("Images: ", TextType.PLAIN),
                TextNode("first", TextType.IMAGE, "https://example.com/1.png"),
                TextNode(" and ", TextType.PLAIN),
                TextNode("second", TextType.IMAGE, "https://example.com/2.png"),
            ],
        )

    def test_split_image_no_images(self) -> None:
        node = TextNode("This has no images", TextType.PLAIN)

        self.assertEqual(
            split_nodes_image([node]),
            [node],
        )

    def test_split_image_preserves_non_plain_nodes(self) -> None:
        node = TextNode("already bold", TextType.BOLD)

        self.assertEqual(
            split_nodes_image([node]),
            [node],
        )


class TestSplitNodesLink(unittest.TestCase):
    def test_split_single_link(self) -> None:
        node = TextNode(
            "This is text with a [link](https://boot.dev)",
            TextType.PLAIN,
        )

        self.assertEqual(
            split_nodes_link([node]),
            [
                TextNode("This is text with a ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
        )

    def test_split_multiple_links(self) -> None:
        node = TextNode(
            "Go to [boot](https://boot.dev) and [youtube](https://youtube.com)",
            TextType.PLAIN,
        )

        self.assertEqual(
            split_nodes_link([node]),
            [
                TextNode("Go to ", TextType.PLAIN),
                TextNode("boot", TextType.LINK, "https://boot.dev"),
                TextNode(" and ", TextType.PLAIN),
                TextNode("youtube", TextType.LINK, "https://youtube.com"),
            ],
        )

    def test_split_link_no_links(self) -> None:
        node = TextNode("This has no links", TextType.PLAIN)

        self.assertEqual(
            split_nodes_link([node]),
            [node],
        )

    def test_split_link_does_not_split_images(self) -> None:
        node = TextNode(
            "This is an image ![alt](https://example.com/image.png)",
            TextType.PLAIN,
        )

        self.assertEqual(
            split_nodes_link([node]),
            [node],
        )


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


class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_textnodes(self) -> None:
        text = "This is **bold** and _italic_ text with a [link](https://boot.dev) and an ![image](https://example.com/image.png)"
        expected = [
            TextNode("This is ", TextType.PLAIN),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text with a ", TextType.PLAIN),
            TextNode("link", TextType.LINK, "https://boot.dev"),
            TextNode(" and an ", TextType.PLAIN),
            TextNode("image", TextType.IMAGE, "https://example.com/image.png"),
        ]

        self.assertEqual(text_to_textnodes(text), expected)

    def test_text_to_textnodes_no_markdown(self) -> None:
        text = "This is plain text with no markdown."
        expected = [TextNode(text, TextType.PLAIN)]

        self.assertEqual(text_to_textnodes(text), expected)


if __name__ == "__main__":
    unittest.main()
