from setuptools import setup
import os


def package_files(directory):
    paths = []
    for path, directories, file_names in os.walk(directory):
        for filename in file_names:
            paths.append(os.path.join('..', path, filename))
    return paths


extra_files = package_files('mtgorp')

setup(
    name = 'mtgorp',
    version = '1.0',
    packages = ['mtgorp'],
    package_data = {'': extra_files},
    install_requires = [
        'antlr4-python3-runtime',
        'appdirs',
        'immutabledict',
        'hardcandy @ https://github.com/guldfisk/hardcandy/tarball/master#egg=hardcandy-1.0',
        'ijson',
        'lazy-property',
        'more-itertools',
        'multiset',
        'numpy',
        'orp @ https://github.com/guldfisk/orp/tarball/master#egg=orp-1.0',
        'pickledb',
        'requests',
        'sqlalchemy',
        'yeetlong @ https://github.com/guldfisk/yeetlong/tarball/master#egg=yeetlong-1.0',
    ]
)
