# examples/mermaid_demo.py

from __future__ import annotations

from kuripot import Kuripot
from kuripot.io import MermaidIO


def main() -> None:
    k = Kuripot()

    net = k.create_net("demo_net")

    state_archive = k.create_archive("state_archive")
    updated_archive = k.create_archive("updated_state_archive")
    operator = k.create_operator("operator_generator")

    state_0 = k.create_token("state_0")
    state_1 = k.create_token("state_1")

    net.add_archive(state_archive, tokens=[state_0])
    net.add_archive(updated_archive)
    net.add_operator(operator)

    net.add_input_arc(state_archive, operator, state_0)
    net.add_output_arc(operator, updated_archive, state_1)

    mermaid = MermaidIO().export(net)

    print("```mermaid")
    print(mermaid)
    print("```")


if __name__ == "__main__":
    main()