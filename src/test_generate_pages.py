import unittest

from generate_pages import extract_title, generate_page


class TestExtractTitle(unittest.TestCase):
    def test_extract_title_with_valid_markdown(self) -> None:
        markdown = "# My Title\n\nThis is some content."
        expected_title = "My Title"
        self.assertEqual(extract_title(markdown), expected_title)

    def test_extract_title_with_no_title(self) -> None:
        markdown = "This is some content without a title."
        with self.assertRaises(Exception):
            extract_title(markdown)

    def test_extract_title_with_multiple_headers(self) -> None:
        markdown = "# First Title\n\n# Second Title\n\nThis is some content."
        expected_title = "First Title"
        self.assertEqual(extract_title(markdown), expected_title)

    def test_extract_title_with_empty_markdown(self) -> None:
        markdown = ""
        with self.assertRaises(Exception):
            extract_title(markdown)


class TestGeneratePage(unittest.TestCase):
    def test_generate_page_with_valid_markdown(self) -> None:
        from_path = "test_files/valid_markdown.md"
        template_path = "test_files/template.html"  # Not used in this implementation
        dest_path = "test_files/generated_page.md"

        # Create a valid markdown file for testing
        with open(from_path, "w") as f:
            f.write("# Test Title\n\nThis is some test content.")

        # Generate the page
        generate_page(from_path, template_path, dest_path)

        # Read the generated page and verify its content
        with open(dest_path, "r") as f:
            generated_content = f.read()
            self.assertEqual(
                generated_content, "# Test Title\n\nThis is some test content."
            )

    def test_generate_page_with_invalid_markdown(self) -> None:
        from_path = "test_files/invalid_markdown.md"
        template_path = "test_files/template.html"  # Not used in this implementation
        dest_path = "test_files/generated_page.md"

        # Create an invalid markdown file for testing
        with open(from_path, "w") as f:
            f.write("This is some content without a title.")

        # Attempt to generate the page and expect an exception
        with self.assertRaises(Exception):
            generate_page(from_path, template_path, dest_path)
