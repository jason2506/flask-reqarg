# -*- coding: utf-8 -*-

from flask import request

from .base import *

__all__ = (
    'request_args',
    'get',
    'post',
    'args',
    'files',
    'cookies',
    'collection'
)


class _FlaskRequestWrapper(RequestWrapperBase):

    @property
    def get_dict(self):
        return self._request.args

    @property
    def post_dict(self):
        return self._request.form

    @property
    def args_dict(self):
        return self._request.values

    @property
    def cookies_dict(self):
        return self._request.cookies

    @property
    def files_dict(self):
        return self._request.files

    def from_get(self, name, default, type):
        return self._request.args.get(name, default, type)

    def from_post(self, name, default, type):
        return self._request.form.get(name, default, type)

    def from_get_or_post(self, name, default, type):
        return self._request.values.get(name, default, type)

    def from_cookies(self, name, default, type):
        return self._request.cookies.get(name, default, type)

    def from_files(self, name):
        return self._request.files.get(name)

    @classmethod
    def create(cls, *args, **kwargs):
        return cls(request)


request_args = _FlaskRequestWrapper.request_args
