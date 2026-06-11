from textnode import TextNode, TextType


def split_nodes_delimiter(
    old_nodes: list[TextNode],
    delimiter: str,
    text_type: TextType,
) -> list[TextNode]:
    # ---- Pseudocode ----
    # For each old node:
    # If it is not plain text:
    #     keep it unchanged.

    # If it is plain text:
    #     split its text by the delimiter.

    #     If the number of parts is even:
    #         there was an unmatched delimiter, so raise an error.

    #     For each split part:
    #         even index = normal text
    #         odd index = delimited text type
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.PLAIN:
            new_nodes.append(old_node)
            continue

        split_text = old_node.text.split(delimiter)

        if len(split_text) % 2 == 0:
            raise ValueError(f"Invalid Markdown syntax: missing closing delimiter '{delimiter}'")

        for index, text in enumerate(split_text):
            if text == "":
                continue

            if index % 2 == 0:
                new_nodes.append(TextNode(text, TextType.PLAIN))
            else:
                new_nodes.append(TextNode(text, text_type))

    return new_nodes
