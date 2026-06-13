import unittest

from inline_markdown import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
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


if __name__ == "__main__":
    unittest.main()
