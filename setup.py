from setuptools import setup

setup(
    name='Verifier',
    version='0.1b0',
    packages=['instance'],
    package_dir={'': 'Verifier'},
    url='github.com/instance-id/verifier',
    license='MIT',
    author='instance.id',
    author_email='system@instance.id',
    description='Verifier : Unity',
    install_requires=['pymysql', 'pyodbc', 'pymssql',
                      'websockets', 'discord', 'requests']
)
