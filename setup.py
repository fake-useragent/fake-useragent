import sys
from setuptools import setup


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


# no codecs\with for python 2.5
def long_description():
    f = open('README.rst')
    rst = f.read()
    f.close()
    return rst


# Python 2.5 capability
major, minor = sys.version_info[:2]
if (major, minor) == (2, 5):
    install_requires.append('simplejson')


setup(
    name='fake-useragent',
    version='0.0.5',
    packages=packages,
    description=description,
    #include_package_data=True,
    long_description=long_description(),
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
