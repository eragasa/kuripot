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

    Construction policy
    -------------------
    KuripotNet uses fail-early construction for the public API. Archives and
    operators must be added to the net before arcs are created between them.

    The validate() method remains useful as a consistency check for imported,
    deserialized, or manually modified nets. Normal API usage should fail at
    the point where an invalid arc is added.

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

        # Public construction fails early: arcs may only reference registered
        # archives and operators.
        if not self.has_archive(archive.archive_id):
            raise ValueError(
                f"Input arc references unknown archive: {archive.archive_id}"
            )

        if not self.has_operator(operator.operator_id):
            raise ValueError(
                f"Input arc references unknown operator: {operator.operator_id}"
            )

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

        # Public construction fails early: arcs may only reference registered
        # archives and operators.
        if not self.has_operator(operator.operator_id):
            raise ValueError(
                f"Output arc references unknown operator: {operator.operator_id}"
            )

        if not self.has_archive(archive.archive_id):
            raise ValueError(
                f"Output arc references unknown archive: {archive.archive_id}"
            )

        self.output_arcs.append(
            (
                operator.operator_id,
                archive.archive_id,
                token,
            )
        )

    def has_archive(
        self,
        archive_id: str,
    ) -> bool:
        """
        Return True if the net contains the requested archive.
        """

        return archive_id in self.archives

    def has_operator(
        self,
        operator_id: str,
    ) -> bool:
        """
        Return True if the net contains the requested operator.
        """

        return operator_id in self.operators

    def validate(self) -> None:
        """
        Validate internal references in the semantic net.

        This checks that every input and output arc references archives and
        operators that have been added to the net.
        """

        for archive_id, operator_id, _token in self.input_arcs:
            if archive_id not in self.archives:
                raise ValueError(
                    f"Input arc references unknown archive: {archive_id}"
                )

            if operator_id not in self.operators:
                raise ValueError(
                    f"Input arc references unknown operator: {operator_id}"
                )

        for operator_id, archive_id, _token in self.output_arcs:
            if operator_id not in self.operators:
                raise ValueError(
                    f"Output arc references unknown operator: {operator_id}"
                )

            if archive_id not in self.archives:
                raise ValueError(
                    f"Output arc references unknown archive: {archive_id}"
                )