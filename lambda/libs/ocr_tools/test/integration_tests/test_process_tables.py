import pytest
from pathlib import Path
from PIL import Image
import io
import ocr_tools


def get_img_bytes(img_file_path: Path) -> bytes:
    img_byte_arr = io.BytesIO()
    img = Image.open(img_file_path)
    img.save(img_byte_arr, format=img.format)
    img_bytes = img_byte_arr.getvalue()
    return img_bytes


def get_pdf_bytes(pdf_file_path: Path) -> bytes:
    with open(pdf_file_path, "rb") as f:
        pdf_bytes = f.read()
    return pdf_bytes


@pytest.fixture
def test_sample_1() -> bytes:
    document_bytes = get_img_bytes(
        Path(__file__).parent.parent / "mocks/all-content.png"
    )
    return document_bytes


@pytest.fixture
def test_sample_2() -> bytes:
    document_bytes = get_pdf_bytes(
        Path(__file__).parent.parent / "mocks/all-content-type.pdf"
    )
    return document_bytes


@pytest.fixture
def test_sample_3() -> bytes:
    document_bytes = get_img_bytes(
        Path(__file__).parent.parent / "mocks/blank-image.png"
    )
    return document_bytes


def test_process_tables_img_input(test_sample_1):
    """Verify a non-empty string is returned when process_tables() is called with an image file.

    Args:
        test_sample_1 (bytes): an image file encoded in bytes"""
    tables = ocr_tools.process_tables(test_sample_1)
    assert type(tables) == str
    assert len(tables) != 0


def test_process_tables_pdf_input(test_sample_2):
    """Verify a non-empty string is returned when process_tables() is called with an PDF file.

    Args:
        test_sample_2 (bytes): a PDF file encoded in bytes"""
    tables = ocr_tools.process_tables(test_sample_2)
    assert type(tables) == str
    assert len(tables) != 0


def test_process_tables_blank_input(test_sample_3):
    """Verify no content is extracted when process_tables() is called with an empty file.

    Args:
        test_sample_3 (bytes): a blank image file encoded in bytes"""
    tables = ocr_tools.process_tables(test_sample_3)
    assert type(tables) == str
    assert len(tables) == 0
