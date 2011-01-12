#!/usr/bin/env python

import commands
import datetime
import glob
import logging
import optparse
import os
import pkg_resources
import plistlib
import pprint
import re
import subprocess
import sys
import tempfile

import Foundation

import genshi.template

logging.basicConfig(level = logging.DEBUG, format = '%(message)s', stream = sys.stderr)
logger = logging.getLogger()

def main(args):
	def store_open_file(option, opt_str, value, parser, *args, **kwargs):
		if value == '-':
			theFile = option.default
		else:
			theFile = file(value, kwargs['mode'])
		setattr(parser.values, option.dest, theFile)

	theUsage = '''%prog [options] [INPUT]'''
	theVersion = '%prog 0.1.12dev'

	####################################################################

#	theDefaultTemplateDirectory = pkg_resources.resource_filename('emogenerator', 'templates')
	theDefaultTemplateDirectory = '/Volumes/Users/schwa/Desktop/emogenerator/objcgenerator/templates'

	parser = optparse.OptionParser(usage=theUsage, version=theVersion)
	parser.add_option('-i', '--input', action='store', dest='input', type='string', metavar='INPUT',
		help='The input xcdatamodel or mom file (type is inferred by file extension).')
	parser.add_option('-o', '--output', action='store', dest='output', type='string', default = '', metavar='OUTPUT',
		help='Output directory for generated files.')
	parser.add_option('-t', '--template', action='store', dest='template', type='string', default = theDefaultTemplateDirectory, metavar='TEMPLATE',
		help='Directory containing templates (default: \'%s\'' % theDefaultTemplateDirectory)
	parser.add_option('-c', '--config', action='store', dest='config', type='string', metavar='CONFIG',
		help='Path to config plist file (values will be passed to template engine as a dictionary)')
	parser.add_option('-v', '--verbose', action='store_const', dest='loglevel', const=logging.INFO, default=logging.WARNING,
		help='set the log level to INFO')
	parser.add_option('', '--loglevel', action='store', dest='loglevel', type='int',
		help='set the log level, 0 = no log, 10+ = level of logging')
	parser.add_option('', '--logfile', action='callback', dest='logstream', type='string', default = sys.stderr, callback=store_open_file, callback_kwargs = {'mode':'w'}, metavar='LOG_FILE',
		help='File to log messages to. If - or not provided then stdout is used.')

	(theOptions, theArguments) = parser.parse_args(args = args[1:])

	for theHandler in logger.handlers:
		logger.removeHandler(theHandler)

#	logger.setLevel(theOptions.loglevel)
	logger.setLevel(logging.DEBUG)

	theHandler = logging.StreamHandler(theOptions.logstream)
	logger.addHandler(theHandler)

	####################################################################

# 	logger.debug(theOptions)
# 	logger.debug(theArguments)

	if theOptions.input == None and len(theArguments) > 0:
		theOptions.input = theArguments.pop(0)

	if True:
		emogenerator(theOptions, theArguments)
	else:
		try:
			emogenerator(theOptions, theArguments)
		except Exception, e:
			logger.error('Error: %s' % str(e))
			sys.exit(1)

def emogenerator(options, inArguments):
	# If we don't have an input file lets try and find one in the cwd
	if options.input == None:
		raise Exception('Could not find a data model file.')

	# If we still don't have an input file we need to bail.
	if not os.path.exists(options.input):
		raise Exception('Input file doesnt exist at %s' % options.input)


	# Set up a list of CoreData attribute types to Cocoa classes/C types. In theory this could be user configurable, but I don't see the need.
	theTypenamesByAttributeType = {
		'string': dict(type = 'NSString *', mode = 'retain'),
		'date': dict(type = 'NSDate *', mode = 'retain'),
		'data': dict(type = 'NSData *', mode = 'retain'),
		'short': dict(type = 'short', mode = 'retain'),
		'int': dict(type = 'int', mode = 'assign'),
		'integer': dict(type = 'int', mode = 'assign'),
		'long long': dict(type = 'long long', mode = 'assign'),
		'double': dict(type = 'double', mode = 'assign'),
		'float': dict(type = 'float', mode = 'assign'),
		'bool': dict(type = 'BOOL', mode = 'assign'),
		'array': dict(type = 'NSArray *', mode = 'assign'),
		}


	theObjectModel = plistlib.readPlist(options.input)

	if options.template == None:
		options.template = 'templates'

