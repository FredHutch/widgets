import unittest
from widgets.base.resource import Resource
from widgets.base.subresource import SubResource


class TestSubResource(unittest.TestCase):

    def test_set_top(self):

        r = Resource(
            id='main',
            value='foo',
            children=[
                SubResource(
                    id='first_sub',
                    children=[
                        SubResource(
                            id='second_sub'
                        )
                    ]
                )
            ]
        )

        self.assertEqual(r.get_value(), 'foo')

        r._get_child('first_sub', 'second_sub').set_top(value='FOO')

        self.assertEqual(r.get_value(), 'FOO')

        r._get_child('first_sub').set_top(value='bar')

        self.assertEqual(r.get_value(), 'bar')


if __name__ == '__main__':
    unittest.main()
