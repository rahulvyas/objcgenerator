//
//  CJSONObject.m
//  GameTest
//
//  Created by Jonathan Wight on 11/24/10.
//  Copyright 2010 toxicsoftware.com. All rights reserved.
//

#import "CJSONObject.h"

@implementation CJSONObject

@synthesize dictionary;

- (id)initWithDictionary:(NSDictionary *)inDictionary
	{
	if ((self = [super init]) != NULL)
		{
		dictionary = [inDictionary retain];
		}
	return(self);
	}
	
- (void)dealloc
	{
	[dictionary release];
	dictionary = NULL;
	//
	[super dealloc];
	}

- (id)primitiveValueForKey:(NSString *)key
	{
	id theValue = [self.dictionary objectForKey:key];
	return(theValue);
	}


@end
