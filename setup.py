import ast
import os
import codecs
from setuptools import setup


class VersionFinder(ast.NodeVisitor):
    def __init__(self):
        self.version = None

    def visit_Assign(self, node):  # noqa
        if node.targets[0].id == '__version__':
            self.version = node.value.s


def read(*parts):
    filename = os.path.join(os.path.dirname(__file__), *parts)
    with codecs.open(filename, encoding='utf-8') as fp:
        return fp.read()


def find_version(*parts):
    finder = VersionFinder()
    finder.visit(ast.parse(read(*parts)))
    return finder.version


classifiers = '''\
Environment :: Web Environment
Intended Audience :: Developers
Topic :: Internet :: WWW/HTTP
Topic :: Software Development :: Libraries
License :: OSI Approved :: Apache Software License
Development Status :: 5 - Production/Stable
Natural Language :: English
Programming Language :: Python
Programming Language :: Python :: 2
Programming Language :: Python :: 3
Operating System :: OS Independent
'''

description = 'Up to date simple useragent faker with real world database'

packages = ['fake_useragent']

install_requires = []


setup(
    name='fake-useragent',
    version=find_version('fake_useragent', 'settings.py'),
    packages=packages,
    description=description,
    long_description=read('README.rst'),
    install_requires=install_requires,
    author='hellysmile',
    author_email='hellysmile@gmail.com',
    url='https://github.com/hellysmile/fake-useragent',
    zip_safe=False,
    license='http://www.apache.org/licenses/LICENSE-2.0',
    classifiers=filter(None, classifiers.split('\n')),
    keywords=[
        'user', 'agent', 'user agent', 'user-agent', 'fake'
    ]
)
