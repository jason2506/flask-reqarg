# -*- coding: utf-8 -*-

from functools import wraps
from inspect import isfunction, getargspec

from flask import request

__all__ = (
    'request_args',
    'get',
    'post',
    'args',
    'files',
    'cookies',
    'collection'
)


def _get_storage_dict_map(request):
    result = {
        '_post': request.form,
        '_get': request.args,
        '_args': request.values,
        '_files': request.files,
        '_cookies': request.cookies,
        '_request': request,
    }
    return result


def _extract_method(kwargs):
    result = kwargs.pop('_method', 'args')
    if result not in ('post', 'get', 'args'):
        result = 'args'
    return result


def _extract_storage_type(kwargs):
    return kwargs.pop('_storage', dict)


def request_args(*args, **kwargs):
    method = _extract_method(kwargs)
    def decorator(func, spec=True):
        func_arg_names = getargspec(func)[0]
        if spec:
            kwargs.update(zip(func_arg_names, args))

        @wraps(func)
        def wrapper(**func_args):
            storage_dict_map = _get_storage_dict_map(request)
            storage_dict = storage_dict_map['_' + method]

            values = {}
            for arg_name in func_arg_names:
                if arg_name in func_args:
                    values[arg_name] = func_args[arg_name]
                elif arg_name in storage_dict_map:
                    values[arg_name] = storage_dict_map[arg_name]
                elif arg_name in kwargs:
                    values[arg_name] = kwargs[arg_name](request, arg_name)
                else:
                    values[arg_name] = storage_dict.get(arg_name)
            return func(**values)
        return wrapper

    if len(args) == 1 and len(kwargs) == 0 and isfunction(args[0]):
        return decorator(args[0], False)
    return decorator


def get(name=None, default=None, type=None):
    def getter(request, arg_name):
        return request.args.get(name or arg_name, default, type)
    return getter


def post(name=None, default=None, type=None):
    def getter(request, arg_name):
        return request.form.get(name or arg_name, default, type)
    return getter


def args(name=None, default=None, type=None):
    def getter(request, arg_name):
        return request.values.get(name or arg_name, default, type)
    return getter


def files(name=None):
    def getter(request, arg_name):
        return request.files.get(name or arg_name)
    return getter


def cookies(name=None, default=None, type=None):
    def getter(request, arg_name):
        return request.cookies.get(name or arg_name, default, type)
    return getter


def collection(*args, **kwargs):
    method = _extract_method(kwargs)
    storage_type = _extract_storage_type(kwargs)

    def getter(request, arg_name):
        storage_dict_map = _get_storage_dict_map(request)
        storage_dict = storage_dict_map['_' + method]

        values = {}
        for arg in args:
            values[arg] = storage_dict.get(arg)
        for arg, arg_getter in kwargs.items():
            values[arg] = arg_getter(request, arg)
        return storage_type(**values)
    return getter

