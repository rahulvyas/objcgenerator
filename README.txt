objcgenerator
============

:author: Jonathan Wight <jwight@mac.com>
:description: Objective-C Code Generator


Goal
----
TODO

Install
-------

With setuptools_::

  $ easy_install -U objcgenerator

.. _setuptools: http://peak.telecommunity.com/DevCenter/setuptools


Usage
-----

In a directory containing a CoreData .xcdatamodel (or .xcdatamodeld) file:

 Usage: objcgenerator [options] [INPUT]

 Options:
   --version             show program's version number and exit
   -h, --help            show this help message and exit
   -i INPUT, --input=INPUT
                         The class specification file (type is inferred by
                         file extension, either plist or json).
   -o OUTPUT, --output=OUTPUT
                         Output directory for generated files.
   -t TEMPLATE, --template=TEMPLATE
                         Directory containing templates.
   -c CONFIG, --config=CONFIG
                         Path to config plist file (values will be passed to
                         template engine as a dictionary)
   -v, --verbose         set the log level to INFO
   --loglevel=LOGLEVEL   set the log level, 0 = no log, 10+ = level of logging
   --logfile=LOG_FILE    File to log messages to. If - or not provided then
                         stdout is used.
