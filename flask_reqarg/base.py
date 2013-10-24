# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractproperty
from functools import wraps
from inspect import isfunction, getargspec
from itertools import izip

__all__ = (
    'get',
    'post',
    'args',
    'files',
    'cookies',
    'collection',
    'RequestWrapperBase'
)


def _extract_method(kwargs):
    result = kwargs.pop('_method', 'args')
    if result not in ('post', 'get', 'args'):
        result = 'args'
    return result


def _extract_storage_type(kwargs):
    return kwargs.pop('_storage', dict)


def _fetch_from_dict(d, name, default, type):
    result = d.get(name, default)
    if type is not None:
        try:
            result = type(result)
        except ValueError:
            result = default
    return result


def get(name=None, default=None, type=None):
    def getter(request, arg_name):
        return request.from_get(name or arg_name, default, type)
    return getter


def post(name=None, default=None, type=None):
    def getter(request, arg_name):
        return request.from_post(name or arg_name, default, type)
    return getter


def args(name=None, default=None, type=None):
    def getter(request, arg_name):
        return request.from_get_or_post(name or arg_name, default, type)
    return getter


def files(name=None):
    def getter(request, arg_name):
        return request.from_files(name or arg_name)
    return getter


def cookies(name=None, default=None, type=None):
    def getter(request, arg_name):
        return request.from_cookies(name or arg_name, default, type)
    return getter


def collection(*args, **kwargs):
    method = _extract_method(kwargs)
    storage_type = _extract_storage_type(kwargs)

    def getter(request, arg_name):
        values = {}
        for arg in args:
            values[arg] = request.fetch(method, arg)
        for arg, arg_getter in kwargs.items():
            values[arg] = arg_getter(request, arg)
        return storage_type(**values)
    return getter


class RequestWrapperBase(object):
    __metaclass__ = ABCMeta

    def __init__(self, request):
        self._request = request
        self._storage_dict_map = {
            '_request': self._request,
            '_get': self.get_dict,
            '_post': self.post_dict,
            '_args': self.args_dict,
            '_cookies': self.cookies_dict,
            '_files': self.files_dict
        }

    def __contains__(self, name):
        return name in self._storage_dict_map

    def __getitem__(self, name):
        return self._storage_dict_map[name]

    def fetch(self, method, name):
        return self._storage_dict_map['_' + method].get(name)

    def from_get(self, name, default, type):
        return _fetch_from_dict(self.get_dict, name, default, type)

    def from_post(self, name, default, type):
        return _fetch_from_dict(self.post_dict, name, default, type)

    def from_get_or_post(self, name, default, type):
        return _fetch_from_dict(self.args_dict, name, default, type)

    def from_cookies(self, name, default, type):
        return _fetch_from_dict(self.cookies_dict, name, default, type)

    def from_files(self, name):
        return self.files_dict.get(name)

    @property
    def request(self):
        return self._request

    @abstractproperty
    def get_dict(self):
        pass

    @abstractproperty
    def post_dict(self):
        pass

    @abstractproperty
    def args_dict(self):
        pass

    @abstractproperty
    def cookies_dict(self):
        pass

    @abstractproperty
    def files_dict(self):
        pass

    @classmethod
    def create(cls, *args, **kwargs):
        pass

    @classmethod
    def request_args(cls, *args, **kwargs):
        method = _extract_method(kwargs)

        def decorator(func, spec=True):
            func_arg_names = getargspec(func)[0]
            if spec:
                kwargs.update(izip(func_arg_names, args))

            @wraps(func)
            def wrapper(*func_args, **func_kwargs):
                values = dict(izip(func_arg_names, func_args))
                request = cls.create(*func_args, **func_kwargs)
                for arg_name in func_arg_names:
                    if arg_name in func_kwargs:
                        values[arg_name] = func_kwargs[arg_name]
                    elif arg_name in request:
                        values[arg_name] = request[arg_name]
                    elif arg_name in kwargs:
                        values[arg_name] = kwargs[arg_name](request, arg_name)
                    else:
                        values[arg_name] = request.fetch(method, arg_name)
                return func(**values)
            return wrapper

        if len(args) == 1 and len(kwargs) == 0 and isfunction(args[0]):
            return decorator(args[0], False)
        return decorator
