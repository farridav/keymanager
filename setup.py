#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='keymanager',
    version='1.0.0',
    author='farridav',
    author_email='info@davidfarrington.co.uk',
    packages=['keyman'],
    scripts=['keymanager'],
    url='https://github.com/farridav/keymanager.git',
    license='MIT',
    description='SSH Key manager, powered by fabric',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Framework :: Fabric',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
    ],
    install_requires=["Fabric"],
)
