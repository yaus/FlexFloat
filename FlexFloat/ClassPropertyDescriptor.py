from typing import Callable, Optional, Any, Type


class ClassPropertyDescriptor(object):
    """
    A class that allows properties to be used at the class level.

    Attributes:
        getter_function (Callable): The getter function for the property.
        setter_function (Callable, optional): The setter function for the property. Defaults to None.
    """

    def __init__(self, getter_function: Callable, setter_function: Optional[Callable] = None):
        """
        Initialize the descriptor with getter and setter methods.

        Args:
            getter_function (Callable): The getter function for the property.
            setter_function (Callable, optional): The setter function for the property. Defaults to None.
        """
        self.getter_function = getter_function
        self.setter_function = setter_function

    def __get__(self, obj: Any, klass: Optional[Type] = None) -> Any:
        """
        Get the value of the property.

        Args:
            obj (Any): The object instance.
            klass (Any, optional): The class of the object instance. Defaults to None.

        Returns:
            Any: The value of the property.
        """
        if klass is None:
            klass = type(obj)
        return self.getter_function.__get__(obj, klass)()

    def __set__(self, obj: Any, value: Any) -> None:
        """
        Set the value of the property.

        Args:
            obj (Any): The object instance.
            value (Any): The value to set.

        Raises:
            AttributeError: If no setter function is defined.
        """
        if not self.setter_function:
            raise AttributeError("can't set attribute")
        type_ = type(obj)
        self.setter_function.__get__(obj, type_)(value)

    def setter(self, func: Callable) -> 'ClassPropertyDescriptor':
        """
        Define the setter method for the property.

        Args:
            func (Callable): The setter function.

        Returns:
            ClassPropertyDescriptor: The descriptor instance.
        """
        if not isinstance(func, (classmethod, staticmethod)):
            func = classmethod(func)
        self.setter_function = func
        return self


def classproperty(func: Callable[[Type], Callable]) -> ClassPropertyDescriptor:
    """
    A function that creates a ClassPropertyDescriptor for a method.

    Args:
        func (Callable[[Type], Callable]): The method to create a ClassPropertyDescriptor for.

    Returns:
        ClassPropertyDescriptor: The descriptor instance.
    """
    if not isinstance(func, (classmethod, staticmethod)):
        func = classmethod(func)

    return ClassPropertyDescriptor(func)
