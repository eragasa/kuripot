# src/kuripot/io/io_snakes.py

from __future__ import annotations

from snakes.nets import PetriNet, Place, Transition, Value

from kuripot.core.net import KuripotNet


class SnakesIO:
    """
    I/O adapter that exports a KuripotNet to a SNAKES PetriNet.

    The exported Petri net is executable by SNAKES. Archives become places,
    operators become transitions, archive tokens become initial place tokens,
    input arcs consume tokens from places, and output arcs produce tokens into
    places.
    """

    def export(
        self,
        net: KuripotNet,
    ) -> PetriNet:
        """
        Export a KuripotNet as a SNAKES PetriNet.
        """

        snakes_net = PetriNet(net.net_id)

        for archive_id, archive in net.archives.items():
            # Places store the actual KuripotToken objects.
            # Arc annotations use Value(token) to match/produce those objects.
            tokens = list(net.archive_tokens.get(archive_id, []))

            snakes_net.add_place(
                Place(
                    archive.archive_id,
                    tokens,
                )
            )

        for operator in net.operators.values():
            snakes_net.add_transition(
                Transition(operator.operator_id)
            )

        for archive_id, operator_id, token in net.input_arcs:
            snakes_net.add_input(
                archive_id,
                operator_id,
                Value(token),
            )

        for operator_id, archive_id, token in net.output_arcs:
            snakes_net.add_output(
                archive_id,
                operator_id,
                Value(token),
            )

        return snakes_net