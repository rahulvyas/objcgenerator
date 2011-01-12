//
//  CORMObject.h
//  GameTest
//
//  Created by Jonathan Wight on 11/24/10.
//  Copyright 2010 toxicsoftware.com. All rights reserved.
//

#import <Foundation/Foundation.h>

@interface CORMObject : NSObject {

}

+ (void)registerProperty:(NSString *)inName transformer:(NSValueTransformer *)inValueTransformer flags:(NSUInteger)inFlags;
+ (NSMutableDictionary *)valueTransformers;

- (id)primitiveValueForKey:(NSString *)key;

@end
