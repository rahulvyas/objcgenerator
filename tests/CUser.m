//
//  CUser.m
//  <#ProjectName#>
//
//  Created by Jonathan Wight on 01/12/11
//  Copyright 2011 toxicsoftware.com. All rights reserved.
//

#import "CUser.h"

+ (void)load
	{
	NSAutoreleasePool *thePool = [[NSAutoreleasePool alloc] init];

	[self registerProperty:@"name" transformer:NULL flags:0];
	[self registerProperty:@"age" transformer:NULL flags:0];
	[self registerProperty:@"tags" transformer:NULL flags:0];

	[thePool release];
	}

@implementation CUser

@dynamic name;
@dynamic age;
@dynamic tags;

@end
