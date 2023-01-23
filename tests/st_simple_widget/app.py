#!/usr/bin/env python3

# The import statement at the top of the script is used
# during local development and will not cause any modules
# to be imported after conversion to HTML

import pandas as pd
import streamlit as st
from widgets.streamlit.widget import StreamlitWidget
from widgets.streamlit.resources.dataframe import StDataFrame
from widgets.streamlit.resources.value import StString
import plotly.express as px


# Give the widget a descriptive name
class SimpleWidget(StreamlitWidget):

    # This app will prompt the user to provide four inputs,
    # one DataFrame (which can be provided as CSV), and
    # three string values.

    resources = [
        StDataFrame(
            id="df",
            value=pd.DataFrame(dict(x=[], y=[], label=[])),
            label="Test CSV",
        ),
        StString(id="x_col", value="x", label="X-axis Column"),
        StString(id="y_col", value="y", label="Y-axis Column"),
        StString(id="label_col", value="label", label="Label Column")
    ]
    # The updated values for each of these resources can be accessed
    # and modified using the .get_value() and .set_value() functions
    # For example:
    #   self.get_value("x_col") -> "x"
    #   or
    #   self.set_value("x_col", "new_value")

    # Specify any packages which should be installed prior to loading

    requirements = [
        "widgets-lib",
        "pandas",
        "plotly"
    ]

    # Specify any inputs statements which are needed by the widget
    # beyond the following (which will be executed by default):
    #   import streamlit as st
    #   from widgets.streamlit.resources.dataframe import StDataFrame
    #   from widgets.streamlit.resources.value import String, Integer, Float
    #   from widgets.streamlit.widget import StreamlitWidget

    extra_imports = [
        "import pandas as pd",
        "import plotly.express as px"
    ]

    # The visualization defined in the viz function will be run and
    # updated every time a user changes the inputs, showing a simple
    # scatterplot.
    def viz(self):

        if st.session_state.df is not None or self.get_value("df").shape[0] > 0: # noqa

            fig = px.scatter(
                data_frame=self.get_value("df"),
                x=self.get_value("x_col"),
                y=self.get_value("y_col"),
                hover_name=self.get_value("label_col")
            )

            st.plotly_chart(fig)

        else:

            st.write("Please provide data to plot")

        self.download_html_button()
        self.download_script_button()
