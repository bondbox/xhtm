# coding:utf-8

from typing import Dict
from urllib.parse import urljoin

from flask import Request
from flask import Response
from flask import stream_with_context
from requests import ConnectionError
from requests import Session

from xhtml.request import StreamResponse


class FlaskProxy():

    EXCLUDED_REQUEST_HEADERS = [
        "connection",
        "content-length",
        "host",
        "keep-alive",
        "proxy-authorization",
        "transfer-encoding",
        "via",
    ]

    EXCLUDED_RESPONSE_HEADERS = [
        "connection",
        "content-encoding",
        "content-length",
        "transfer-encoding",
    ]

    def __init__(self, target: str) -> None:
        # self.__session: Session = Session()
        self.__target: str = target

    @property
    def session(self) -> Session:
        return Session()

    @property
    def target(self) -> str:
        return self.__target

    def urljoin(self, path: str) -> str:
        return urljoin(base=self.target, url=path)

    @classmethod
    def headers(cls, request: Request) -> Dict[str, str]:
        return {k: v for k, v in request.headers.items() if k.lower() not in cls.EXCLUDED_REQUEST_HEADERS}  # noqa:E501

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
            target_url: str = self.urljoin(request.path.lstrip("/"))
            if request.method == "GET":
                response = self.session.get(
                    url=target_url,
                    data=request.data,
                    headers=self.headers(request),
                    cookies=request.cookies,
                    stream=True
                )
                return self.forward(StreamResponse(response))
            elif request.method == "POST":
                response = self.session.post(
                    url=target_url,
                    data=request.data,
                    headers=self.headers(request),
                    cookies=request.cookies,
                    stream=True
                )
                return self.forward(StreamResponse(response))
            return Response("Method Not Allowed", status=405)
        except ConnectionError:
            return Response("Bad Gateway", status=502)
