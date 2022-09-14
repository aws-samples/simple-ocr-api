from .ocr_use_case import OCRServiceUseCase
from constructs import Construct
from aws_cdk import aws_apigateway, aws_lambda, aws_iam, aws_cognito
from typing import List, Optional, Union


class OCRService(Construct):
    def __init__(
        self,
        scope: Construct,
        id: str,
        custom_auth: Union[aws_apigateway.Authorizer, None] = None,
        custom_auth_type: Union[aws_apigateway.AuthorizationType, None] = None,
        **kwargs,
    ) -> None:

        super().__init__(scope, id)

        self.api = aws_apigateway.RestApi(
            self, "ocr-service-api", rest_api_name=f"OCRServiceAPI"
        )
        self.use_cases: List[OCRServiceUseCase] = []
        self.auth = self._get_auth(custom_auth)
        self.auth_type = self._get_auth_type(custom_auth_type)

    @property
    def api_id(self) -> str:
        return self.api.rest_api_id

    @property
    def get_use_cases(self) -> str:
        return self.use_cases

    def add_use_case(
        self,
        id: str,
        use_case_name: str,
        function_props: aws_lambda.FunctionProps,
        api_resource_path: str,
        additional_lambda_role_policies: Optional[
            List[Union[aws_iam.Policy, aws_iam.ManagedPolicy]]
        ] = None,
    ):
        """Adds a new use case to the Simple OCR Service .
        A use case is a Lambda function fronted by an API Gateway resource. The Lambda function performs an OCR task, such as extracting text from an image.
        Args:
            id (str): the id of the use case
            use_case_name (str): the name of the use case
            function_props (aws_lambda.FunctionProps): the properties of the lambda function
            api_resource_path (str): the path of the API Gateway resource for this use case
            additional_lambda_role_policies (Optional[ List[Union[aws_iam.Policy, aws_iam.ManagedPolicy]] ], optional): additional IAM policies to attach to the Lambda function. Defaults to None.
        """
        self.use_cases.append(
            OCRServiceUseCase(
                self,
                id=id,
                use_case_name=use_case_name,
                function_props=function_props,
                rest_api=self.api,
                additional_lambda_role_policies=additional_lambda_role_policies,
                api_resource_path=api_resource_path,
                auth=self.auth,
                auth_type=self.auth_type,
            )
        )
        return self.use_cases[-1]

    def _get_auth(self, custom_auth):
        if custom_auth == None:
            auth = None
        else:
            assert isinstance(
                custom_auth, aws_apigateway.Authorizer
            ), "custom_auth must be an instance of aws_apigateway.Authorizer"
            auth = custom_auth
        return auth

    def _get_auth_type(self, custom_auth_type):
        if custom_auth_type == None:
            auth_type = None
        else:
            auth_type = custom_auth_type

        return auth_type
