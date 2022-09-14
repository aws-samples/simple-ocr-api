import base64
from typing import ByteString


def convert_to_binary(encoded_document: str) -> ByteString:
    """Converts base64 encoded document to bytes.

    Args:
        encoded_document (str): base64 encoded document.

    Raises:
        IncompleteDocumentStream: the input document stream is incomplete and cannot be converted.

    Returns:
        document_as_bytes (ByteString): the input document encoded as bytes.
    """
    if not isinstance(encoded_document, str):
        raise ValueError("Document stream must be a base64 string.")
    else:
        document_as_bytes = base64.b64decode(encoded_document)
        return document_as_bytes