# 	logger.info('Using \'%s\'' % options.input)
# 	logger.info('Templates \'%s\'' % options.input)
# 	logger.info('Processing \'%s\'', options.input)
# 	logger.info('Using output directory: \'%s\'', options.output)
# 	logger.info('Using template directory: \'%s\'', options.template)

	# Start up genshi..
	theLoader = genshi.template.TemplateLoader(options.template)

	theContext = dict(
		C = lambda X:X[0].upper() + X[1:],
		author = Foundation.NSFullUserName(),
		date = datetime.datetime.now().strftime('%x'),
		year = datetime.datetime.now().year,
		organizationName = '__MyCompanyName__',
		options = dict(
			suppressAccessorDeclarations = True,
			suppressAccessorDefinitions = True,
			),
		)

	theXcodePrefs = Foundation.NSDictionary.dictionaryWithContentsOfFile_(os.path.expanduser('~/Library/Preferences/com.apple.xcode.plist'))
	if theXcodePrefs:
		if 'PBXCustomTemplateMacroDefinitions' in theXcodePrefs:
			if 'ORGANIZATIONNAME' in theXcodePrefs['PBXCustomTemplateMacroDefinitions']:
				theContext['organizationName'] = theXcodePrefs['PBXCustomTemplateMacroDefinitions']['ORGANIZATIONNAME']

	# Process each entity...
	for theEntityName in theObjectModel:
		theEntityDescription = theObjectModel[theEntityName]
		# Create a dictionary describing the entity, we'll be passing this to the genshi template.
		theEntityDict = {
			'name': theEntityDescription['typename'],
			'className': theEntityDescription['classname'],
			'superClassName': 'CJSONObject',
			'properties': [],
			'relatedEntityClassNames': [],
			}

# 		if theEntityDescription.superentity():
# 			theEntityDict['superClassName'] = theEntityDescription.superentity().managedObjectClassName()

		# Process each property of the entity.
		for thePropertyDescription in theEntityDescription['properties']:

			# This dictionary describes the property and is appended to the entity dictionary we created earlier.
			thePropertyDict = {
				'property': thePropertyDescription,
				'name': thePropertyDescription['name'],
				'mode': 'assign',
				'type': None,
				}

			if thePropertyDescription['type'] not in theTypenamesByAttributeType:
				logger.warning('Did not understand the property type: %s', thePropertyDescription['type'])
				continue

			theTypenameByAttributeType = theTypenamesByAttributeType[thePropertyDescription['type']]

			thePropertyDict.update(theTypenameByAttributeType)

			theEntityDict['properties'].append(thePropertyDict)

		theTemplateNames = ['classname.h.genshi', 'classname.m.genshi']
		for theTemplateName in theTemplateNames:

			theTemplate = theLoader.load(theTemplateName, cls=genshi.template.NewTextTemplate)

			theContext['entity'] = theEntityDict

			try:
				theStream = theTemplate.generate(**theContext)
				theNewContent = theStream.render()
			except Exception, e:
				raise

			theFilename = theEntityDict['className'] + '.' + re.match(r'.+\.(.+)\.genshi', theTemplateName).group(1)

			theOutputPath = os.path.join(options.output, theFilename)

			file(theOutputPath, 'w').write(theNewContent)

if __name__ == '__main__':
	os.chdir(os.path.expanduser('~/Desktop/emogenerator/tests'))
	main(['emogenerator', '-i', 'test.plist'])
