# kuripot/io/io_snakes.py

from __future__ import annotations

from snakes.nets import PetriNet, Place, Transition, Value

from kuripot.core.net import KuripotNet


class SnakesIO:
    name = "snakes"

    def export(
        self,
        net: KuripotNet,
    ) -> PetriNet:
        snakes_net = PetriNet(net.name)

        for archive_name, archive in net.archives.items():
            tokens = [
                Value(token)
                for token in net.archive_tokens.get(archive_name, [])
            ]

            snakes_net.add_place(
                Place(
                    archive.name,
                    tokens,
                )
            )

        for operator in net.operators.values():
            snakes_net.add_transition(
                Transition(operator.name)
            )

        for archive_name, operator_name, token in net.input_arcs:
            snakes_net.add_input(
                archive_name,
                operator_name,
                Value(token),
            )

        for operator_name, archive_name, token in net.output_arcs:
            snakes_net.add_output(
                archive_name,
                operator_name,
                Value(token),
            )

        return snakes_net