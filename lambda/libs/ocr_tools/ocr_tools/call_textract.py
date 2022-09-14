import boto3
from typing import Dict, ByteString

from .custom_errors import AWSAuthFailed


def extract_key_value_pairs(document_byte_stream: ByteString) -> Dict:
    """Extracts key-value pairs from document using Amazon Textract.

    Args:
        document_byte_stream (ByteString): input document encoded as a bytes. The document bytes must be in PNG or JPEG format.

    Raises:
        AWSAuthFailed: AWS authentication failure if AWS credentials not recognised.

    Returns:
        Dict: Dictionary containing Amazon Textract response.
    """

    client = boto3.client("textract")

    response = client.analyze_document(
        Document={
            "Bytes": document_byte_stream,
        },
        FeatureTypes=["FORMS"],
    )

    return response


def extract_tables(document_byte_stream: ByteString) -> Dict:
    """Extracts tables from document using Amazon Textract.

    Args:
        document_byte_stream (ByteString): input document encoded as a bytes. The document bytes must be in PNG or JPEG format.

    Raises:
        AWSAuthFailed: AWS authentication failure if AWS credentials not recognised.

    Returns:
        Dict: Dictionary containing Amazon Textract response.
    """

    client = boto3.client("textract")

    response = client.analyze_document(
        Document={
            "Bytes": document_byte_stream,
        },
        FeatureTypes=[
            "TABLES",
        ],
    )

    return response


def extract_text(document_byte_stream: ByteString) -> Dict:
    """Extracts text from input document using Amazon Textract.

    Args:
        document_byte_stream (ByteString): input document encoded as a bytes.The document bytes must be in PNG or JPEG format.

    Raises:
        AWSAuthFailed: AWS authentication failure if AWS credentials not recognised.

    Returns:
        Dict: Dictionary containing Amazon Textract response.
    """

    client = boto3.client("textract")
    response = client.detect_document_text(
        Document={
            "Bytes": document_byte_stream,
        },
    )
    return response
