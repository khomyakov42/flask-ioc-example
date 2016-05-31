from setuptools import setup, find_packages

setup(
    name='sample',
    install_requires=[
        'Flask>=0.10.1',
        'Flask-API',
        'Flask-Testing',
        'psycopg2',
        'inject'
    ],
    packages=find_packages(),
)
