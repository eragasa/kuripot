# kuripot
KURIPOT is a lightweight framework for representing scientific workflows as archived states, executable operators, and traceable transformations.

KURIPOT stands for:

`Knowledge-Unit Repository for Interpretable Processes, Operators, and Traces`

The framework treats a workflow as a state-transition system. Archives store explicit state tokens. Operators consume tokens from input archives and produce tokens in output archives. Execution traces record how states, artifacts, models, datasets, and derived outputs are produced.

The initial implementation uses Petri-net semantics, with later support planned for graph export, simulation, and process-mining backends.



## Local Installation

Local installation

Create a local virtual environment:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

Verify the active Python environment:

```bash
python --version
which python
```

Expected output:

```bash
Python 3.12.x
/Users/eugene/repos/eugeneragasa/code/kuripot/.venv/bin/python
```

Install the package in editable mode with development dependencies:

```
python -m pip install --upgrade pip setuptools
python -m pip install -e ".[dev]"
pytest
```

```bash
python3.12 -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip setuptools
python -m pip install -e ".[dev]"
pytest
```

expected response

```bash
Python 3.12.x
/Users/eugene/repos/eugeneragasa/code/kuripot/.venv/bin/python
```

Install the package

python -m pip install --upgrade pip setuptools
python -m pip install -e ".[dev]"
pytest

`Kuripot`
- creates semantic objects
- owns registry of IO adapters
- spawns backend implementations

`KuripotNet`
- backend-independent semantic graph/net object

`io_snakes.py`
- converts KuripotNet $\leftrightarrow$ SNAKES PetriNet

`io_networkx.py`
- converts KuripotNet $\leftrightarrow$ NetworkX graph

`io_pm4py.py`
- converts KuripotNet $\leftrightarrow$ PMPy net


## License
This repository uses separate terms for source code and non-code materials.

Source code is licensed under the Apache License, Version 2.0. See `LICENSE`.

Documentation, diagrams, lecture material, examples, explanatory text, and other non-code educational or research materials are licensed under the Creative Commons Attribution-NonCommercial 4.0 International License. See `LICENSE-DOCS`.

Commercial use of the non-code materials is not permitted without written permission from the copyright holder.

## Citation

# KURIPOT

KURIPOT is a lightweight framework for representing scientific workflows as archived states, executable operators, and traceable transformations.

KURIPOT stands for:

```text
Knowledge-Unit Repository for Interpretable Processes, Operators, and Traces
```

The framework treats a workflow as a state-transition system. Archives store explicit state tokens. Operators consume tokens from input archives and produce tokens in output archives. Execution traces record how states, artifacts, models, datasets, and derived outputs are produced.

The initial implementation uses Petri-net semantics, with later support planned for graph export, simulation, and process-mining backends.

## Core idea

KURIPOT separates the semantic model from implementation backends.

`Kuripot`

* creates semantic objects
* owns the registry of I/O adapters
* spawns backend implementations

`KuripotNet`

* represents a backend-independent semantic graph/net object

`Archive`

* represents a state archive
* corresponds to a Petri-net place

`Operator`

* represents an executable transformation
* corresponds to a Petri-net transition

`Token`

* represents a concrete state, artifact, dataset, model, configuration, or output

`Trace`

* represents provenance and execution history

## Planned I/O adapters

`io_snakes.py`

* converts `KuripotNet` $\leftrightarrow$ SNAKES `PetriNet`

`io_networkx.py`

* converts `KuripotNet` $\leftrightarrow$ NetworkX graph

`io_pm4py.py`

* converts `KuripotNet` $\leftrightarrow$ PM4Py net or process-mining structure

## Local installation

Create a local virtual environment:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

Verify the active Python environment:

```bash
python --version
which python
```

Expected output:

```bash
Python 3.12.x
/Users/eugene/repos/eugeneragasa/code/kuripot/.venv/bin/python
```

Install the package in editable mode with development dependencies:

```bash
python -m pip install --upgrade pip setuptools
python -m pip install -e ".[dev]"
pytest
```

## Planned I/O Adaparters
`io_snakes.py` - converts `KuripotNet` $\leftrightarrow$ SNAKES
`io_networkx.py` - converts `KuripotNet` $\leftrightarrow$ NetworkX graph
`io_pm4py.py` - converts `KuripotNet` $\leftrightarrow$ PM4Py  net or process-mining structure

## Development status

This repository is in early scaffold development.

The first implementation target is a minimal backend-independent KuripotNet, followed by adapters for SNAKES and NetworkX.

## License

This repository uses separate terms for software and educational materials.

Source code, tests, examples, configuration files, and software documentation are licensed under the Apache License, Version 2.0. See `LICENSE`.

Lecture material, diagrams, explanatory essays, research notes, and other non-code educational materials are licensed under the Creative Commons Attribution-NonCommercial 4.0 International License. See `LICENSE-DOCS`.

Commercial use of the educational materials is not permitted without written permission from the copyright holder.

## Citation

If you use KURIPOT in teaching, research, software, publications, or derivative educational material, please cite this repository.

```bibtex
@software{ragasa_kuripot_2026,
  author = {Ragasa, Eugene Joseph M.},
  title = {KURIPOT: Knowledge-Unit Repository for Interpretable Processes, Operators, and Traces},
  year = {2026},
  url = {https://github.com/eugeneragasa/kuripot}
}
```



## Copyright

Copyright 2026 Eugene Joseph Medalla Ragasa.

