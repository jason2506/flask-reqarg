Welcome to Flask-ReqArg
=======================

API Reference
-------------

.. currentmodule:: flask.ext.reqarg

Decorator
`````````

.. decorator::
    request_arg(*args, **kwargs)

    Binds request arguments to function arguments.

    The simplest way to use it is to put this decorator on the line before the view function, then use the name of GET or POST arguments as the name of function arguments:

    .. code-block:: python

        @request_args
        def bar(arg1, arg2, arg3):
            # rest of code

    and it is equal to the following code:

    .. code-block:: python

        def bar():
            arg1 = request.args.get('arg1')
            arg2 = request.args.get('arg2')
            arg3 = request.args.get('arg3')
            # rest of code

    As you can see, the value of request arguments will be automatically bound to the corresponding function arguments.

    This also accepts some :ref:`fetchers <argument_fetcher>` as arguments to specify the method or name of the request arguments. The target function argument be bound depends on the position of fetcher in the ``args`` and the name set in the ``kwargs``.

    Here's a more complex example:

    .. code-block:: python

        @request_args(get(), z=post('a'))
        def view(x, y, z):
            # rest of code

    The :func:`get` fetcher, which is first argument of :func:`request_args`, binds first function argument ``x`` to the GET argument with the same name. And the :func:`post` fetcher binds the function argument ``z`` to the POST argument ``a``.

    The function argument ``y``, on the other hand, are not explicitly specified in the argument of :func:`request_args`. As a result, it is bound to the argument passed by GET or POST method (by default).


.. _argument_fetcher:

Argument Fetcher
````````````````

.. function::
    get(name=None, default=None, type=None)
    post(name=None, default=None, type=None)
    args(name=None, default=None, type=None)
    cookies(name=None, default=None, type=None)
    files(name=None)

    Fetches request argument and maps it to the function argument.

    :param `name`: The name of request argument. If ``name`` is not given, it treats the name of corresponding argument as the name of requment argument.
    :param `default`: The default value to be used if the requested data doesn't exist.
    :param `type`: A callable that is used to convert the retrieved value. If the value can't be converted, the corresponding function argument will be set to the default value.

.. function::
    collection(*args, **kwargs)

    Puts the retrieved request arguments in a collection (default is :class:`dict`), and then maps it to the function argument.

    This function can have the ``_storage`` argument to specify a callable which accepts arguments and creates the collection object.

    Other acceptable arguments are same as :func:`request_arg`.
