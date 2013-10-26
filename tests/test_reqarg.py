# -*- coding: utf-8 -*-

try:
    from io import BytesIO
except ImportError:
    from StringIO import StringIO as BytesIO

from flask import Flask, make_response
from nose.tools import assert_equal

from flask.ext.reqarg import *


class TestReqArg(object):
    def setUp(self):
        self.app = Flask(__name__)

    def test_fetch_request_args(self):
        @self.app.route('/hello')
        @request_args
        def view(name):
            return 'Hello, {0}!'.format(name)

        @self.app.route('/hello/<name>')
        @request_args
        def view_with_name(name):
            return 'Hello, {0}!'.format(name)

        client = self.app.test_client()
        resp = client.get('/hello', query_string={'name': 'John'})
        assert_equal(resp.get_data(True), 'Hello, John!')
        resp = client.get('/hello/Jason', query_string={'name': 'John'})
        assert_equal(resp.get_data(True), 'Hello, Jason!')

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

    def test_fetch_request_args_with_opts(self):
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

    def test_fetch_request_args_with_default_source(self):
        @request_args(get(), z=get(), _source='post')
        def view(x, y, z):
            return 'x={0},y={1},z={2}'.format(x, y, z)

        with self.app.test_request_context(
                method='POST',
                query_string={'x': 'pqr', 'z': '123'},
                data={'y': 'ijk'}):
            assert_equal(view(), 'x=pqr,y=ijk,z=123')

        with self.app.test_request_context(
                query_string={'x': 'pqr', 'y': 'ijk', 'z': '123'}):
            assert_equal(view(), 'x=pqr,y=None,z=123')

    def test_fetch_files(self):
        @request_args(hello=files())
        def view(hello):
            filename = hello.filename
            content = hello.stream.read()
            return '[{0}] {1}'.format(filename, content.decode())

        stream = BytesIO()
        stream.write(b'hello, world')
        stream.seek(0)
        with self.app.test_request_context(
                method='POST',
                data={'hello': (stream, 'hello.txt')}):
            assert_equal(view(), '[hello.txt] hello, world')

    def test_fetch_cookies(self):
        @self.app.route('/set', methods=['POST'])
        @request_args(val=post())
        def set(val):
            resp = make_response('done')
            resp.set_cookie('val', val)
            return resp

        @self.app.route('/get')
        @request_args(val=cookies())
        def get(val):
            return val

        client = self.app.test_client()
        client.post('/set', data={'val': 'bar'})
        resp = client.get('/get')
        assert_equal(resp.get_data(True), 'bar')

    def test_fetch_collection(self):
        class Article(object):
            def __init__(self, title, text, author):
                self.title = title
                self.content = text
                self.author = author

            def __str__(self):
                return 'Title: {0.title}\n{0.content}\nby. {0.author}'.format(self)

        @request_args(article=collection('title', 'content', 'author'))
        def view(article):
            return 'Title: {title}\n{content}\nby. {author}'.format(**article)

        @request_args(article=collection('title', 'author', text=post('content'), _storage=Article))
        def view_(article):
            return str(article)

        with self.app.test_request_context(
                method='POST',
                data={
                    'title': 'FooBar',
                    'content': 'foobarfoobar',
                    'author': 'Mary'
                }):
            assert_equal(view(), 'Title: FooBar\nfoobarfoobar\nby. Mary')
            assert_equal(view_(), 'Title: FooBar\nfoobarfoobar\nby. Mary')

