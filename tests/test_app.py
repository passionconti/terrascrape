import sys


def test_python_version():
    assert sys.version_info.major == 3
    assert sys.version_info.minor == 7
