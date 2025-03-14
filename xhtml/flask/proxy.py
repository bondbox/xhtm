# coding:utf-8

from urllib.parse import urljoin

from flask import Request
from flask import Response
from flask import stream_with_context
import requests

from xhtml.request import StreamResponse


class FlaskProxy():
    EXCLUDED_HEADERS = ["content-encoding", "content-length", "transfer-encoding", "connection"]  # noqa:E501

    def __init__(self, target: str) -> None:  # noqa:E501
        self.__target: str = target

    @property
    def target(self) -> str:
        return self.__target

    def urljoin(self, path: str) -> str:
        return urljoin(base=self.target, url=path)

    @classmethod
    def forward(cls, sr: StreamResponse) -> Response:
        headers = [(k, v) for k, v in sr.response.raw.headers.items() if k.lower() not in cls.EXCLUDED_HEADERS]  # noqa:E501
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
            target_url: str = self.urljoin(request.path.lstrip("/"))
            if request.method == "GET":
                response = requests.get(
                    url=target_url,
                    headers=request.headers,
                    cookies=request.cookies,
                    stream=True
                )
                return self.forward(StreamResponse(response))
            elif request.method == "POST":
                response = requests.post(
                    url=target_url,
                    data=request.data,
                    headers=request.headers,
                    cookies=request.cookies,
                    stream=True
                )
                return self.forward(StreamResponse(response))
            return Response("Method Not Allowed", status=405)
        except requests.ConnectionError:
            return Response("Bad Gateway", status=502)
