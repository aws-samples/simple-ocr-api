from pydantic import BaseModel


class ExtractData(BaseModel):
    documentStream: str


class ExtractDataResp(BaseModel):
    contentType: str
    extractedData: str
