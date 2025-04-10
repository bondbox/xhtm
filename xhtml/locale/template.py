# coding:utf-8

from os.path import join

from xlc.language.message import Message
from xlc.language.segment import Section

from xhtml.header.accept import AcceptLanguage
from xhtml.template import Template


class LocaleTemplate(Template):
    def __init__(self, base: str):
        self.__message: Message = Message(join(base, "locale"))
        super().__init__(base)

    def search(self, accept_language: str, section: str) -> Section:
        language: AcceptLanguage = AcceptLanguage(accept_language)
        return language.choice(self.__message).seek(section)
