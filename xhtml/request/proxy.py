# coding:utf-8

from typing import Dict
from typing import MutableMapping
from typing import Optional
from urllib.parse import urljoin

from requests import get
from requests import post

from xhtml.request.stream import StreamResponse


class ProxyError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class MethodNotAllowed(ProxyError):
    def __init__(self) -> None:
        super().__init__("Method Not Allowed")


class RequestProxy():
    """API Request Proxy"""

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
        self.__target: str = target

    @property
    def target(self) -> str:
        return self.__target

    def urljoin(self, path: str) -> str:
        return urljoin(base=self.target, url=path)

    @classmethod
    def filter_headers(cls, headers: MutableMapping[str, str]) -> Dict[str, str]:  # noqa:E501
        return {k: v for k, v in headers.items() if k.lower() not in cls.EXCLUDED_REQUEST_HEADERS}  # noqa:E501

    def request(self, path: str, method: str, data: Optional[bytes] = None,
                headers: Optional[MutableMapping[str, str]] = None
                ) -> StreamResponse:
        target_url: str = self.urljoin(path.lstrip("/"))
        if method == "GET":
            response = get(
                url=target_url,
                data=data,
                headers=headers,
                stream=True
            )
            return StreamResponse(response)
        if method == "POST":
            response = post(
                url=target_url,
                data=data,
                headers=headers,
                stream=True
            )
            return StreamResponse(response)
        raise MethodNotAllowed()
