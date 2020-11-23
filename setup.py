from setuptools import setup

setup(
    name='DassPass',
    version='0.2',
    packages=['forms', 'modules', 'objects'],
    author='nliaquin',
    description='A simple local password manager.',
    install_requires=['cryptography', 'pyperclip'], #external packages as dependencies
)
