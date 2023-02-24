import unittest
from widgets.base.widget import Widget


class NewWidget(Widget):
    """Define a new type of widget."""

    foo = "bar"

    def newfunction(self):
        print(self.foo)


class ImportedWidget(NewWidget):
    """This will be the class of the widget which is imported."""

    foo = "BAR"


class TestModule(unittest.TestCase):

    def test_parent_source(self):

        # Instantiate a widget from ImportedWidget
        w = ImportedWidget()

        # The source for ImportedWidget does contain itself
        self.assertTrue(
            "class ImportedWidget" in w.source_self(),
            w.source_self()
        )

        # The combined set of all sources also includes itself
        self.assertTrue(
            "class ImportedWidget" in w.source_all(),
            w.source_all()
        )

        # While the source for ImportedWidget does not contain its parent
        self.assertFalse("class NewWidget" in w.source_self(), w.source_self())

        # Its parent is found in the results of source_all()
        self.assertTrue("class NewWidget" in w.source_all(), w.source_all())


if __name__ == '__main__':
    unittest.main()
