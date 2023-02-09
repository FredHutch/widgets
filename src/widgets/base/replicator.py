from widgets.base.resource_list import ResourceList
from widgets.base.resource import Resource


class Replicator(ResourceList):
    """
    Self-modifying list of Resources which is able to add new elements
    and rearrange the order of the existing elements.
    """

    def _new_id(self):
        """Return an id attribute which can be used for a new element."""

        i = 0
        while f"elem_{i}" in self._resource_dict:
            i += 1
        return f"elem_{i}"

    def new(self):
        """
        Return an instance of a new element.
        Should be overriden by instances of this class.
        """

        # By using the ._new_id() function we can ensure that the
        # id of the new resource will not conflict with any existing
        return Resource(id=self._new_id())

    def append(self):
        """Add a new element at the end of the list."""

        # Make the new element
        new_elem = self.new()

        # Add it to the resource list
        self.resources.append(new_elem)

        # Attach it to the self._resource_dict and assign the .parent attribute
        self._attach_resource(new_elem)

    def insert(self, ix: int):
        """Insert a new element at a specific index position."""

        # Make the new element
        new_elem = self.new()

        # Insert it within the resource list
        self.resources.insert(ix, new_elem)

        # Attach it to the self._resource_dict and assign the .parent attribute
        self._attach_resource(new_elem)

    def remove(self, ix: int):
        """Remove an element from a specific index position."""

        # Remove the element from the list
        removed_elem = self.resources.pop(ix)

        # Delete the key from the _resource_dict
        del self._resource_dict[removed_elem.id]
