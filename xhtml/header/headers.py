# coding:utf-8

from enum import Enum
from typing import Dict
from typing import Iterator


class Headers(Enum):
    """HTTP headers

    Reference:
        https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers
    """
    ACCEPT = "Accept"
    ACCEPT_ENCODING = "Accept-Encoding"
    ACCEPT_LANGUAGE = "Accept-Language"
    ACCEPT_RANGES = "Accept-Ranges"
    ACCESS_CONTROL_ALLOW_CREDENTIALS = "Access-Control-Allow-Credentials"
    ACCESS_CONTROL_ALLOW_HEADERS = "Access-Control-Allow-Headers"
    ACCESS_CONTROL_ALLOW_METHODS = "Access-Control-Allow-Methods"
    ACCESS_CONTROL_ALLOW_ORIGIN = "Access-Control-Allow-Origin"
    ACCESS_CONTROL_EXPOSE_HEADERS = "Access-Control-Expose-Headers"
    ACCESS_CONTROL_MAX_AGE = "Access-Control-Max-Age"
    ACCESS_CONTROL_REQUEST_HEADERS = "Access-Control-Request-Headers"
    ACCESS_CONTROL_REQUEST_METHOD = "Access-Control-Request-Method"
    AGE = "Age"
    ALLOW = "Allow"
    AUTHORIZATION = "Authorization"
    CACHE_CONTROL = "Cache-Control"
    CONNECTION = "Connection"
    CONTENT_DISPOSITION = "Content-Disposition"
    CONTENT_ENCODING = "Content-Encoding"
    CONTENT_LANGUAGE = "Content-Language"
    CONTENT_LENGTH = "Content-Length"
    CONTENT_LOCATION = "Content-Location"
    CONTENT_RANGE = "Content-Range"
    CONTENT_TYPE = "Content-Type"
    COOKIE = "Cookie"
    DATE = "Date"
    ETAG = "ETag"
    EXPIRES = "Expires"
    FROM = "From"
    HOST = "Host"
    IF_MATCH = "If-Match"
    IF_MODIFIED_SINCE = "If-Modified-Since"
    IF_NONE_MATCH = "If-None-Match"
    IF_RANGE = "If-Range"
    IF_UNMODIFIED_SINCE = "If-Unmodified-Since"
    KEEP_ALIVE = "Keep-Alive"
    LAST_MODIFIED = "Last-Modified"
    LOCATION = "Location"
    MAX_FORWARDS = "Max-Forwards"
    ORIGIN = "Origin"
    PRAGMA = "Pragma"
    PROXY_AUTHENTICATE = "Proxy-Authenticate"
    PROXY_AUTHORIZATION = "Proxy-Authorization"
    RANGE = "Range"
    REFERER = "Referer"
    RETRY_AFTER = "Retry-After"
    SERVER = "Server"
    SET_COOKIE = "Set-Cookie"
    TE = "TE"
    TRAILER = "Trailer"
    TRANSFER_ENCODING = "Transfer-Encoding"
    UPGRADE = "Upgrade"
    USER_AGENT = "User-Agent"
    VARY = "Vary"
    VIA = "Via"
    WARNING = "Warning"


class Cookies():
    def __init__(self, *cookies: str):
        self.__cookies: Dict[str, str] = {}
        for item in cookies:
            for cookie in item.split(";"):
                k, v = cookie.split("=", maxsplit=1)
                self.__cookies[k.strip()] = v.strip()

    def __len__(self) -> int:
        return len(self.__cookies)

    def __iter__(self) -> Iterator[str]:
        return iter(self.__cookies)

    def __getitem__(self, key: str) -> str:
        return self.__cookies[key]

    def __contains__(self, key: str) -> bool:
        return key in self.__cookies

    def get(self, key: str, default: str = "") -> str:
        return self.__cookies.get(key, default)
