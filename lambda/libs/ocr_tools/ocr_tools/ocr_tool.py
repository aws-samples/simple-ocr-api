# TO DO: remove try-except
#

from typing import ByteString
import ocr_tools


def process_text(document_byte_stream: ByteString) -> str:
    """Extracts and formats text from document.

    Args:
        document_byte_stream (ByteString): the input document as a byte stream.
        is_pdf (bool): whether the document is a PDF or not.

    Returns:
        values (str): the detected text.
    """

    response = ocr_tools.extract_text(document_byte_stream)
    values = ocr_tools.get_text(response)

    return values


def process_key_value_pairs(document_byte_stream: ByteString) -> str:
    """Extracts and formats key-value pairs from input document.

    Args:
        document_byte_stream (ByteString): the input document as a byte stream.
        is_pdf (bool): whether the document is a PDF or not.

    Returns:
        values (str): the detected key-value pairs.
    """

    response = ocr_tools.extract_key_value_pairs(document_byte_stream)
    values = ocr_tools.get_key_value_pairs(response)

    return values


def process_tables(document_byte_stream: ByteString) -> str:
    """Extracts and formats tables from document.

    Args:
        document_byte_stream (ByteString): the input document as a byte stream.
        is_pdf (bool): whether the document is a PDF or not.

    Returns:
        values (str): the detected tables.
    """
    response = ocr_tools.extract_tables(document_byte_stream)
    values = ocr_tools.get_tables(response)

    return values
