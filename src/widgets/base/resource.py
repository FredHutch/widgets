from copy import deepcopy
from inspect import getmro, getsource, isfunction, signature
from typing import Any, Dict, Generator, List, Union
import numpy as np
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

    id: Union[str, None] = None
    value: Union[Any, None] = None
    label: Union[str, None] = None
    help: Union[str, None] = None
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
        value: Union[Any, None] = None,
        children: List['Resource'] = [],
        label: Union[str, None] = None,
        help: Union[str, None] = None,
        **kwargs
    ) -> None:
        """
        Set up the attributes which are used by all Resource objects.
        """

        # The 'id' cannot be empty
        if id is None or len(id) == 0:
            msg = f"Must provide id for Resource ({self.__class__.__name__})"
            raise ResourceConfigurationException(msg)

        # Save the id and starting value for this particular resource
        self.id = id

        # If a value was provided
        if value is not None:
            # Assign it
            self.value = value
        # If a value was not provided
        else:
            # Assign a copy of the class attribute
            self.value = deepcopy(self.__class__.value)

        # If no label is provided
        if label is None:
            # If the class does not have a label defined
            if self.__class__.label is None:
                # default to the id
                self.label = id.title()
            # If the class does have a label defined
            else:
                # Assign it
                self.label = deepcopy(self.__class__.label)

        # If a label is provided
        else:
            # Assign it to the class
            self.label = deepcopy(label)

        # Assign the help text, if any is provided
        if help is not None:
            self.help = deepcopy(help)
        # Otherwise default to the class attribute
        else:
            self.help = deepcopy(self.__class__.help)

        # Any additional keyword arguments
        for attr, val in kwargs.items():

            # Will be attached to this object
            self.__dict__[attr] = deepcopy(val)

        # Attach the children
        self._attach_children(children)

    def _attach_children(self, children):
        """Attach all provided children to the Resource"""

        # Children must be a list
        if not isinstance(children, list):
            msg = f"children must be a list, not {type(children)}"
            raise ResourceConfigurationException(msg)

        # The _resource_dict must be empty at initialization
        self._children_dict = dict()

        # If children were provided
        if isinstance(children, list) and len(children) > 0:

            # Attach the resource list to the object
            self.children = children

        # Otherwise
        else:

            # Use the children defined by the class
            self.children = deepcopy(self.__class__.children)

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

    #############
    # UTILITIES #
    #############
    def _root(self) -> 'Resource':
        """Return the recursive parent element which does not have a parent."""

        if self.parent is None:
            return self
        else:
            return self.parent._root()

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

    def _ix(self) -> int:
        """
        Return the index position of this element in the list of children.
        """

        assert self.parent is not None, "Cannot get ix - is not a child"

        return [
            r.id
            for r in self.parent.children
        ].index(
            self.id
        )

    ##########
    # SOURCE #
    ##########
    def source_init(self, indent=4) -> str:
        """Return the code used to initialize this resource."""

        spacer = "".join([" " for _ in range(indent)])

        # Get the parameters used to initialize the object
        params = self.source_init_params(self.__class__)

        # Format the params as a string
        params_str = f',\n{spacer}{spacer}{spacer}'.join([
            f"{kw}={self._source_val(val, indent=indent+4)}"
            for kw, val in params.items()
        ])

        return f"{self.__class__.__name__}(\n{spacer}{spacer}{spacer}{params_str}\n{spacer}{spacer})" # noqa

    def source_init_params(self, cls, skip=["self", "kwargs"]):
        """Format the set of params used to initialize the object."""

        # Get the signature of the initialization function
        sig = signature(cls.__init__)

        # Build up the parameters to use to invoke the object
        params = {}

        for kw in sig.parameters.keys():
            if kw in skip:
                continue
            else:
                params[kw] = self.get(attr=kw)

        return params

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

            # If this element has already been added
            if self._name() in gathered_source:

                # Insert the source at the end of the dict
                # so that it is bumped to the top of the source code
                src = gathered_source[self._name()]
                del gathered_source[self._name()]
                gathered_source[self._name()] = src

            # If this element has not been added
            else:

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

        # If there are any option elements
        for option in getattr(self, 'options', []):

            # And those option elements are Resources
            if isinstance(option, Resource):

                # Add any source code which they may reference
                gathered_source = option._recursive_source(
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

    def _parent_class_chain(self):
        """Yield all recursive parent classes which are Resource-based."""

        try:
            c = self._parent_class()()
        except Exception as e:
            msg = f"Exception while instantiating parent of '{self.id}'"
            msg = msg + '\n\n' + f"Parent: {self._parent_name()}"
            msg = msg + '\n\n' + str(e)
            raise ResourceExecutionException(msg)

        while hasattr(c, "_is_resource"):
            yield c.__class__

            c = c._parent_class()()

    def _source_attributes(self) -> str:
        """
        Return a text block which captures the attributes of this class which
        are specified as keyword arguments in the __init__ methods of this
        class or any of its parents.
        """

        # Keep track of the attributes
        attributes = dict()

        # Start with this class and add all of the
        # attributes defined in the init
        for kw, attrib in self.source_init_params(self.__class__).items():
            attributes[kw] = attrib

        # Now walk up the chain of parent classes
        for cls in self._parent_class_chain():

            # For each of the init methods on those classes
            for kw, attrib in self.source_init_params(cls).items():

                # If the kw has not yet been encountered
                if kw not in attributes:

                    # Add it
                    attributes[kw] = attrib

        return "\n\n".join([
            f"    {kw} = {self._source_val(attrib)}"
            for kw, attrib in attributes.items()
        ])

    def _source_functions(self) -> str:
        """
        Return a text block with source code for all functions which
        are defined by this class.
        """

        # Iterate through functions defined for this class
        # and join their source code
        return "\n\n".join([
            getsource(val)
            for _, val in self.__class__.__dict__.items()
            if isfunction(val)
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
        elif isinstance(val, (list, np.ndarray)):
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
            msg = f"No child resource exists within {self.id}: {child_id}"
            raise ResourceExecutionException(msg)

        # If additional levels of nesting were specified
        if len(cont) > 0:
            # Recursively call the same function
            return r._get_child(*cont)
        # If no additional levels were requested
        else:
            # Return the element
            return r

    def _find_child(self, id) -> Generator['Resource', None, None]:
        """Yield all nested child elements with the matching id."""

        if self.id == id:
            yield self

        for child in self.children:
            yield from child._find_child(id)

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
            r = self._get_child(*path)

        # Otherwise, use this element
        else:
            r = self

        # The .value attribute may be a special case in child classes
        if attr == "value":
            return r.get_value(**kwargs)
        else:
            return r.get_attr(attr, **kwargs)

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
            r = self._get_child(*path)

        # Otherwise, use this element
        else:
            r = self

        # The .value attribute may be a special case in child classes
        if attr == "value":
            r.set_value(value, **kwargs)
        else:
            r.set_attr(attr, value, **kwargs)

        # If the update flag was set
        if update:

            # Invoke the .run_self() function
            r.run_self()

    def set_attr(self, attr, val, **kwargs) -> None:
        """Set the value of an attribute for this resource."""

        self.__dict__[attr] = val

    def set_value(self, val, **kwargs) -> None:
        """Set the value of the 'value' attribute for this resource."""

        self.set_attr("value", val, **kwargs)

    def all_values(self, path=[], flatten=False, **kwargs) -> dict:
        """
        Return a dict with the values of every child Resource.
        The keys of the dict will be the .id element, while the
        value will be:
        (a) the results of .get_value() for each Resource
            which does not have any children, and
        (b) the results of .all_values() for each Resource which
            does have children.

        Alternately, if flatten=True then the output will be
        a single dict with keys given as the .id element and
        values as the results of .get_value() for each Resource,
        regardless of whether or not it has children.

        NOTE: flatten=True will raise an error if duplicate .id
        elements are encountered.

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
            return r.all_values(path=path, flatten=flatten, **kwargs)

        # If no path was provided
        else:

            # If there are child elements attached to this Resource
            if len(self._children_dict) > 0:

                # Return a dict with the results of all_values()
                # for that set of child Resources
                values = {
                    child_id: child.all_values(**kwargs)
                    for child_id, child in self._children_dict.items()
                }

                if flatten:

                    # Flatten the dict
                    return self._flatten(values, _running={})

                else:

                    # Return the nested dict
                    return values

            # Otherwise, if there are no child elements
            else:

                # Just return the value from .get_value()
                return self.get_value(**kwargs)

    def _flatten(self, values: dict, _running={}):
        """Internal method to flatten the values of a dict."""

        for kw, val in values.items():

            if isinstance(val, dict):
                _running = self._flatten(val, _running=_running)

            else:

                if kw in _running:
                    msg = f"Cannot flatten, duplicate .id found: {kw}"
                    raise ResourceExecutionException(msg)

                else:
                    _running[kw] = val

        return _running
