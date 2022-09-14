from typing import List, Optional, Union

from aws_cdk import aws_lambda, aws_iam, aws_apigateway
from constructs import Construct


class OCRServiceUseCase(Construct):
    def __init__(
        self,
        scope: Construct,
        id: str,
        use_case_name: str,
        function_props: aws_lambda.FunctionProps,
        rest_api: aws_apigateway.RestApi,
        api_resource_path: str,
        auth: aws_apigateway.IAuthorizer,
        auth_type: aws_apigateway.AuthorizationType,
        additional_lambda_role_policies: Optional[
            List[Union[aws_iam.Policy, aws_iam.ManagedPolicy]]
        ] = None,
        **kwargs,
    ) -> None:
        """Creates a new use case for the Simple OCR Service .

        A use case is a Lambda function fronted by an API Gateway resource. The Lambda function performs an OCR task, such as extracting text from an image.

        Args:
            scope (Construct): _description_
            id (str): _description_
            use_case_name (str): the name of the use case
            function_props (aws_lambda.FunctionProps): the properties of the lambda function
            rest_api (aws_apigateway.RestApi): the rest api to attach the lambda function to
            api_resource_path (str): the path of the API Gateway resource
            additional_lambda_role_policies (Optional[ List[Union[aws_iam.Policy, aws_iam.ManagedPolicy]] ], optional): additional IAM policies to attach to the Lambda function. Defaults to None.
        """

        super().__init__(scope, id)
        self.use_case_name = use_case_name
        self.api_resource_path = api_resource_path
        self.use_case_name = use_case_name
        self.rest_api = rest_api
        self.auth = auth
        self.auth_type = auth_type
        self.api_resource_path = api_resource_path
        self.lambda_function = self._create_lambda_function(
            function_props, additional_lambda_role_policies
        )
        self.resource = self._add_api_gateway_resource()

    @property
    def resource_path(self):
        return self.api_resource_path

    @property
    def name(self):
        return self.use_case_name

    def _add_policies_to_lambda_role(
        self, lambda_function, additional_lambda_role_policies
    ):
        """Adds additional policies to the Lambda function role.

        Raises:
            ValueError: raised if additional_lambda_role_policies is not None and not a list of either aws_iam.Policy or aws_iam.ManagedPolicy
        """
        # if additional_lambda_role_policies != None:
        for policy in additional_lambda_role_policies:

            if isinstance(policy, aws_iam.Policy):
                lambda_function.role.attach_inline_policy(policy)

            elif isinstance(policy, aws_iam.ManagedPolicy):
                lambda_function.role.add_managed_policy(policy)

            else:
                raise ValueError(
                    f"Policy {policy} is not a valid policy. Must be either aws_iam.Policy or aws_iam.ManagedPolicy"
                )

    def _create_lambda_function(
        self,
        function_props: aws_lambda.FunctionProps,
        additional_lambda_role_policies: Optional[
            List[Union[aws_iam.Policy, aws_iam.ManagedPolicy]]
        ],
    ):
        """Creates the Lambda function for the Simple OCR Service  use case.

        Args:
            function_props (aws_lambda.FunctionProps): the properties of the lambda function
            additional_lambda_role_policies (Optional[ List[Union[aws_iam.Policy, aws_iam.ManagedPolicy]] ], optional): additional IAM policies to attach to the Lambda function. Defaults to None."""
        lambda_function = aws_lambda.Function(
            self,
            id=f"{self.use_case_name}Lambda",
            runtime=function_props.runtime,
            handler=function_props.handler,
            code=function_props.code,
            timeout=function_props.timeout,
            layers=function_props.layers,
            retry_attempts=function_props.retry_attempts,
            memory_size=function_props.memory_size,
        )
        if additional_lambda_role_policies != None:
            self._add_policies_to_lambda_role(
                lambda_function, additional_lambda_role_policies
            )

        return lambda_function

    def _add_api_gateway_resource(self):
        """Adds an API resource for the Simple OCR Service  use case to the API Gateway."""
        lambda_integration = aws_apigateway.LambdaIntegration(self.lambda_function)
        resource = self.rest_api.root.add_resource(path_part=self.api_resource_path)
        method = resource.add_method(
            http_method="POST",
            integration=lambda_integration,
            authorizer=self.auth if self.auth != None else None,
            authorization_type=self.auth_type if self.auth_type != None else None,
        )
        return resource
