#!/usr/bin/env python3
import os

import aws_cdk as cdk

from infrastructure.ocr_service_stack import OcrServiceStack


app = cdk.App()
OcrServiceStack(
    app,
    "OcrServiceStack",
)

app.synth()
