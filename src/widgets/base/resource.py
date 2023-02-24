from inspect import getmro, getsource, isfunction, signature
from typing import Any, Dict, List, Union
from widgets.base.exceptions import ResourceConfigurationException
from widgets.base.exceptions import ResourceExecutionException
from widgets.base.exceptions import CLIExecutionException
from widgets.base.helpers import render_template


class Resource:
    """
    Base class for all Resources used by Widgets.

    Attributes:
            id (str):          The unique key used to identify the resource.
            value:             The starting value for the resource.
            label (str):       Label displayed to the user for the resource.
            children (list):   Any child Resource objects nested within this.
            parent (Resource): Parent Resource object this is nested within.
            help (str):        Help text describing the resource to the user.
    """

    id = ""
    value = None
    label = ""
    help = ""
    parent: Union['Resource', None] = None
    children: List['Resource'] = list()
    _children_dict: Dict[str, 'Resource'] = dict()
    # Quick way to check if the object is a Resource
    _is_resource = True

    ##################
    # INITIALIZATION #
    ##################
    def __init__(
        self,
        id="resource",
        value=None,
        children: List['Resource'] = [],
        label="",
        help="",
        **kwargs
    ) -> None:
        """
        Set up the attributes which are used by all Resource objects.
        """

        # The 'id' cannot be empty
        if len(id) == 0:
            msg = "Must provide id for Resource"
            raise ResourceConfigurationException(msg)

        # Save the id and starting value for this particular resource
        self.id = id
        self.value = value

        # If no label is provided, default to the id
        self.label = id.title() if label == "" else label
        self.help = help

        # Any additional keyword arguments
        for attr, val in kwargs.items():

            # Will be attached to this object
            self.__dict__[attr] = val

        # Attach the children
        self._attach_children(children)

    def _attach_children(self, children):
        """Attach all provided children to the Resource"""

        # The _resource_dict must be empty at initialization
        self._children_dict = dict()

        # If children were provided
        if len(children) > 0:

            # Attach the resource list to the object
            self.children = children

        # Otherwise
        else:

            # Use the children defined by the class
            self.children = self.__class__.children

        # Iterate over each resource defined as a child element
        for child in self.children:

            # Attach the resource to the list
            self._attach_child(child)

    def _attach_child(self, child: 'Resource'):
        """Attach a Resource as a child."""

        # Make sure that the child is of the class 'Resource'
        msg = f"Child elements must all be Resources ({type(child)})"
        try:
            if not child._is_resource:
                raise ResourceConfigurationException(msg)
        except: # noqa
            raise ResourceConfigurationException(msg)

        # Make sure that the id attribute is not repeated
        if child.id in self._children_dict:
            msg = f"Resource ids must be unique (repeated: {child.id})"
            raise ResourceConfigurationException(msg)

        # Add to the dict
        self._children_dict[child.id] = child

        # Attach this list as the parent of the resource
        child.parent = self

    #############
    # EXECUTION #
    #############
    def run(self, **kwargs) -> None:
        """
        Primary entrypoint used to execute the functionality of the Resource.

        1.  prep(): for any tasks which need to happen before the child
            resources are executed;
        2.  run_children(): call the run() method for all child resources;
        3.  run_self(): functionality associated with this Resource
        """

        self.prep(**kwargs)
        self.run_children(**kwargs)
        self.run_self(**kwargs)

    def prep(self, **kwargs) -> None:
        """
        The prep() method should be overridden by any Resource based on this.
        """
        pass

    def run_children(self, **kwargs) -> None:
        """Run the .run() method for each child Resource."""

        for r in self.children:
            r.run(**kwargs)

    def run_self(self, **kwargs) -> None:
        """
        The run_self() method should be overridden by any widget based on this.
        """
        pass

    def stop(self) -> None:
        """
        Halt the operations of the Resource.
        To be overridden by any child classes.
        """
        pass

    #################
    # EDIT CHILDREN #
    #################
    def _new_child_id(self, id_prefix="elem_") -> str:
        """Return an id attribute which can be used for a new child element."""

        i = 0
        while f"{id_prefix}{i}" in self._children_dict:
            i += 1
        return f"{id_prefix}{i}"

    def new_child(self, **kwargs) -> 'Resource':
        """
        Return an instance of a new child Resource.
        Should be overriden by instances of this class.
        """

        # If the user provides an 'id' kwarg, that will take precedence.
        # Otherwise, by using the ._new_child_id() function we can ensure
        # that the id of the new resource will not conflict with any existing.
        # If the 'id_prefix' kwarg is provided, that will be used.
        return Resource(
            id=kwargs.get(
                'id',
                self._new_child_id(
                    id_prefix=kwargs.get('id_prefix', 'elem_')
                )
            ),
            **{
                kw: val
                for kw, val in kwargs.items()
                if kw not in ['id', 'id_prefix']
            }
        )

    def append_child(self, **kwargs) -> None:
        """Add a new element at the end of the list of children."""

        # Make the new element
        new_elem = self.new_child(**kwargs)

        # Add it to the resource list
        self.children.append(new_elem)

        # Attach it to the self._resource_dict and assign the .parent attribute
        self._attach_child(new_elem)

    def insert_child(self, ix: int, **kwargs) -> None:
        """Insert a new child element at a specific index position."""

        # Make the new element
        new_elem = self.new_child(**kwargs)

        # Insert it within the resource list
        self.children.insert(ix, new_elem)

        # Attach it to the self._resource_dict and assign the .parent attribute
        self._attach_child(new_elem)

    def remove_child(self, ix: int) -> None:
        """Remove a child element from a specific index position."""

        # Remove the element from the list
        removed_elem = self.children.pop(ix)

        # Stop the operations of the Resource
        removed_elem.stop()

        # Delete the key from the _resource_dict
        del self._children_dict[removed_elem.id]

    #############
    # UTILITIES #
    #############
    def _path_to_root(self) -> List[str]:
        """
        Return the list of .id elements for this resource
        and all of its parent elements.
        """

        path = [self.id]
        if self.parent is not None:
            path.extend(self.parent._path_to_root())
        return path

    def _assert_isinstance(self, cls, case=True, parent=False):
        """
        Assert isinstance(self, cls) is case for this object.
        Use parent=True to recursively check parents.
        """

        if case:

            if not isinstance(self, cls):
                msg = f"{self.id} is not an instance of {cls.__name__}"
                raise ResourceConfigurationException(msg)

        else:

            if isinstance(self, cls):
                msg = f"{self.id} is an instance of {cls.__name__}"
                raise ResourceConfigurationException(msg)

        if parent and self.parent is not None:
            self.parent._assert_isinstance(cls, case=case, parent=parent)

    ##########
    # SOURCE #
    ##########
    def source_init(self, indent=4, skip=["self", "kwargs"]) -> str:
        """Return the code used to initialize this resource."""

        spacer = "".join([" " for _ in range(indent)])

        # Get the signature of the initialization function
        sig = signature(self.__class__.__init__)

        # Build up the parameters to use to invoke the object
        params = {}

        for kw in sig.parameters.keys():
            if kw in skip:
                continue
            else:
                params[kw] = self.get(attr=kw)

        # Format the params as a string
        params_str = f',\n{spacer}{spacer}{spacer}'.join([
            f"{kw}={self._source_val(val, indent=indent+4)}"
            for kw, val in params.items()
        ])

        return f"{self.__class__.__name__}(\n{spacer}{spacer}{spacer}{params_str}\n{spacer}{spacer})" # noqa

    def source_self(self) -> str:
        """
        Return the source code for this live widget as a string.
        """

        source = render_template(
            "source.py.j2",
            name=self._name(),
            parent_name=self._parent_name(),
            attributes=self._source_attributes(),
            functions=self._source_functions()
        )

        # Backticks in the source code will cause errors in HTML
        if "`" in source:
            raise CLIExecutionException("Script may not contain backticks (`)")

        return source

    def source_all(self) -> str:
        """
        Return the source code for this live widget as a string,
        including the source code for any other custom Resource-based classes
        which are defined in the __main__ scope.
        """

        return "\n\n".join(
            source
            for source in list(self._recursive_source(
                gathered_source={}
            ).values())[::-1]
        )

    def _recursive_source(self, gathered_source=dict()) -> dict:
        """
        Recursively traverse child elements to gather the source code for all
        Resource-based classes which are defined in the main scope.
        """

        # If this element was not defined in the widgets module
        if not self.__class__.__module__.startswith('widget'):

            # If this element has not been added
            if self._name() not in gathered_source:

                # Add it
                gathered_source[self._name()] = self.source_self()

            # Recursively add the parent element
            p = self._parent_class()()
            gathered_source = p._recursive_source(
                gathered_source=gathered_source
            )

            # For all child elements
            for child in self.children:

                # Add any source code which they may reference
                gathered_source = child._recursive_source(
                    gathered_source=gathered_source
                )

        # Return the complete set of sources which were found
        return gathered_source

    def _name(self) -> str:
        """Return the name of this widget."""

        return self.__class__.__name__

    def _parent_name(self) -> str:
        """Return the name of the parent class for this object."""

        return self._parent_class().__name__

    def _parent_class(self):
        """Return the parent class for this object."""

        for cls in getmro(self.__class__):
            if cls != self.__class__:
                return cls

    def _class_items(self, filter_functions=False):
        """
        Yield the items associated with the class of this widget.
        If filter_functions is True, yield only functions, otherwise
        do not yield any functions.
        """
        for kw, val in self.__class__.__dict__.items():
            if kw.startswith("__"):
                continue
            if filter_functions == isfunction(val):
                yield kw, val

    def _source_attributes(self) -> str:
        """
        Return a text block which captures the attributes of this class.
        """

        attributes = []

        # Iterate over the attributes of this class
        for kw, attrib in self._class_items(filter_functions=False):

            # Add it to the list
            attributes.append(f"    {kw} = {self._source_val(attrib)}")

        return "\n\n".join(attributes)

    def _source_functions(self) -> str:
        """
        Return a text block with source code for all functions of this widget
        which do not match the parent class.
        """

        return "\n\n".join([
            getsource(func)
            for _, func in self._class_items(filter_functions=True)
        ])

    def _source_val(self, val, indent=4) -> Any:
        """
        Return a string representation of an attribute value
        which can be used in source code initializing this resource.
        """

        if isinstance(val, str):
            return f'"{val}"'
        if isinstance(val, int) or isinstance(val, float):
            return f'{val}'
        elif isinstance(val, list):
            return f"""[{', '.join([
                self._source_val(i, indent=indent)
                for i in val
            ])}]"""
        elif isinstance(val, Resource):
            return val.source_init(indent=indent)
        else:
            return val

    ######################
    # GET/SET ATTRIBUTES #
    ######################
    def _get_child(self, child_id, *cont) -> 'Resource':
        """Return the child Resource with a corresponding id."""

        # Get the child resource
        r = self._children_dict.get(child_id)

        # If no key exists for child_id
        if r is None:
            msg = f"No child resource exists: {child_id}"
            raise ResourceExecutionException(msg)

        # If additional levels of nesting were specified
        if len(cont) > 0:
            # Recursively call the same function
            return r._get_child(*cont)
        # If no additional levels were requested
        else:
            # Return the element
            return r

    def get(
        self,
        path: List[str] = [],
        attr: str = "value",
        **kwargs
    ) -> Any:
        """
        Get the value of an attribute of a resource, optionally
        including a path to access attributes in nested child Resources.

        Optional kwargs are passed to the get_attr() method for the Resource.
        """

        # If a path to child elements was indicated
        if len(path) > 0:

            # Get the indicated resource
            r = self._get_child(path[0])

            # Recursively run this get function on that object
            return r.get(
                path=path[1:],
                attr=attr,
                **kwargs
            )

        else:

            # Otherwise, get an attribute of this element
            # The .value attribute may be a special case in child classes
            if attr == "value":
                return self.get_value(**kwargs)
            else:
                return self.get_attr(attr, **kwargs)

    def get_attr(self, attr, **kwargs) -> Any:
        """Return the value of the attribute for this resource."""

        # First get the attribute defined in the object
        if attr in self.__dict__:
            return self.__dict__.get(attr)

        else:

            # Next try to get the attribute defined in the class
            if attr in self.__class__.__dict__:
                return self.__class__.__dict__.get(attr)

            # If it isn't present in either place, raise an error
            else:
                msg = f"Attribute does not exist {attr} for {self.id}"
                raise ResourceExecutionException(msg)

    def get_value(self, **kwargs) -> Any:
        """
        Return the selected value of this resource (the 'value' attribute).
        Provided in the base class to be overridden by specialized resources.
        """

        return self.get_attr("value", **kwargs)

    def set(
        self,
        path: List[str] = [],
        attr: str = "value",
        value: Any = None,
        update=True,
        **kwargs
    ) -> Any:
        """
        Set the value of an attribute of a resource, optionally
        including a path to access attributes in nested child Resources.

        If update == True, the .update() method will be called after
        setting the value.

        Optional kwargs are passed to the set_attr() method for the Resource.
        """

        # If a path to child elements was indicated
        if len(path) > 0:

            # Get the indicated resource
            r = self._get_child(path[0])

            # Recursively run this set function on that object
            r.set(
                path=path[1:],
                attr=attr,
                value=value,
                update=update,
                **kwargs
            )

        else:

            # Otherwise, set an attribute of this element
            # The .value attribute may be a special case in child classes
            if attr == "value":
                self.set_value(value, **kwargs)
            else:
                self.set_attr(attr, value, **kwargs)

            # If the update flag was set
            if update:

                # Invoke the .run_self() function
                self.run_self()

    def set_attr(self, attr, val, **kwargs) -> None:
        """Set the value of an attribute for this resource."""

        self.__dict__[attr] = val

    def set_value(self, val, **kwargs) -> None:
        """Set the value of the 'value' attribute for this resource."""

        self.set_attr("value", val, **kwargs)

    def all_values(self, path=[], **kwargs) -> dict:
        """
        Return a dict with the values of every child Resource.
        The keys of the dict will be the .id element, while the
        value will be:
        (a) the results of .get_value() for each Resource
            which does not have any children, and
        (b) the results of .all_values() for each Resource which
            does have children.

        Providing a list to the path= argument will return the
        output of all_values() for the nested child resource
        located at that path.

        Optional kwargs will be passed along to those methods.
        """

        # If a path was specified
        if len(path) > 0:

            # The first element in the path must be a child .id
            child_id = path.pop(0)

            # Get the resource
            r = self._get_child(child_id)

            # Return the all_values() result for that resource
            return r.all_values(path=path, **kwargs)

        # If no path was provided
        else:

            # If there are child elements attached to this Resource
            if len(self._children_dict) > 0:

                # Return a dict with the results of all_values()
                # for that set of child Resources
                return {
                    child_id: child.all_values(**kwargs)
                    for child_id, child in self._children_dict.items()
                }

            # Otherwise, if there are no child elements
            else:

                # Just return the value from .get_value()
                return self.get_value(**kwargs)
