# -*- coding: utf-8 -*-
import traceback
import collections.abc
from odoo.tools import ustr
from odoo.http import JsonRPCDispatcher
from werkzeug.exceptions import NotFound

def serialize_exception(exception):
    name = type(exception).__name__
    module = type(exception).__module__

    return {
        'name': f'{module}.{name}' if module else name,
        'debug': traceback.format_exc(),
        'message': ustr(exception),
        'arguments': exception.args,
        'context': getattr(exception, 'context', {}),
    }

class SessionExpiredException(Exception):
    pass

class JsonRPCDispatcherRebrand(JsonRPCDispatcher):

    def handle_error(self, exc: Exception) -> collections.abc.Callable:
        """
        Handle any exception that occurred while dispatching a request to
        a `type='json'` route. Also handle exceptions that occurred when
        no route matched the request path, that no fallback page could
        be delivered and that the request ``Content-Type`` was json.

        :param exc: the exception that occurred.
        :returns: a WSGI application
        """
        error = {
            'code': 200,  # this code is the JSON-RPC level code, it is
                          # distinct from the HTTP status code. This
                          # code is ignored and the value 200 (while
                          # misleading) is totally arbitrary.
            'message': "SGEEDE ERP Server Error",
            'data': serialize_exception(exc),
        }
        if isinstance(exc, NotFound):
            error['code'] = 404
            error['message'] = "404: Not Found"
        elif isinstance(exc, SessionExpiredException):
            error['code'] = 100
            error['message'] = "SGEEDE ERP Session Expired"

        return self._response(error=error)