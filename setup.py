"""
Flask-ReqArg
------------

The decorator that maps request arguments into function arguments.
"""

from setuptools import setup

setup(
    name='Flask-ReqArg',
    version='0.1.4',
    url='https://github.com/jason2506/flask-reqarg/',
    license='BSD',
    author='Chi-En Wu',
    author_email='',
    description='The decorator that maps request arguments into function arguments.',
    long_description=__doc__,
    packages=['flask_reqarg'],
    zip_safe=False,
    platforms='any',
    install_requires=['Flask'],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)

