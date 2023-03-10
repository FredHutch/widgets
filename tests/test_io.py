import unittest
from widgets.base.io import _load_module, load_widget
from widgets.base.exceptions import IOException, WidgetInitializationException
from widgets.base.widget import Widget
import widgets.streamlit as wist


class TestIO(unittest.TestCase):

    def test_load_widget(self):

        # Load the test widget
        w = load_widget("tests/assets/app.py", "SimpleWidget")
        self.assertIsInstance(w(), Widget)

        # Trying to load a non-existant module raises an error
        self.assertRaises(
            IOException,
            lambda: load_widget("tests/assets/app.py", 'FooBar')
        )

        # Trying to load a broken module raises an error
        self.assertRaises(
            WidgetInitializationException,
            lambda: load_widget("tests/assets/app.py", 'SimpleWidgetNoBase')
        )

    def test_load_module(self):

        # Trying to load a non-existant file raises an error
        self.assertRaises(
            IOException,
            lambda: _load_module('foo/bar.py')
        )

    def test_load_streamlit_widget(self):

        # Load the test streamlit widget
        w = load_widget("tests/assets/app.py", "SimpleStWidget")
        self.assertIsInstance(w(), wist.StreamlitWidget)

    def test_load_widget_errors(self):

        self.assertRaises(
            IOException,
            lambda: load_widget("tests/assets/wrong_path.py", "SimpleWidget")
        )

        self.assertRaises(
            IOException,
            lambda: load_widget("tests/assets/app.py", "WrongName")
        )

        self.assertRaises(
            WidgetInitializationException,
            lambda: load_widget("tests/assets/app.py", "SimpleWidgetNoBase")
        )


if __name__ == '__main__':
    unittest.main()
