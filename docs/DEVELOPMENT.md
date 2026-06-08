# Development Notes

## Test organization

KURIPOT tests are organized by package namespace and behavioral case.

For small classes, a single test file per class is acceptable:

```text
tests/kuripot/core/test_KuripotToken.py
tests/kuripot/core/test_KuripotArchive.py
tests/kuripot/core/test_KuripotOperator.py
```

For more complex adapters, tests are split by behavior:

```text
tests/kuripot/io/networkx/
    conftest.py
    test_NetworkXIO_protocol.py
    test_NetworkXIO_validation.py
    test_NetworkXIO_empty.py
    test_NetworkXIO_nodes.py
    test_NetworkXIO_edges.py
```

The reason for this split is that I/O adapters have several independent responsibilities:

- satisfying the public I/O protocol
- validating a semantic net before export
- exporting empty nets
- exporting archive and operator nodes
- exporting input and output arcs
- preserving token metadata

Keeping these cases in separate files makes each test file answer one question. This is preferable to one large adapter test file because adapter behavior will grow as new backends are added.

## Fixture policy

Fixtures are used only when they represent reusable semantic objects or canonical workflows.

Good fixture candidates:

- adapter instances such as `networkx_io`
- canonical nets such as `simple_transition_net`
- deliberately malformed imported/deserialized nets such as `invalid_raw_net`

Avoid micro-fixtures for one-off objects that are clearer when constructed inside the test body.

For example, this is usually unnecessary:

```python
@pytest.fixture
def archive() -> KuripotArchive:
    return KuripotArchive(archive_id="state_archive")
```

when the archive is used in only one test.

Prefer local construction:

```python
archive = KuripotArchive(archive_id="state_archive")
```

inside the test.

## Validation policy

KURIPOT uses fail-early construction for normal public API use. Archives and operators must be added to a `KuripotNet` before arcs are created between them.

The `validate()` method remains necessary because future loaders, serializers, importers, or external adapters may construct nets from raw data. In those cases, malformed references may enter the object before public methods are called.

Therefore:

```text
add_input_arc()
add_output_arc()
    fail early during normal construction

validate()
    checks consistency before export or after import/deserialization
```

All I/O adapters should call:

```python
net.validate()
```

before exporting to an external representation.

## Test naming convention

Test files for class-level behavior may follow the class name:

```text
test_KuripotNet.py
test_KuripotToken.py
```

Case-split adapter tests should include both the adapter name and the behavior:

```text
test_NetworkXIO_validation.py
test_NetworkXIO_edges.py
```

Avoid repeating the same basename in different folders, such as multiple files named `test_exports.py`, unless the test directories are explicitly packaged. Repeated basenames can cause pytest import-mismatch errors.