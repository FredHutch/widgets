#!/usr/bin/env python3

# The import statement at the top of the script is used
# during local development and will not cause any modules
# to be imported after conversion to HTML

import pandas as pd
import streamlit as st
import widgets.streamlit as wist
import plotly.express as px


# Give the widget a descriptive name
class SimpleWidget(wist.StreamlitWidget):

    # This app will prompt the user to provide a set of inputs,
    # one DataFrame (which can be provided as CSV), and
    # strings indicating which columns to plot.
    # The list of resources will be wrapped in an expand/collapse
    # element, which starts off as being expanded by default.

    children = [
        wist.StExpander(
            id='options_expander',
            label='Options',
            expanded=True,
            children=[
                wist.StDataFrame(
                    id="df",
                    value=pd.DataFrame(dict(x=[], y=[], label=[])),
                    label="Test CSV",
                ),
                wist.StSelectString(
                    id="x_col",
                    label="X-axis Column"
                ),
                wist.StString(
                    id="x_label",
                    label="X-axis Label",
                    value="x-axis"
                ),
                wist.StSelectString(
                    id="y_col",
                    label="Y-axis Column"
                ),
                wist.StString(
                    id="y_label",
                    label="Y-axis Label",
                    value="y-axis"
                )
            ]
        )
    ]
    # The updated values for each of these resources can be accessed
    # and modified using the .get() and .set() functions
    # For example:
    #   self.get(path=["x_col"]) -> "x"
    #   or
    #   self.set(path=["x_col"], "new_value")
    # Additionally, self.all_values() creates a dict with the values
    # for all of the resources.

    # The attributes of the resources can also be modified, using the
    # .set() and .get() functions.
    # For example, to update the options displayed for the x_col menu:
    #   self.set("x_col", "options", ["x", "y", "label"])

    # Specify any packages which should be installed prior to loading

    requirements = [
        "pandas",
        "plotly"
    ]

    # Specify any inputs statements which are needed by the widget
    # beyond the following (which will be executed by default):
    # import streamlit as st
    # from widgets.streamlit import *

    extra_imports = [
        "import pandas as pd",
        "import plotly.express as px"
    ]

    # The visualization defined in the viz function will be run and
    # updated every time a user changes the inputs, showing a simple
    # scatterplot.
    def run_self(self):

        # Get the updated DataFrame from the UI
        df = self.get(path=["options_expander", "df"])

        # If a table has been uploaded
        if df is not None and df.shape[0] > 0:

            # Update the options for the x_col, y_col, and label_col variables
            self.update_options(df.columns.values)

            # After making that update, get the complete set of values
            # It is a nuance of streamlit that this object will not be
            # updated appropriately if called before .update_options()
            vals = self.all_values(path=["options_expander"])

            # Make a plot
            fig = px.scatter(
                data_frame=df,
                x=vals["x_col"],
                y=vals["y_col"],
                hover_data=df.columns.values,
                labels={
                    vals["x_col"]: vals["x_label"],
                    vals["y_col"]: vals["y_label"]
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
        for resource_id in ["x_col", "y_col"]:

            # Update the options attribute of the resource
            self.set(
                path=["options_expander", resource_id],
                attr="options",
                value=list(options)
            )


if __name__ == "__main__":
    w = SimpleWidget()
    w.run()
