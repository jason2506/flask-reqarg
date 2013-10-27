# -*- coding: utf-8 -*-

from sys import version_info
from abc import ABCMeta, abstractproperty
from functools import wraps
from inspect import isfunction, getargspec

if version_info[0] == 2:
    from itertools import izip as zip

__all__ = (
    'get',
    'post',
    'args',
    'files',
    'cookies',
    'collection',
    'RequestWrapperBase'
)


def _extract_opt_source(kwargs):
    result = kwargs.pop('_source', 'args')
    if result not in ('post', 'get', 'args', 'files', 'cookies'):
        result = 'args'
    return result


def _extract_opt_storage_type(kwargs):
    return kwargs.pop('_storage', dict)


def _fetch_from_dict(d, name, default, type):
    result = d.get(name, default)
    if type is not None:
        try:
            result = type(result)
        except ValueError:
            result = default
    return result


def get(name=None, default=None, type=None, getlist=False):
    def fetch_one(request, arg_name):
        return request.from_get(name or arg_name, default, type)

    def fetch_all(request, arg_name):
        return request.list_from_get(name or arg_name)

    return fetch_all if getlist else fetch_one


def post(name=None, default=None, type=None, getlist=False):
    def fetch_one(request, arg_name):
        return request.from_post(name or arg_name, default, type)

    def fetch_all(request, arg_name):
        return request.list_from_post(name or arg_name)

    return fetch_all if getlist else fetch_one


def args(name=None, default=None, type=None, getlist=False):
    def fetch_one(request, arg_name):
        return request.from_get_or_post(name or arg_name, default, type)

    def fetch_all(request, arg_name):
        return request.list_from_get_or_post(name or arg_name)

    return fetch_all if getlist else fetch_one


def files(name=None, getlist=False):
    def fetch_one(request, arg_name):
        return request.from_files(name or arg_name)

    def fetch_all(request, arg_name):
        return request.list_from_files(name or arg_name)

    return fetch_all if getlist else fetch_one


def cookies(name=None, default=None, type=None):
    def fetch(request, arg_name):
        return request.from_cookies(name or arg_name, default, type)
    return fetch


def collection(*args, **kwargs):
    source = _extract_opt_source(kwargs)
    storage_type = _extract_opt_storage_type(kwargs)

    def getter(request, arg_name):
        values = {}
        for arg in args:
            values[arg] = request.from_source(source, arg)
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

    def from_source(self, source, name):
        return self._storage_dict_map['_' + source].get(name)

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

    def list_from_get(self, name):
        return self.get_dict.getlist(name)

    def list_from_post(self, name):
        return self.post_dict.getlist(name)

    def list_from_get_or_post(self, name):
        return self.args_dict.getlist(name)

    def list_from_files(self, name):
        return self.files_dict.getlist(name)

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
        source = _extract_opt_source(kwargs)

        def decorator(func, spec=True):
            func_arg_names = getargspec(func)[0]
            if spec:
                kwargs.update(zip(func_arg_names, args))

            @wraps(func)
            def wrapper(*func_args, **func_kwargs):
                request = cls.create(*func_args, **func_kwargs)

                values = func_kwargs.copy()
                for arg_name in func_arg_names:
                    if arg_name in kwargs:
                        values[arg_name] = kwargs[arg_name](request, arg_name)
                    elif arg_name not in values:
                        values[arg_name] = request.from_source(source, arg_name)
                return func(**values)
            return wrapper

        if len(args) == 1 and len(kwargs) == 0 and isfunction(args[0]):
            return decorator(args[0], False)
        return decorator

