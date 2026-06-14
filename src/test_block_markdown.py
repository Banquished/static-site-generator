import unittest

from block_markdown import (
    BlockType,
    block_to_block_type,
    markdown_to_blocks,
    markdown_to_html_node,
)


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self) -> None:
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_no_blocks(self) -> None:
        md = "This is a single paragraph with no blocks."
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [md])


class TestBlockToBlockType(unittest.TestCase):
    def test_block_to_block_type(self) -> None:
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING_1)
        self.assertEqual(block_to_block_type("## Heading 2"), BlockType.HEADING_2)
        self.assertEqual(block_to_block_type("### Heading 3"), BlockType.HEADING_3)
        self.assertEqual(block_to_block_type("#### Heading 4"), BlockType.HEADING_4)
        self.assertEqual(block_to_block_type("##### Heading 5"), BlockType.HEADING_5)
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEADING_6)
        self.assertEqual(block_to_block_type("> Quote"), BlockType.BLOCKQUOTE)
        self.assertEqual(
            block_to_block_type("- List item"), BlockType.UNORDERED_LIST_ITEM
        )
        self.assertEqual(
            block_to_block_type("1. List item"), BlockType.ORDERED_LIST_ITEM
        )
        self.assertEqual(
            block_to_block_type("This is a paragraph."), BlockType.PARAGRAPH
        )

    def test_block_to_block_type_empty(self) -> None:
        self.assertEqual(block_to_block_type(""), BlockType.PARAGRAPH)

    def test_block_to_block_type_whitespace(self) -> None:
        self.assertEqual(block_to_block_type("   "), BlockType.PARAGRAPH)

    def test_block_to_block_type_unexpected(self) -> None:
        self.assertEqual(block_to_block_type("!@#$%^&*()"), BlockType.PARAGRAPH)


class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_paragraphs(self) -> None:
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self) -> None:
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
