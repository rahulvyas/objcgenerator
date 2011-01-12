#!/usr/bin/env python

import json
import types
import pprint

class TypeProcessor(object):

	def __init__(self):
		self.types = {}

	def process_object(self, obj):
		if type(obj) == types.DictType:
			theProperties = self.process_dict(obj)
# 			if not len([x for x in self.types.values() if x['properties'] != theProperties]):
			theTypename = 'TYPE_%d' % len(self.types)
			self.types[theTypename] = {'typename': theTypename, 'properties': theProperties}

	def process_dict(self, obj):
		theProperties = []

		for theKey, theRecord in obj.items():
			if type(theRecord) in types.StringTypes:
				theProperties.append(dict(name = theKey, type = 'string'))
			elif type(theRecord) == types.IntType:
				theProperties.append(dict(name = theKey, type = 'integer'))
			elif type(theRecord) == types.ListType:
				theProperties.append(dict(name = theKey, type = 'array'))
				for theObject in theRecord:
					self.process_object(theObject)

		return theProperties


d = json.load(file('/Volumes/Users/schwa/Desktop/objcgenerator/tests/test_data.json'))

t = TypeProcessor()
t.process_object(d)
pprint.pprint(t.types)
