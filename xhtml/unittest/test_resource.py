# coding:utf-8

from pathlib import Path
from unittest import TestCase
from unittest import main
from unittest import mock

from xhtml import resource


class TestFileResource(TestCase):

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

    def test_file_not_found(self):
        self.assertRaises(FileNotFoundError, resource.FileResource, "test.txt")

    @mock.patch.object(resource.Path, "open")
    @mock.patch.object(resource.Path, "is_file")
    def test_render(self, mock_is_file, mock_open):
        mock_is_file.side_effect = [True]
        with mock.mock_open(mock_open, read_data=b""):
            self.assertEqual(resource.FileResource(Path("test.html")).render(), "")  # noqa:E501


class TestResource(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.res: resource.Resource = resource.Resource()

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_find(self):
        self.assertIsInstance(self.res.find(resource.Resource.FAVICON), resource.FileResource)  # noqa:E501
        with mock.patch.object(getattr(self.res, "_Resource__cache"), "get") as mock_get:  # noqa:E501
            mock_get.side_effect = [resource.CacheMiss("test")]
            self.assertIsInstance(self.res.find(resource.Resource.FAVICON), resource.FileResource)  # noqa:E501
        self.assertIsNone(self.res.find("test.txt"))

    def test_favicon(self):
        self.assertIsInstance(self.res.favicon.loadb(), bytes)

    def test_favicon_ext(self):
        self.assertEqual(self.res.favicon.ext, ".ico")

    def test_seek(self):
        self.assertIsInstance(self.res.seek("logo.svg").loads(), str)

    def test_seek_file_not_found(self):
        self.assertRaises(FileNotFoundError, self.res.seek, "test.txt")


if __name__ == "__main__":
    main()
