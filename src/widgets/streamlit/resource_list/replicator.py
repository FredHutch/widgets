import streamlit as st
from streamlit.delta_generator import DeltaGenerator
from widgets.streamlit import StResourceList
from widgets.base.replicator import Replicator


class StReplicator(StResourceList, Replicator):
    """
    Self-modifying list of Resources which is able to add new elements
    and rearrange the order of the existing elements.
    """

    def append_button(
        self,
        container: DeltaGenerator = None,
        label="Add"
    ) -> None:
        """Render a button to add a new element at the end of the list."""

        if container is None:

            container = st.container()

        container.button(
            label=label,
            help="Add a new element to the end of the list",
            on_click=self.append
        )

    def insert_button(
        self, ix: int,
        container: DeltaGenerator = None,
        label="Insert"
    ):
        """
        Render a button to insert a new element at a specific index position.
        """

        if container is None:

            container = st.container()

        container.button(
            label=label,
            help="Insert a new element into the list",
            on_click=self.insert,
            args=[ix]
        )

    def remove_button(
        self,
        ix: int,
        container: DeltaGenerator = None,
        label="Remove"
    ):
        """
        Render a button to remove an element from a specific index position.
        """

        if container is None:

            container = st.container()

        container.button(
            label=label,
            help="Insert a new element into the list",
            on_click=self.remove,
            args=[ix]
        )
