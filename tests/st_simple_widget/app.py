import pandas as pd
import streamlit as st
from widgets.streamlit.widget import StreamlitWidget
from widgets.streamlit.resources.dataframe import DataFrame
from widgets.streamlit.resources.value import String, Float, Integer
import plotly.express as px


class SimpleWidget(StreamlitWidget):

    resources = [
        DataFrame(
            id="df",
            default=pd.DataFrame(dict(x=[], y=[], label=[])),
            label="Test CSV",
        ),
        String(id="x_col", default="x", label="X-axis Column"),
        String(id="y_col", default="y", label="Y-axis Column"),
        String(id="label_col", default="label", label="Label Column")
    ]

    def viz(self):

        if st.session_state.df is not None and self.data["df"].shape[0] > 0:

            fig = px.scatter(
                data_frame=self.data["df"],
                x=self.data["x_col"],
                y=self.data["y_col"],
                hover_name=self.data["label_col"]
            )

            st.plotly_chart(fig)

        else:

            st.write("Please provide data to plot")


if __name__ == "__main__":

    widget = SimpleWidget()

    widget.run()