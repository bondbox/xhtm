# coding:utf-8

from pathlib import Path
from typing import Optional

from xkits_lib.unit import TimeUnit

from xhtml.resource import Resource

BASE_DIR: Path = Path(__file__).parent


class Template(Resource):
    FAVICON: str = "favicon.ico"

    def __init__(self, base: Optional[Path] = None, lifetime: TimeUnit = 0):
        super().__init__(base if base and base.is_dir() else BASE_DIR, lifetime)  # noqa:E501
