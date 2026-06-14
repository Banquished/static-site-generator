import os

from block_markdown import markdown_to_html_node


def extract_title(markdown: str) -> str:
    """
    Extracts the title from a markdown string. The title is assumed to be the first line that starts with '# '.

    Args:
        markdown (str): The markdown string to extract the title from.

    Returns:
        str: The extracted title.

    Raises:
        Exception: If no title is found, an Exception is raised indicating that the markdown does not contain a valid title.
    """
    header = ""
    for line in markdown.splitlines():
        if line.startswith("# "):
            header = line[2:].strip()
            return header

    raise Exception(f"Markdown does not contain a valid title: {markdown}")


def generate_page(
    from_path: str, template_path: str, dest_path: str, basepath: str
) -> None:
    """
    Generates a page by reading markdown content from a source file,
    extracting the title, and then writing the content to a destination file.

    Args:
        from_path (str): The path to the source markdown file.
        template_path (str): The path to the template file
        (not used in this implementation).
        dest_path (str): The path to the destination file
        where the generated page will be written.

    Raises:
        Exception: If there is an error reading the source file or
        writing to the destination file, an Exception is raised with an
        appropriate error message.
    """
    try:
        with open(from_path, "r") as f:
            # 1. Print a message:
            print(
                f"Generating page from `{from_path}` to `{dest_path}` using `{template_path}` template."
            )
            # 2. Read the markdown file at `from_path` and store its content in a variable.
            markdown = f.read()
            # 3. Read the template file at `template_path` and store the contents in a variable.
            with open(template_path, "r") as t:
                template_content = t.read()
                print(f"Read template content from `{template_path}` successfully.")

            # 4. Use `markdown_to_html_node` function and `.to_html()` method
            #    to convert the markdown file to an HTML string.
            markdown_converted = markdown_to_html_node(markdown).to_html()
            print("Converted markdown to HTML successfully.")

            # 5. Use `extract_title` to grab the title of the page.
            title = extract_title(markdown)
            print(f"Extracted title: {title}")

            # 6. Replace the `{{ Title }}` and `{{ Content }}` placeholders in the
            # template with the HTML and title you generated.
            page_content = (
                template_content.replace("{{ Title }}", title)
                .replace("{{ Content }}", markdown_converted)
                .replace('href="/', f'href="{basepath}')
                .replace('src="/', f'src="{basepath}')
            )

            # 7. Write the new full HTML page to a file at `dest_path`.
            #    Be sure to create any necessary directories if they don't exist.
            with open(dest_path, "w") as dest_file:
                dest_file.write(page_content)
                print(f"Page generated successfully at: {dest_path}")

    except Exception as e:
        raise Exception(f"Error generating page: {e}")


def generate_pages_recursive(
    dir_path_content: str, template_path: str, dest_dir_path: str, basepath: str
) -> None:
    """
    Recursively generates pages for all markdown files in a given directory.

    Args:
        dir_path_content (str): The path to the directory containing markdown files.
        template_path (str): The path to the template file.
        dest_dir_path (str): The path to the destination directory where generated pages will be saved.
        basepath (str): The base path to be used in the generated pages.

    Raises:
        Exception: If there is an error during page generation, an Exception is raised with an appropriate error message.
    """

    try:
        # Ensure the destination directory exists
        os.makedirs(dest_dir_path, exist_ok=True)

        # Iterate through each item in the content directory
        for item in os.listdir(dir_path_content):
            item_path = os.path.join(dir_path_content, item)

            if os.path.isdir(item_path):
                # Recursively handle nested subdirectories
                generate_pages_recursive(
                    item_path,
                    template_path,
                    os.path.join(dest_dir_path, item),
                    basepath,
                )
            elif item.endswith(".md"):
                # Generate page for markdown files
                dest_file_path = os.path.join(
                    dest_dir_path, item.replace(".md", ".html")
                )
                generate_page(item_path, template_path, dest_file_path, basepath)

    except Exception as e:
        raise Exception(f"Error generating pages recursively: {e}")
