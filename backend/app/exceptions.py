class ServiceError(Exception):
    status_code = 500

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class InvalidVideoError(ServiceError):
    status_code = 400


class VideoNotFoundError(ServiceError):
    status_code = 404


class TranscriptUnavailableError(ServiceError):
    status_code = 422


class ExternalServiceError(ServiceError):
    status_code = 503


class ConfigurationError(ServiceError):
    status_code = 503
