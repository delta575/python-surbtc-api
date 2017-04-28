from setuptools import setup

setup(
    name='surbtc',
    version='0.2.0',
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
        'coverage>=4.0',
        'python-decouple>=3.0',
    ],
    zip_safe=True
)
