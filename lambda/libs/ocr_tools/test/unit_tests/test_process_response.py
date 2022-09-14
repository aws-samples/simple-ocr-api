import ocr_tools
import pytest
from pathlib import Path
import json
from ocr_tools import process_response


@pytest.fixture
def return_document(document_file_path):
    with open(document_file_path) as test_response:
        resp = json.load(test_response)
    return resp


def return_txt_file(document_file_path):
    with open(document_file_path) as f:
        resp = f.read()
    return resp


@pytest.fixture
def test_sample_1():
    document = return_document(
        Path(__file__).parent.parent / "mocks/analyze-id-response.json"
    )
    return document


@pytest.fixture
def test_sample_2():
    document = return_document(
        Path(__file__).parent.parent / "mocks/detect-text-response.json"
    )
    return document


@pytest.fixture
def test_sample_3():
    document = return_document(
        Path(__file__).parent.parent / "mocks/detect-text-response.json"
    )
    return document


@pytest.fixture
def test_sample_4():
    document = return_document(
        Path(__file__).parent.parent / "mocks/analyze-document-forms.json"
    )
    return document


@pytest.fixture
def kvp_test_1():
    string = "Key,Value\r\nSubtotal,$0.00\r\nDiscount,$0.00\r\nDATE OF ISSUE:,MM/DD/YYYY\r\nINVOICE NUMBER:,00001\r\nBILLED TO,\"Client name 123 Your Street City, State, Country Zip Code Phone\"\r\nTax rate,%\r\nTax,$0.00\r\nINVOICE TOTAL,$0.00\r\nPlease pay invoice by,MM/DD/YYYY\r\nYOUR COMPANY NAME,\"Building name 123 Your + 1-541-754-3010 Street City/State, Country you@email.co.uk Zip Code yourwebsite.co.uk\"\r\n\r\n"
    return string


@pytest.fixture
def kvp_test_2():
    string = "Key,Value\r\nEXP,08/31/2014\r\nDL,11234568\r\nDOB,08/31/1977\r\nDD,00/00/0000NNNAN/ANFD/YY\r\nRSTR NONE,DONOR\r\nWGT,125 lb\r\nEYES BRN,ISS 08/31/2009\r\nHAIR,BRN\r\n\r\n"
    return string


def test_reformat_key_value_pairs(kvp_test_1):
    """Verify key value pairs are re-formatted as {"key1":"value1"}"""
    reformatted_kvp = ocr_tools.reformat_key_value_pairs(kvp_test_1)
    assert reformatted_kvp == '{"Subtotal": "$0.00", "Discount": "$0.00", "DATE OF ISSUE:": "MM/DD/YYYY", "INVOICE NUMBER:": "00001", "BILLED TO": "Client name 123 Your Street City, State, Country Zip Code Phone", "Tax rate": "%", "Tax": "$0.00", "INVOICE TOTAL": "$0.00", "Please pay invoice by": "MM/DD/YYYY", "YOUR COMPANY NAME": "Building name 123 Your + 1-541-754-3010 Street City/State, Country you@email.co.uk Zip Code yourwebsite.co.uk"}'


def test_reformat_key_value_pairs_2(kvp_test_2):
    """Verify key value pairs are re-formatted as {"key1":"value1"}"""
    reformatted_kvp = ocr_tools.reformat_key_value_pairs(kvp_test_2)
    assert reformatted_kvp == '{"EXP": "08/31/2014", "DL": "11234568", "DOB": "08/31/1977", "DD": "00/00/0000NNNAN/ANFD/YY", "RSTR NONE": "DONOR", "WGT": "125 lb", "EYES BRN": "ISS 08/31/2009", "HAIR": "BRN"}'


def test_get_text():
    """Verify a string is returned from get_text() function"""

    response_file_path = (
        Path(__file__).parent.parent / "mocks/analyze-document-tables.json"
    )
    f = open(response_file_path)
    response = json.load(f)

    text = process_response.get_text(response)

    assert type(text) == str


def test_get_tables():
    """Verify a string is returned from get_tables() function"""
    response_file_path = (
        Path(__file__).parent.parent / "mocks/analyze-document-tables.json"
    )
    f = open(response_file_path)
    response = json.load(f)
    tables = process_response.get_tables(response)
    print(tables)
    assert type(tables) == str


def test_get_key_value_pairs():
    """Verify a string is return from get_key_value_pairs() function"""
    response_file_path = (
        Path(__file__).parent.parent / "mocks/analyze-document-forms.json"
    )
    f = open(response_file_path)
    response = json.load(f)
    key_value_pairs = process_response.get_key_value_pairs(response)
    assert key_value_pairs == '{"Key1:": "key2", "Palm-tree colour:": "green"}'
