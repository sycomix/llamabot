"""Decorators for turning Python functions into Jinja2-templated prompts.

This module contains decorators for turning Python functions' docstrings
into Jinja2-templated functions that accept function arguments
and return the Jinja2 templated docstrings as strings when called.

Inspired from the Outlines library.
"""


from functools import wraps
import jinja2
from jinja2 import meta
import inspect


def prompt(func):
    """Wrap a Python function into a Jinja2-templated prompt.

    :param func: The function to wrap.
    :return: The wrapped function.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        """Wrapper function.

        :param args: Positional arguments to the function.
        :param kwargs: Keyword arguments to the function.
        :return: The Jinja2-templated docstring.
        :raises ValueError: If a variable in the docstring
            is not passed into the function.
        """
        # get the function's docstring.
        docstring = func.__doc__

        # map args and kwargs onto func's signature.
        signature = inspect.signature(func)
        kwargs = signature.bind(*args, **kwargs).arguments

        # create a Jinja2 environment
        env = jinja2.Environment()

        # parse the docstring
        parsed_content = env.parse(docstring)

        # get all variables in the docstring
        variables = meta.find_undeclared_variables(parsed_content)

        # check if all variables are in kwargs
        for var in variables:
            if var not in kwargs:
                raise ValueError(f"Variable '{var}' was not passed into the function")

        # interpolate docstring with args and kwargs
        template = jinja2.Template(docstring)
        return template.render(**kwargs)

    return wrapper
