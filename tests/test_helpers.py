import unittest
from widgets.base.helpers import decompress_string
from widgets.base.helpers import compress_string


class TestHelpers(unittest.TestCase):

    def test_string_compression(self):

        orig = "This is a string to compress"

        comp = compress_string(orig)

        self.assertIsInstance(comp, str)

        self.assertNotEqual(orig, comp, f"{orig} == {comp}")

    def test_string_decompression(self):

        orig = "This is a string to compress"

        comp = compress_string(orig)

        decomp = decompress_string(comp)

        self.assertEqual(orig, decomp, f"{orig} != {decomp}")


if __name__ == '__main__':
    unittest.main()
