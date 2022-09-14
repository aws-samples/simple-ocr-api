# libraries
# ---------
from typing import List, Dict
import os
import pathlib
import aws_cdk
from aws_cdk import (
    aws_lambda,
    aws_iam,
    Stack,
    Duration,
)
from constructs import Construct
from .custom_constructs import OCRService
from cdk_lambda_layer_builder.constructs import BuildPyLayerAsset

CURRENT_FILEPATH = pathlib.Path(__file__).absolute()
CURRENT_DIRPATH = CURRENT_FILEPATH.parent.absolute()
PROJECT_DIRPATH: pathlib.Path = CURRENT_DIRPATH.parent.parent.absolute()
LAMBDA_DIRPATH = PROJECT_DIRPATH / "lambda"
LIB_DIRPATH: pathlib.Path = LAMBDA_DIRPATH / "libs"


class OcrServiceStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        lambda_python_version = aws_lambda.Runtime.PYTHON_3_8

        #### Lambda layers #####
        ########################

        ocrtools_layer_asset = BuildPyLayerAsset.from_modules(
            self,
            "OCRToolsAsset",
            local_module_dirs=[LIB_DIRPATH / "ocr_tools"],
            py_runtime=lambda_python_version,
        )

        ocrtools_layer = aws_lambda.LayerVersion(
            self,
            id="OCRToolsLayer",
            code=aws_lambda.Code.from_bucket(
                ocrtools_layer_asset.asset_bucket, ocrtools_layer_asset.asset_key
            ),
            compatible_runtimes=[lambda_python_version],
            description="OCRTools library",
        )

        #### OCR use cases #####
        ###########################

        analyze_document_policy = aws_iam.Policy(
            self,
            "AnalyzeDocumentPolicy",
            statements=[
                aws_iam.PolicyStatement(
                    actions=["textract:AnalyzeDocument"],
                    resources=["*"],
                )
            ],
        )

        detect_document_text_policy = aws_iam.Policy(
            self,
            "DetectDocumentTextPolicy",
            statements=[
                aws_iam.PolicyStatement(
                    actions=["textract:DetectDocumentText"],
                    resources=["*"],
                )
            ],
        )

        lambda_props = aws_lambda.FunctionProps(
            runtime=lambda_python_version,
            handler="main.handler",
            code=aws_lambda.Code.from_asset(os.path.join(LAMBDA_DIRPATH)),
            timeout=Duration.seconds(5 * 60),
            layers=[ocrtools_layer],            retry_attempts=0,
            memory_size=2000,
        )

        ocr_service = OCRService(self, "OCRService")

        ocr_service.add_use_case(
            id="extract-text",
            use_case_name="extract-text",
            function_props=lambda_props,
            additional_lambda_role_policies=[detect_document_text_policy],
            api_resource_path="extract-text",
        )

        ocr_service.add_use_case(
            id="extract-key-value-pairs",
            use_case_name="extract-key-value-pairs",
            function_props=lambda_props,
            additional_lambda_role_policies=[analyze_document_policy],
            api_resource_path="extract-key-value-pairs",
        )

        ocr_service.add_use_case(
            id="extract-tables",
            use_case_name="extract-tables",
            function_props=lambda_props,
            additional_lambda_role_policies=[analyze_document_policy],
            api_resource_path="extract-tables",
        )

        aws_cdk.CfnOutput(
            self,
            "base-api-invoke-url",
            value=f"https://{ocr_service.api_id}.execute-api.{self.region}.amazonaws.com/prod/",
            export_name=f"{self.stack_name}-api-endpoint",
        )

        use_case_urls = self.get_use_case_urls(ocr_service)
        for item in use_case_urls:
            print(item)
            aws_cdk.CfnOutput(
                self,
                f'{item["name"]}-invoke-url',
                value=item["url"],
                export_name=f'{self.stack_name}-{item["name"]}-endpoint',
            )

    def get_use_case_urls(self, ocr_service: OCRService) -> List[Dict[str, str]]:
        use_case_urls: List[Dict] = []
        for use_case in ocr_service.use_cases:
            use_case_url_by_name: Dict = {}
            use_case_id = use_case.name
            use_case_url = f"https://{ocr_service.api_id}.execute-api.{self.region}.amazonaws.com/prod/{use_case.resource_path}"
            use_case_url_by_name["name"] = use_case_id
            use_case_url_by_name["url"] = use_case_url
            use_case_urls.append(use_case_url_by_name)
        return use_case_urls
