import argparse
import sys
import pytest

from rlanutils.io.args import KeyValueAction


def test_key_value_action():
    parser = argparse.ArgumentParser()
    parser.add_argument("--keyvalue", nargs="+", action=KeyValueAction)
    args = parser.parse_args(["--keyvalue", "key1=val1", "key2=val2"])

    assert args.keyvalue == {"key1": "val1", "key2": "val2"}, "The KeyValueAction did not parse the arguments correctly"


def test_key_value_action_with_invalid_input():
    if sys.version_info.major == 3 and sys.version_info.minor > 8:
        parser = argparse.ArgumentParser(exit_on_error=False)
        parser.add_argument("--keyvalue", nargs="+", action=KeyValueAction)

        with pytest.raises(argparse.ArgumentError):
            args = parser.parse_args(["--keyvalue", "key1val1"])
