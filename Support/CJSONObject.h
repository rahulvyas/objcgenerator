//
//  CJSONObject.h
//  GameTest
//
//  Created by Jonathan Wight on 11/24/10.
//  Copyright 2010 toxicsoftware.com. All rights reserved.
//

#import "CORMObject.h"

@interface CJSONObject : CORMObject {

}

@property (readwrite, nonatomic, retain) NSDictionary *dictionary;

- (id)initWithDictionary:(NSDictionary *)inDictionary;

@end
