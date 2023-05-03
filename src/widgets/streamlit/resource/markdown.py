from widgets.st_base.resource import StResource


class StMarkdown(StResource):
    """Simple markdown display"""

    value = ""
    sidebar = False

    def __init__(
        self,
        id="markdown",
        value="",
        sidebar=False,
        disable_sidebar=False,
    ) -> None:
        """
        Set up the attributes which are used by all Resource objects.
        """

        super().__init__(
            id=id,
            value=value,
            children=[],
            sidebar=sidebar,
            disable_sidebar=disable_sidebar
        )

    def run_self(self):

        self._get_ui_element(
            sidebar=self.sidebar,
            empty=True
        ).markdown(
            self.value
        )
