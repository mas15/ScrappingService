import json

from nameko.exceptions import safe_for_serialization
from nameko.web.handlers import HttpRequestHandler
from werkzeug.wrappers import Response


class HttpError(Exception):
    error_code = 'BAD_REQUEST'
    status_code = 400


class NotFoundError(HttpError):
    error_code = 'NOT_FOUND'
    status_code = 404


class ConflictError(HttpError):
    status_code = 409


class HttpEntrypoint(HttpRequestHandler):
    def response_from_exception(self, exc):
        if isinstance(exc, HttpError):
            response = Response(
                json.dumps({
                    'error': exc.error_code,
                    'message': safe_for_serialization(exc),
                }),
                status=exc.status_code,
                mimetype='application/json'
            )
            return response
        return HttpRequestHandler.response_from_exception(self, exc)


http = HttpEntrypoint.decorator
