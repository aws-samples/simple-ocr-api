class AWSAuthFailed(Exception):
    """Raises if AWS credentials are unavailable.

    """

    def __init__(self, message="AWS authentication failed."):
        self.message = message
        super().__init__(self.message)


class NotaPDF(Exception):
    """Raises if the input document was specified as a PDF but it is not a PDF.

    """

    def __init__(self, message="The file provided was specified as a PDF, but it is not a PDF."):
        self.message = message
        super().__init__(self.message)


class IncompleteDocumentStream(Exception):
    """Raises if the input base64 stream is incomplete.

    """

    def __init__(self, message="The document stream provided is incomplete."):
        self.message = message
        super().__init__(self.message)
