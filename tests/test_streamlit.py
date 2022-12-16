import os
import pandas as pd
import unittest
from widgets.streamlit.resources.dataframe import DataFrame
from widgets.streamlit.resources.value import String, Integer, Float


class TmpFile:
    def __init__(self, fn, value=None):
        self.fn = fn
        if value is not None:
            with open(fn, "w") as handle:
                handle.write(str(value))

    def __enter__(self) -> str:
        return self.fn

    def __exit__(self, exc_type, exc_value, exc_tb):
        # Delete the file
        os.remove(self.fn)


class TestStreamlit(unittest.TestCase):

    def test_dataframe(self):

        df_default = pd.DataFrame(dict(a=[1, 2, 3], b=['a', 'b', 'c']))

        df = DataFrame(
            id="test_dataframe",
            default=df_default
        )

        # Check the default value
        self.assertTrue(df_default.equals(df.load()), "Default DataFrame does not match")

        # Save a different value
        df_saved = pd.DataFrame(dict(a=[1, 2, 3], b=['x', 'y', 'z']))
        with TmpFile("test_dataframe.csv.gz") as fn:

            # Save to the path expected by the resoruce
            df_saved.to_csv(fn, index=None)

            # Check the saved value
            self.assertTrue(df_saved.equals(df.load()), "Saved DataFrame does not match")

    def test_string(self):

        s = String(
            id="test_string",
            default="default"
        )

        # Check the default value
        self.assertEqual(s.load(), "default", "Default string does not match")

        # Save a different value
        with TmpFile("test_string.txt", "saved") as fn:

            # Check the saved value
            self.assertEqual(s.load(), "saved", "Saved string does not match")

    def test_integer(self):

        s = Integer(
            id="test_integer",
            default=0
        )

        # Check the default value
        self.assertEqual(s.load(), 0, "Default integer does not match")

        # Save a different value
        with TmpFile("test_integer.txt", 1) as fn:

            # Check the saved value
            self.assertEqual(s.load(), 1, "Saved integer does not match")

    def test_float(self):

        s = Float(
            id="test_float",
            default=0.0
        )

        # Check the default value
        self.assertEqual(s.load(), 0.0, "Default float does not match")

        # Save a different value
        with TmpFile("test_float.txt", 1.1) as fn:

            # Check the saved value
            self.assertEqual(s.load(), 1.1, "Saved float does not match")


if __name__ == '__main__':
    unittest.main()