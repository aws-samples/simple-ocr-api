from mangum import Mangum
from util.core import throwErrorHttp, get_lambda_logger
import ocr_tools
from interfaces.core import ExtractData, ExtractDataResp
from fastapi import FastAPI


app = FastAPI()

logger = get_lambda_logger()


@app.post("/extract-text", response_model=ExtractDataResp)
def extract_text(payload: ExtractData):
    """Extracts text from an input document and returns the result.

    Args:
        payload (ExtractData): Event payload containing a document stream encoded as Base64. Defaults to extract_text_examples.

    Returns:
        response (ExtractDataResp): Response containing the type of content extracted (plain-text, key-value pairs, or tables) and the extracted string.
    """

    try:
        logger.info("Starting data extraction")
        document_bytes = ocr_tools.convert_to_binary(payload.documentStream)
        detected_text = ocr_tools.process_text(document_byte_stream=document_bytes)

        response = {"contentType": "text", "extractedData": detected_text}
        logger.info("Data successfully extracted.")
        return response

    except Exception as e:
        logger.info("Data extraction failed")
        logger.error(e, exc_info=True)
        throwErrorHttp(e)


@app.post("/extract-key-value-pairs", response_model=ExtractDataResp)
def extract_key_value_pairs(payload: ExtractData):
    """Extracts key-value pairs from an input document and returns the result.

    Args:
        payload (ExtractData): Event payload containing a document stream encoded as Base64. Defaults to extract_key_value_pairs_examples.

    Returns:
        response (ExtractDataResp): Response containing the type of content extracted (plain-text, key-value pairs, or tables) and the extracted string.
    """

    try:
        logger.info("Starting data extraction")
        document_bytes = ocr_tools.convert_to_binary(payload.documentStream)
        key_value_pairs = ocr_tools.process_key_value_pairs(document_bytes)

        response = {"contentType": "key-value pairs", "extractedData": key_value_pairs}
        logger.info("Data successfully extracted.")
        return response

    except Exception as e:
        logger.info("Data extraction failed")
        logger.error(e, exc_info=True)
        throwErrorHttp(e)


@app.post("/extract-tables", response_model=ExtractDataResp)
def extract_tables(payload: ExtractData):
    """Extracts tables from an input document and returns the result.

    Args:
        payload (ExtractData): Event payload containing a document stream encoded as Base64. Defaults to extract_tables_examples.

    Returns:
        response (ExtractDataResp): Response containing the type of content extracted (tables) and the extracted string.
    """

    try:
        logger.info("Starting data extraction")
        document_bytes = ocr_tools.convert_to_binary(payload.documentStream)
        tables = ocr_tools.process_tables(document_byte_stream=document_bytes)

        response = {"contentType": "tables", "extractedData": tables}

        logger.info("Data successfully extracted.")
        return response

    except Exception as e:
        logger.info("Data extraction failed")
        logger.error(e, exc_info=True)
        throwErrorHttp(e)


handler = Mangum(app=app)
