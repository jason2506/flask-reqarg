# Flask-ReqArg

**ReqArg** is a [Flask](http://flask.pocoo.org/) extension that maps request arguments into function arguments.

## Overview

If we want to get the request arguments, such as parameters passed by GET or POST method, one common way is fetching value from a dictionary-like object for each argument:

    from flask import request

    @app.route('/foo')
    def bar():
        arg1 = request.args.get('arg_name1')
        arg2 = request.args.get('arg_name2')
        arg3 = request.args.get('arg_name3')
        // rest of code

By using **ReqArg**, you can simply apply the `@request_args` decorator to bind request arguments to function arguments:

    @app.route('/foo')
    @request_args
    def bar(arg_name1, arg_name2, arg_name3):
        // rest of code

This can make your code simpler and more clear.

## License

This package is [BSD-licensed](http://www.opensource.org/licenses/BSD-3-Clause). See LICENSE file for more detail.
