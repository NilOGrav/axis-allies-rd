"""Text renderer: the resolved layout as plain text."""

import os


def render_terminal(graph, resolved_layout):

    lines = []

    nodes_by_position = sorted(
        resolved_layout["nodes"].items(),
        key=lambda item: (
            item[1]["column"],
            item[1]["row"]
        )
    )

    current_column = None

    for tech_id, position in nodes_by_position:

        column = position["column"]

        if current_column is not None and column != current_column:
            lines.append("")

        current_column = column

        node = graph["nodes"][tech_id]

        lines.append(
            f"row {position['row']:>3}: "
            f"{tech_id} - {node['name']}"
        )

    return "\n".join(lines)


def write_text_file(text, output_file):

    os.makedirs(os.path.dirname(output_file) or ".", exist_ok=True)

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(text)
        f.write("\n")


def render_text(graph, resolved_layout, terminal_file):

    terminal_output = render_terminal(
        graph,
        resolved_layout
    )

    print(terminal_output)

    write_text_file(
        terminal_output,
        terminal_file
    )
