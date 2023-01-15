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
    # The data provided for each of these elements will be
    # available in the viz() scope using the self.data object

    resources = [
        StDataFrame(
            id="df",
            default=pd.DataFrame(dict(x=[], y=[], label=[])),
            label="Test CSV",
        ),
        StString(id="x_col", default="x", label="X-axis Column"),
        StString(id="y_col", default="y", label="Y-axis Column"),
        StString(id="label_col", default="label", label="Label Column")
    ]

    # Specify any packages which should be installed prior to loading

    requirements = [
        "widgets",
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

        if st.session_state.df is not None or self.data["df"].shape[0] > 0:

            fig = px.scatter(
                data_frame=self.data["df"],
                x=self.data["x_col"],
                y=self.data["y_col"],
                hover_name=self.data["label_col"]
            )

            st.plotly_chart(fig)

        else:

            st.write("Please provide data to plot")

        self.download_html_button()
        self.download_script_button()
