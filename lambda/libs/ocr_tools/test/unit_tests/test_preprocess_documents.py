from email import message
from ocr_tools import convert_to_binary
from pathlib import Path
import pytest


@pytest.fixture
def base64_file() -> str:
    return Path(__file__).parent.parent / "mocks/base_64.txt"


@pytest.fixture
def test_sample_1(base64_file) -> str:
    with open(base64_file, "r") as f:
        file = f.read()
    return file


@pytest.fixture
def byte_stream():
    string = "this is some text"
    byte_stream = string.encode("ascii")
    return byte_stream


def test_convert_to_binary(test_sample_1):
    """Test base64 succesfully converts to binary format.

    Args:
        test_sample_1 (str): a base64-encoded string
    """
    doc_as_binary = convert_to_binary(test_sample_1)
    assert type(doc_as_binary) == bytes


def test_raises_exception_with_incorrect_input(byte_stream):
    with pytest.raises(ValueError) as excinfo:
        doc_as_binary = convert_to_binary(byte_stream)
    assert "Document stream must be a base64 string." in str(excinfo.value)
