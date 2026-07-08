# coding:utf-8

from os.path import join
from pathlib import Path
from typing import Optional

from jinja2 import Environment
from xkits_lib.cache import CacheMiss
from xkits_lib.cache import CachePool
from xkits_lib.unit import TimeUnit

BASE_DIR: Path = Path(__file__).parent


class FileResource():

    def __init__(self, path: Path):
        if not isinstance(path, Path) or not path.is_file():
            message = f"No such file: {path}"
            raise FileNotFoundError(message)
        self.__data: Optional[bytes] = None
        self.__path: Path = path

    @property
    def ext(self) -> str:
        return self.path.suffix

    @property
    def path(self) -> Path:
        return self.__path

    def loadb(self) -> bytes:
        if self.__data is None:
            with self.path.open("rb") as rhdl:
                self.__data = rhdl.read()
        return self.__data

    def loads(self, encoding: str = "utf-8") -> str:
        return self.loadb().decode(encoding=encoding)

    def render(self, **context: str) -> str:
        """render html template"""
        return Environment().from_string(self.loads()).render(**context)


class Resource():
    FAVICON: str = "favicon.ico"

    def __init__(self, base: Optional[Path] = None, lifetime: TimeUnit = 0):
        self.__cache: CachePool[str, FileResource] = CachePool(lifetime)
        self.__base: Path = base if base and base.is_dir() else BASE_DIR

    @property
    def base(self) -> Path:
        return self.__base

    @property
    def favicon(self) -> FileResource:
        return self.seek(self.FAVICON)

    def find(self, *args: str) -> Optional[FileResource]:
        def check(base: Path, real: str) -> Optional[Path]:
            return path if (path := base / real).is_file() else check(BASE_DIR, real) if base != BASE_DIR else None  # noqa:E501

        if (real := join(*args)) in self.__cache:
            try:
                return self.__cache.get(real)
            except CacheMiss:
                pass

        resource: Optional[FileResource] = None
        if isinstance(path := check(self.base, real), Path):
            resource = FileResource(path)
            self.__cache.put(real, resource)
        return resource

    def seek(self, *args: str) -> FileResource:
        if not isinstance(resource := self.find(*args), FileResource):
            raise FileNotFoundError(f"No such file: {join(*args)}")
        return resource
