
from setuptools import setup, find_packages

# http://docs.python.org/distutils/setupscript.html#additional-meta-data

setup(
	name = 'objcgenerator',
	version = '0.1.0dev',

	install_requires = ['genshi >= 0.5'],
	packages = find_packages(exclude = [ 'ez_setup', 'tests' ]),
	package_data = { '': ['templates/*'] },
	include_package_data = True,
	scripts = ['scripts/objcgenerator'],
	zip_safe = True,
	author = 'Jonathan Wight',
	author_email = 'jwight@mac.com',
	classifiers = [
		'Development Status :: 3 - Alpha',
		'Environment :: MacOS X :: Cocoa',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: BSD License',
		'Operating System :: MacOS :: MacOS X',
		'Programming Language :: Objective C',
		'Topic :: Database',
		'Topic :: Software Development :: Build Tools',
		],
	description = 'Objective-C Code Generator',
	license = 'BSD License',
	long_description = file('README.txt').read(),
	platform = 'Mac OS X',
	url = 'http://github.com/schwa/objcgenerator',
	)

