from pathlib import Path
from rlanutils.io.fs import read_yaml
from rlanutils.io.fs import mktmpdir

def test_read_yaml_compatible_with_pathlib_path():
    tmp_dir = mktmpdir()
    with open(tmp_dir / "test.yaml", "w") as f:
        f.write("a: 1\nb: 2")
    test_yaml = tmp_dir / "test.yaml"
    assert read_yaml(test_yaml) == {"a": 1, "b": 2}
