import pytest
from pathlib import Path
from PIL import Image
import io
from ocr_tools import extract_text, extract_key_value_pairs, extract_tables


@pytest.fixture
def img_bytes() -> bytes:
    img_file_path = Path(__file__).parent.parent / "mocks/all-content.png"
    img_byte_arr = io.BytesIO()
    img = Image.open(img_file_path)
    img.save(img_byte_arr, format=img.format)
    img_bytes = img_byte_arr.getvalue()
    return img_bytes


def test_extract_text(img_bytes):
    """Tests the extract_text function returns a dictionary when sent an image byte stream.

    Args:
        img_bytes (bytes): an image encoded as bytes
    """
    response = extract_text(document_byte_stream=img_bytes)
    assert type(response) == dict


def test_extract_key_value_pairs(img_bytes):
    """Tests the extract_key_value_pairs function returns a dictionary when sent an image byte stream.

    Args:
        img_bytes (bytes): an image encoded as bytes
    """
    response = extract_key_value_pairs(document_byte_stream=img_bytes)
    assert type(response) == dict


def test_extract_tables(img_bytes):
    """Tests the extract_tables function returns a dictionary when sent an image byte stream.

    Args:
        img_bytes (bytes): an image encoded as bytes
    """
    response = extract_tables(document_byte_stream=img_bytes)
    assert type(response) == dict
