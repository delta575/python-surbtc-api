import sys
from setuptools import setup

if not (sys.version_info >= (3, 5)):
    sys.exit('Sorry, only Python 3.5 or later is supported')

setup(
    name='surbtc',
    version='0.2.1',
    description='SURBTC API Wrapper for Python 3',
    url='https://github.com/delta575/python-surbtc-api',
    author='Felipe Aránguiz, Sebastian Aránguiz',
    authoremail='faranguiz575@gmail.com, sarang575@gmail.com',
    license='MIT',
    packages=[
        'surbtc'
    ],
    package_dir={
        'surbtc': 'surbtc',
    },
    install_requires=[
        'requests',
    ],
    tests_require=[
        'python-decouple',
    ],
    zip_safe=True
)
