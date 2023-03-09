from typing import Union
from widgets.base.resource import Resource


class SubResource(Resource):
    """
    Nested below Resource objects as children, a SubResource
    has the ability to .set an attribute on the first object
    above it which is not also a SubResource.
    """

    def set_top(self, attr="value", value=None):
        """
        Set the value of an attribute on the first object
        above this one in the chain of parents which is not
        also a SubResource object.
        """

        # If the parent object also has a set_top() method
        if getattr(self.parent, "set_top", None) is not None:

            # Invoke it
            self.parent.set_top(attr=attr, value=value)

        else:
            self.parent.set(path=[], attr=attr, value=value)
