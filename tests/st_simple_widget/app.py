#!/usr/bin/env python3

# The import statement at the top of the script is used
# during local development and will not cause any modules
# to be imported after conversion to HTML

import pandas as pd
import streamlit as st
from widgets.streamlit.widget import StreamlitWidget
from widgets.streamlit.resources.dataframe import StDataFrame
from widgets.streamlit.resources.value import StSelectString
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
        StSelectString(id="x_col", label="X-axis Column"),
        StString(id="x_label", label="X-axis Label", value="x-axis"),
        StSelectString(id="y_col", label="Y-axis Column"),
        StString(id="y_label", label="Y-axis Label", value="y-axis"),
        StSelectString(id="label_col", label="Label Column")
    ]
    # The updated values for each of these resources can be accessed
    # and modified using the .get_value() and .set_value() functions
    # For example:
    #   self.get_value("x_col") -> "x"
    #   or
    #   self.set_value("x_col", "new_value")

    # The attributes of the resources can also be modified, using the
    # .set() and .get() functions.
    # For example, to update the options displayed for the x_col menu:
    #   self.set("x_col", "options", ["x", "y", "label"])

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

        # Get the updated values from the UI
        df = self.get_value("df")

        # If a table has been uploaded
        if df is not None and df.shape[0] > 0:

            # Update the options for the x_col, y_col, and label_col variables
            self.update_options(df.columns.values)

            # Make a plot
            fig = px.scatter(
                data_frame=df,
                x=self.get_value("x_col"),
                y=self.get_value("y_col"),
                hover_name=self.get_value("label_col"),
                labels={
                    self.get_value("x_col"): self.get_value("x_label"),
                    self.get_value("y_col"): self.get_value("y_label")
                }
            )

            # Display the plot
            st.plotly_chart(fig)

        # If no table has been uploaded
        else:

            # Print a simple message to the user
            st.write("Please provide data to plot")

        self.download_html_button()
        self.download_script_button()

    # Custom methods can be defined for the widget
    def update_options(self, options):
        """Update the options displayed for each of the column menus."""

        # For each of the resources
        for resource_id in ["x_col", "y_col", "label_col"]:

            # Update the options attribute of the resource
            self.set(resource_id, "options", list(options))


if __name__ == "__main__":
    w = SimpleWidget()
    w.run()
