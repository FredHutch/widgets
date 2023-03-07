import unittest
from widgets.base.exceptions import ResourceConfigurationException
import widgets.streamlit as wist


class ExampleDuplicator(wist.StDuplicator):
    pass


class TestDuplicator(unittest.TestCase):

    def test_duplicator_init(self):

        # Cannot instantiate without defining children
        self.assertRaises(
            ResourceConfigurationException,
            lambda: wist.StDuplicator()
        )

        # Cannot instantiate with non-list children
        self.assertRaises(
            ResourceConfigurationException,
            lambda: wist.StDuplicator(children="foobar")
        )

        # Cannot instantiate with non-list value
        self.assertRaises(
            ResourceConfigurationException,
            lambda: wist.StDuplicator(value="foobar")
        )

        # No errors when children are defined
        try:
            ExampleDuplicator(children=[wist.StString(id='string')])
        except Exception as e:
            self.fail(
                f"Could not instantiate Duplicator: {str(e)}"
            )

        # No errors when children and value are defined
        try:
            ExampleDuplicator(
                children=[wist.StString(id='string')],
                value=[True]
            )
        except Exception as e:
            self.fail(
                f"Could not instantiate Duplicator: {str(e)}"
            )

        # No errors when children and button lists are defined
        try:
            ExampleDuplicator(
                children=[
                    wist.StString(id='string1'),
                    wist.StString(id='string2')
                ],
                end_button=[False, True],
                middle_button=[True, False],
                hide_button=[False, False]
            )
        except Exception as e:
            self.fail(
                f"Could not instantiate Duplicator: {str(e)}"
            )

        # No errors when a base type is defined
        try:
            ExampleDuplicator(init_class=wist.StString, init_n=10)
        except Exception as e:
            self.fail(
                f"Could not instantiate Duplicator: {str(e)}"
            )

        # Cannot instantiate with non-callable element
        self.assertRaises(
            ResourceConfigurationException,
            lambda: wist.StDuplicator(init_class="foobar", init_n=10)
        )

        # Cannot instantiate with non-list end_button
        self.assertRaises(
            ResourceConfigurationException,
            lambda: wist.StDuplicator(init_class=wist.StString, init_n=10, end_button="foobar") # noqa
        )

        # Cannot instantiate with non-bool end_button
        self.assertRaises(
            ResourceConfigurationException,
            lambda: wist.StDuplicator(init_class=wist.StString, init_n=10, end_button=["foobar"]) # noqa
        )

    def test_duplicator_ix_funcs(self):

        r = wist.StDuplicator(
            init_class=wist.StString,
            init_n=10
        )

        r.value[1] = True
        r.value[3] = True

        self.assertTrue(
            r._final_ix() == 3
        )

        self.assertTrue(
            r._is_end(4)
        )

        self.assertTrue(
            r._is_middle(2)
        )


if __name__ == '__main__':
    unittest.main()
