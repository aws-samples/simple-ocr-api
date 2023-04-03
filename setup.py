import setuptools

setuptools.setup(
    name="simple_ocr_api",
    version="1.0.0",
    author="Laine Wishart",
    author_email="lwwishar@amazon.com",
    description="Application code and infrastructure to invoke Amazon Textract APIs via a custom API",
    packages=setuptools.find_packages(),
    install_requires=[
        f"cdk_lambda_layer_builder @ git+https://github.com/aws-samples/aws-cdk-lambda-layer-builder.git#egg=cdk_lambda_layer_builder",
        "aws-cdk-lib==2.31.1",
        "constructs==10.1.300",
        "boto3==1.24.4",
        "wheel",
    ],
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.7",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT No Attribution License (MIT-0)",
    ],
    python_requires=">=3.7",
)
