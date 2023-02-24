#!/usr/bin/env python3

from widgets.base.resource import Resource
import widgets.streamlit as wist


class NewResource(Resource):
    foo = "bar"


class NewNewResource(NewResource):
    foo = "BAR"


class NewWidget(wist.StreamlitWidget):

    children = [
        NewResource(id='new'),
        NewNewResource(id='newnew'),
    ]


r = NewNewResource()

print(r.source_all())

w = NewWidget()

print(w._render_script())
