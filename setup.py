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
	name='mtgorp',
	version='1.0',
	packages=['mtgorp'],
	package_data={'': extra_files},
	dependency_links=[
		# 'https://github.com/guldfisk/orp/tarball/master#egg=package-1.0',
		'git+ssh://git@github.com/guldfisk/orp.git@1.0#egg=package-1.0',
	],
	install_requires=[
		'orp',
	]
)