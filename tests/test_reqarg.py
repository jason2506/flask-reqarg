# -*- coding: utf-8 -*-

from flask import Flask
from nose.tools import assert_equal

from flaskext.reqarg import *


class TestReqArg(object):
    def setUp(self):
        self.app = Flask(__name__)


    def test_fetch_request_args(self):
        @request_args
        def view(name):
            return 'Hello, {0}!'.format(name)

        with self.app.test_request_context(
                query_string={'name': 'John'}):
            assert_equal(view(), 'Hello, John!')


    def test_fetch_GET_and_POST_args(self):
        @request_args(x=get(), y=post(), z=args())
        def view(x, y, z):
            return 'x={0},y={1},z={2}'.format(x, y, z)

        with self.app.test_request_context(
                method='POST',
                query_string={'x': 'ijk'},
                data={'y': 'pqr', 'z': 'abc'}):
            assert_equal(view(), 'x=ijk,y=pqr,z=abc')

        with self.app.test_request_context(
                method='POST',
                query_string={'y': 'pqr', 'z': 'abc'},
                data={'x': 'ijk'}):
            assert_equal(view(), 'x=None,y=None,z=abc')


    def test_fetch_request_args_with_options(self):
        @request_args(get(default='bar'), z=get(type=int, default=999))
        def view(x, y, z):
            return 'x={0},y={1},z={2}'.format(x, y, z)

        with self.app.test_request_context(
                query_string={'x': 'pqr', 'y': 'ijk', 'z': '123'}):
            assert_equal(view(), 'x=pqr,y=ijk,z=123')

        with self.app.test_request_context(
                query_string={'y': 'ijk', 'z': 'abc'}):
            assert_equal(view(), 'x=bar,y=ijk,z=999')

        with self.app.test_request_context():
            assert_equal(view(), 'x=bar,y=None,z=999')


    def test_fetch_request_arg_collection(self):
        @request_args(article=collection('title', 'content', 'author'))
        def view(article):
            return 'Title: {title}\n{content}\nby. {author}'.format(**article)

        with self.app.test_request_context(
                method='POST',
                data={
                    'title': 'FooBar',
                    'content': 'foobarfoobar',
                    'author': 'Mary'
                }):
            assert_equal(view(), 'Title: FooBar\nfoobarfoobar\nby. Mary')

