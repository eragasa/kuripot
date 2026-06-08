# src/kuripot/io/io_mermaid.py

from __future__ import annotations

from kuripot.core.net import KuripotNet


class MermaidIO:
    """
    I/O adapter that exports a KuripotNet to Mermaid flowchart syntax.

    Mermaid export is intended for documentation, Markdown, Obsidian, GitHub,
    and quick visual inspection. It is not an execution backend.

    Archives are rendered as rounded nodes.
    Operators are rendered as rectangular nodes.
    Input arcs point from archives to operators.
    Output arcs point from operators to archives.
    """

    def export(
        self,
        net: KuripotNet,
    ) -> str:
        """
        Export a KuripotNet as a Mermaid flowchart string.
        """

        net.validate()

        lines: list[str] = ["flowchart LR"]

        for archive_id in net.archives:
            lines.append(
                f'    {self._node_id(archive_id)}(({archive_id}))'
            )

        for operator_id in net.operators:
            lines.append(
                f'    {self._node_id(operator_id)}["{operator_id}"]'
            )

        for archive_id, operator_id, token in net.input_arcs:
            lines.append(
                f'    {self._node_id(archive_id)} '
                f'-- "{token.token_id}" --> '
                f'{self._node_id(operator_id)}'
            )

        for operator_id, archive_id, token in net.output_arcs:
            lines.append(
                f'    {self._node_id(operator_id)} '
                f'-- "{token.token_id}" --> '
                f'{self._node_id(archive_id)}'
            )

        return "\n".join(lines)

    def _node_id(
        self,
        value: str,
    ) -> str:
        """
        Convert a Kuripot identifier into a Mermaid-safe node identifier.
        """

        safe = value.replace("-", "_").replace(".", "_").replace(" ", "_")

        return f"node_{safe}"