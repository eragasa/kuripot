# src/kuripot/core/net.py

from __future__ import annotations

from dataclasses import dataclass, field

from .archive import KuripotArchive
from .operator import KuripotOperator
from .token import KuripotToken


@dataclass
class KuripotNet:
    """
    A backend-independent semantic representation of a Kuripot workflow net.

    A KuripotNet stores archives, operators, tokens, and arcs without committing
    to a specific execution backend such as SNAKES, NetworkX, SimPN, or PM4Py.

    In Petri-net language:

    - archives correspond to places
    - operators correspond to transitions
    - tokens correspond to marked objects in places
    - input arcs connect archives to operators
    - output arcs connect operators to archives

    Parameters
    ----------
    net_id:
        Stable identifier for the workflow net.
    """

    net_id: str

    archives: dict[str, KuripotArchive] = field(default_factory=dict)
    operators: dict[str, KuripotOperator] = field(default_factory=dict)

    archive_tokens: dict[str, list[KuripotToken]] = field(default_factory=dict)

    input_arcs: list[tuple[str, str, KuripotToken]] = field(default_factory=list)
    output_arcs: list[tuple[str, str, KuripotToken]] = field(default_factory=list)

    def add_archive(
        self,
        archive: KuripotArchive,
        tokens: list[KuripotToken] | None = None,
    ) -> None:
        """
        Add an archive to the net.

        If tokens are provided, they are inserted into the archive's initial
        token list.
        """

        self.archives[archive.archive_id] = archive
        self.archive_tokens.setdefault(archive.archive_id, [])

        if tokens is not None:
            self.archive_tokens[archive.archive_id].extend(tokens)

    def add_operator(
        self,
        operator: KuripotOperator,
    ) -> None:
        """
        Add an operator to the net.
        """

        self.operators[operator.operator_id] = operator

    def add_input_arc(
        self,
        archive: KuripotArchive,
        operator: KuripotOperator,
        token: KuripotToken,
    ) -> None:
        """
        Add an input arc from an archive to an operator.

        This records that the operator consumes the specified token from the
        archive when translated into an executable Petri-net backend.
        """

        self.input_arcs.append(
            (
                archive.archive_id,
                operator.operator_id,
                token,
            )
        )

    def add_output_arc(
        self,
        operator: KuripotOperator,
        archive: KuripotArchive,
        token: KuripotToken,
    ) -> None:
        """
        Add an output arc from an operator to an archive.

        This records that the operator produces the specified token into the
        archive when translated into an executable Petri-net backend.
        """

        self.output_arcs.append(
            (
                operator.operator_id,
                archive.archive_id,
                token,
            )
        )