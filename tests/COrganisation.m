//
//  COrganisation.m
//  <#ProjectName#>
//
//  Created by Jonathan Wight on 01/12/11
//  Copyright 2011 toxicsoftware.com. All rights reserved.
//

#import "COrganisation.h"

+ (void)load
	{
	NSAutoreleasePool *thePool = [[NSAutoreleasePool alloc] init];

	[self registerProperty:@"name" transformer:NULL flags:0];
	[self registerProperty:@"users" transformer:NULL flags:0];

	[thePool release];
	}

@implementation COrganisation

@dynamic name;
@dynamic users;

@end
