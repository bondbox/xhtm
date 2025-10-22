# coding:utf-8

import unittest

from xhtml.header.accept import AcceptLanguage
from xhtml.header.accept import LanguageQ
from xhtml.header.authorization import Authorization
from xhtml.header.cookie import Cookies
from xhtml.header.headers import HeaderMapping
from xhtml.header.headers import HeaderSequence
from xhtml.header.headers import Headers
from xhtml.header.headers import RequestLine
from xhtml.header.headers import StatusLine


class TestHeader(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_request_line(self):
        request_line = RequestLine("POST / HTTP/1.1")
        self.assertEqual(request_line.protocol, "HTTP/1.1")
        self.assertEqual(request_line.method, "POST")
        self.assertEqual(request_line.target, "/")

    def test_status_line(self):
        status_line = StatusLine("HTTP/1.1 200 OK")
        self.assertEqual(status_line.protocol, "HTTP/1.1")
        self.assertEqual(status_line.status_code, 200)
        self.assertEqual(status_line.status_text, "OK")

    def test_header_mapping(self):
        headers = HeaderMapping.parse([f"{Headers.ACCEPT.value}: text/html"])
        self.assertEqual(headers.get(Headers.ACCEPT.value), "text/html")
        self.assertEqual(headers.get(Headers.ACCEPT.http2), "text/html")
        self.assertEqual(len(headers), 1)

        for header in Headers:
            headers[header.value] = header.name

        self.assertEqual(len(headers), 56)

        for k, v in headers:
            self.assertIn(k, headers)
            self.assertEqual(headers[k], v)

    def test_header_sequence(self):
        headers = HeaderSequence.parse([f"{Headers.ACCEPT.value}: ACCEPT"])
        self.assertEqual(len(headers), 1)

        for header in Headers:
            headers.add(header.value, header.name)

        self.assertEqual(len(headers), 57)

        for k, v in headers:
            self.assertEqual(k.upper(), v.replace("_", "-"))


class TestAuthorization(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_basic(self):
        auth = Authorization.paser("Basic ZGVtbzp0ZXN0")
        self.assertIsInstance(auth, Authorization.Basic)
        self.assertEqual(auth.type, Authorization.Basic.TYPE)
        assert isinstance(auth, Authorization.Basic)
        self.assertEqual(auth.password, "test")
        self.assertEqual(auth.username, "demo")

    def test_bearer(self):
        auth = Authorization.paser("Bearer test")
        self.assertIsInstance(auth, Authorization.Bearer)
        self.assertEqual(auth.type, Authorization.Bearer.TYPE)
        assert isinstance(auth, Authorization.Bearer)
        self.assertEqual(auth.password, "test")
        self.assertEqual(auth.username, "")

    def test_api_key(self):
        auth = Authorization.paser("ApiKey test")
        self.assertIsInstance(auth, Authorization.APIKey)
        self.assertEqual(auth.type, Authorization.APIKey.TYPE)
        assert isinstance(auth, Authorization.APIKey)
        self.assertEqual(auth.password, "test")
        self.assertEqual(auth.username, "")


class TestCookies(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.cookies = Cookies("ID=5D43B5D:FG=1; Domain=example.com; Path=/; A= 1 ; B= 2; C=3 ")  # noqa:E501

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_len(self):
        self.assertEqual(len(self.cookies), 6)
        self.assertEqual(len(Cookies("")), 0)

    def test_iter(self):
        for cookie in self.cookies:
            self.assertIsInstance(cookie, str)
            self.assertIn(cookie, self.cookies)

    def test_get(self):
        self.assertEqual(self.cookies.get("ID"), "5D43B5D:FG=1")
        self.assertEqual(self.cookies["Domain"], "example.com")
        self.assertEqual(self.cookies["Path"], "/")
        self.assertEqual(self.cookies["A"], " 1 ")
        self.assertEqual(self.cookies["B"], " 2")
        self.assertEqual(self.cookies["C"], "3 ")
        self.assertEqual(self.cookies.get("Test"), "")


class TestLanguageQ(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.q: LanguageQ = LanguageQ("zh-CN,zh", 0.9)

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_str(self):
        self.assertEqual(str(self.q), "zh-CN,zh;q=0.9")

    def test_len(self):
        self.assertEqual(len(self.q), 2)


class TestAcceptLanguage(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.lang: AcceptLanguage = AcceptLanguage("zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6")  # noqa:E501

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_len_and_contains(self):
        self.assertEqual(len(self.lang), 5)
        self.assertNotIn("zh-TW", self.lang)
        self.assertNotIn("zh-HK", self.lang)
        self.assertIn("zh-CN", self.lang)
        self.assertIn("zh", self.lang)
        self.assertIn("en", self.lang)


if __name__ == "__main__":
    unittest.main()
