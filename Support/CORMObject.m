//
//  CORMObject.m
//  GameTest
//
//  Created by Jonathan Wight on 11/24/10.
//  Copyright 2010 toxicsoftware.com. All rights reserved.
//

#import "CORMObject.h"

#import <objc/runtime.h>

static id MyGetter(CORMObject *self, SEL selector);

@interface CORMObject ()
@property (readwrite, nonatomic, retain) NSCache *valueCache;
@end

#pragma mark -

@implementation CORMObject

@synthesize valueCache;

+ (void)registerProperty:(NSString *)inName transformer:(NSValueTransformer *)inValueTransformer flags:(NSUInteger)inFlags
	{
	NSAutoreleasePool *thePool = [[NSAutoreleasePool alloc] init];

	if (inValueTransformer)
		{
		[[self valueTransformers] setObject:inValueTransformer forKey:inName];
		}

    if (class_addMethod(self, NSSelectorFromString(inName), (IMP)MyGetter, "@@:") == NO)
		{
		NSLog(@"Can't add method to class.");
		}

	[thePool release];
	}

+ (NSMutableDictionary *)valueTransformers
	{
	static char *sTransformerKey = "ORM_transformers";

	NSMutableDictionary *theTransformers = objc_getAssociatedObject(self, sTransformerKey);
	if (theTransformers == NULL)
		{
		theTransformers = [NSMutableDictionary dictionary];

		objc_setAssociatedObject(self, sTransformerKey, theTransformers, OBJC_ASSOCIATION_RETAIN);
		}
	return(theTransformers);
	}

#pragma mark -

- (void)dealloc
	{
	[valueCache release];
	valueCache = NULL;
	//
	[super dealloc];
	}

#pragma mark -

- (NSCache *)valueCache
	{
	if (valueCache == NULL)
		{
		valueCache = [[NSCache alloc] init];
		}
	return(valueCache);
	}

- (id)primitiveValueForKey:(NSString *)key
	{
//	AssertUnimplemented_();
	return(NULL);
	}

@end

#pragma mark -

static id MyGetter(CORMObject *self, SEL selector)
	{
	NSString *theKey = NSStringFromSelector(selector);
	id theValue = [self.valueCache objectForKey:theKey];
	if (theValue == NULL)
		{
		theValue = [self primitiveValueForKey:theKey];
		NSValueTransformer *theValueTransformer = [[[self class] valueTransformers] objectForKey:theKey];
		if (theValueTransformer)
			{
			theValue = [theValueTransformer transformedValue:theValue];
			[self.valueCache setObject:theValue forKey:theKey];
			}
		}
	return(theValue);
	}
