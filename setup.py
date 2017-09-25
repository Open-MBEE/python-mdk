"""A setuptools based setup module.
"""

from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='python-mdk',
    version='0.1.3',
    description='Python wrapper for MMS integration.',
    long_description=long_description,
    author='JPL CAE, Brandon Campanile',
    author_email='cae-support@jpl.nasa.gov',
    url='',
    license='ASL 2.0',
    install_requires=["requests>=2.14.0"],
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='mms mdk development',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
)
