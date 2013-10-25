Welcome to Flask-ReqArg
=======================

.. currentmodule:: flask.ext.reqarg


Installation
------------

Install the extension with `easy_install`: ::

    $ easy_install Flask-ReqArg

or `pip`: ::

    $ pip install Flask-ReqArg

You can also download the latest version from `GitHub <https://github.com/jason2506/flask-reqarg>`_: ::

    $ git clone https://github.com/jason2506/flask-reqarg.git
    $ cd flask-reqarg
    $ python setup.py develop


Overview
--------

When you are writing some web applications, the most common way to fetch the request arguments, such as parameters passed by GET or POST methods, is to fetch values from a dictionary-like object:

.. code-block:: python

    from flask import request

    @app.route('/foo')
    def bar():
        arg1 = request.args.get('arg1')
        arg2 = request.args.get('arg2')
        arg3 = request.args.get('arg3')
        # rest of code

The repeatedly calling of ``request.args.get()`` is tedious and not interesting for the people who write the code.

Now, **Flask-ReqArg** can avoid you to write such a boring code.

The simplest way to use it is to put the :func:`@request_args <request_args>` decorator on the line before the view function, then use the name of GET or POST arguments as the name of function arguments:

.. code-block:: python

    from flask.ext.reqarg import request_args

    @app.route('/foo')
    @request_args
    def bar(arg1, arg2, arg3):
        # rest of code

As you can see, the value of request arguments will be automatically bound to the corresponding function arguments. This can make your code simpler and more clear.


.. _using_fetchers:

Using the Fetchers
------------------

For explicitly specifying the request method or argument names to be bound, :func:`@request_args <request_args>` also accepts some :ref:`fetchers <argument_fetcher>` as its arguments.

Here is a example:

.. code-block:: python

    @request_args(get(), z=post('a'))
    def view(x, y, z):
        # rest of code

The :func:`get` fetcher, which is the first argument of :func:`@request_args <request_args>`, binds the first function argument ``x`` to the GET argument with the same name. In addition, the :func:`post` fetcher binds the function argument ``z`` to the POST argument ``a``.

The function argument ``y``, on the other hand, are not explicitly specified in the argument of :func:`@request_args <request_args>`. As a result, it is bound to the argument passed by GET or POST method (by default).


API Reference
-------------

Decorator
`````````

.. decorator::
    request_args(*args, **kwargs)

    Binds request arguments to function arguments.

    :param `_method`: The default request method of the retrieved arguments. Acceptable values include: ``'get'`` (GET method), ``'post'`` (POST method), and ``'args'`` (GET or POST method). Defaults to ``'args'``.

    This decorator also accepts some :ref:`fetchers <argument_fetcher>` as arguments. See :ref:`using_fetchers`.


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

    Puts the retrieved request arguments in a collection, and then maps it to the function argument.

    :param `_storage`: A callable which accepts arguments and creates the collection object. Defaults to :class:`dict`.

    Other acceptable arguments are same as :func:`@request_args <request_args>`.
