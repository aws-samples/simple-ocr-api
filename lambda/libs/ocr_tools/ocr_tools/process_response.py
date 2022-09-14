import csv
from typing import Dict
import json

from textractprettyprinter.t_pretty_print import (
    Pretty_Print_Table_Format,
    Textract_Pretty_Print,
    get_string,
    get_tables_string,
)


def reformat_key_value_pairs(kvp_string: str) -> str:
    """Reformats key value pairs string into a JSON format.

    Args:
        kvp_string (str): a string containing key-value pairs in the format "key,value\r\nkey-1,value-1\r\nkey-2,value-2"


    Returns:
        kv_dict (Dict[str, str]): a string in the format '{"key-1":"value-1","key-2":"value-2"}'
    """
    kv_dict: Dict[str, str] = {}
    rows = list(csv.reader(kvp_string.splitlines()))
    for row in rows[1:]:  # first row is excluded because it contains headers
        if len(row) > 0:
            kv_dict[row[0]] = row[1]
    return json.dumps(kv_dict)


def get_text(textract_response: Dict) -> str:
    """Extracts text as lines from Amazon Textract response.

    Args:
        textract_response (Dict): Response from Textract Detect Text API.

    Returns:
        text (str): Extracted text in line format.
    """
    text = get_string(textract_response, output_type=[Textract_Pretty_Print.LINES])
    return text


def get_tables(textract_response: Dict) -> str:
    """Extract tables from Amazon Textract response.

    Args:
        textract_response (Dict): Response from Textract Analyze Document API.

    Returns:
        tables (str): Extracted tables in CSV format.
    """

    tables = get_tables_string(
        textract_json=textract_response,
        table_format=Pretty_Print_Table_Format.csv,
    )
    return tables


def get_key_value_pairs(textract_response: Dict) -> str:
    """Extract key-value pairs from Amazon Textract response.

    Args:
        textract_response (Dict): Response from Textract Analyze Document API.

    Returns:
        key_vals (str): Extracted key-value pairs.
    """
    key_vals = get_string(
        textract_json=textract_response,
        output_type=[Textract_Pretty_Print.FORMS],
        table_format=Pretty_Print_Table_Format.csv,
    )

    reformatted_key_vals = reformat_key_value_pairs(key_vals)

    return reformatted_key_vals
