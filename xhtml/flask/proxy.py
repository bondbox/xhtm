# coding:utf-8

from flask import Request
from flask import Response
from flask import stream_with_context
from requests import ConnectionError

from xhtml.request import MethodNotAllowed
from xhtml.request import RequestProxy
from xhtml.request import StreamResponse


class FlaskProxy(RequestProxy):

    def __init__(self, target: str) -> None:
        super().__init__(target)

    @classmethod
    def forward(cls, sr: StreamResponse) -> Response:
        headers = [(k, v) for k, v in sr.response.raw.headers.items() if k.lower() not in cls.EXCLUDED_RESPONSE_HEADERS]  # noqa:E501
        response = Response(stream_with_context(sr.generator), sr.response.status_code, headers)  # noqa:E501
        for cookie in sr.response.cookies:
            response.set_cookie(
                key=cookie.name,
                value=cookie.value or "",
                expires=cookie.expires,
                path=cookie.path,
                domain=cookie.domain,
                secure=cookie.secure
            )
        return response

    def request(self, request: Request) -> Response:
        try:
            headers = self.filter_headers({k: v for k, v in request.headers.items()})  # noqa:E501
            response = super().request(path=request.path,
                                       method=request.method,
                                       data=request.data,
                                       headers=headers,
                                       cookies=request.cookies)
            return self.forward(response)
        except MethodNotAllowed:
            return Response("Method Not Allowed", status=405)
        except ConnectionError:
            return Response("Bad Gateway", status=502)
