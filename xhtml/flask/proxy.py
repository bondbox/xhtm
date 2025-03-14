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
        return Response(stream_with_context(sr.generator), sr.response.status_code, headers)  # noqa:E501

    def request(self, request: Request) -> Response:
        try:
            target_url: str = self.urljoin(request.path.lstrip("/"))
            if request.method == "GET":
                return self.forward(StreamResponse(requests.get(target_url, headers=request.headers, stream=True)))  # noqa:E501
            elif request.method == "POST":
                return self.forward(StreamResponse(requests.post(target_url, headers=request.headers, data=request.data, stream=True)))  # noqa:E501
            return Response("Method Not Allowed", status=405)
        except requests.ConnectionError:
            return Response("Bad Gateway", status=502)
