import setuptools

setuptools.setup(
    name="ocrtools",
    version="1.0.0",
    author="Laine Wishart",
    author_email="lwwishar@amazon.com",
    description="A collection of helper functions and classes for OCR",
    packages=setuptools.find_packages(),
    install_requires=[
        "amazon_textract_prettyprinter==0.0.13",
        "amazon-textract-response-parser==0.1.30",
        "boto3==1.24.4",
        "botocore==1.27.17",
        "fastapi==0.78.0",
        "mangum==0.17.0",
        "Pillow==10.0.0",
        "pydantic==1.10.4",
        "pytest==7.1.2",
        "setuptools==65.6.3",
        "uvicorn==0.20.0",
    ],  # checks if libs are installed, and installs if not
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT No Attribution License (MIT-0)",
    ],
    python_requires=">=3.7",
)
