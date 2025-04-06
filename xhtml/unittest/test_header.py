# coding:utf-8

import unittest

from xhtml.header.accept import AcceptLanguage
from xhtml.header.accept import LanguageQ
from xhtml.header.headers import Cookies


class TestCookies(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.cookies = Cookies("ID=5D43B5D:FG=1; Domain=example.com; Path=/")

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_len(self):
        self.assertEqual(len(self.cookies), 3)

    def test_iter(self):
        for cookie in self.cookies:
            self.assertIsInstance(cookie, str)
            self.assertIn(cookie, self.cookies)

    def test_get(self):
        self.assertEqual(self.cookies.get("ID"), "5D43B5D:FG=1")
        self.assertEqual(self.cookies["Domain"], "example.com")
        self.assertEqual(self.cookies["Path"], "/")
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
