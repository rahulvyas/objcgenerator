//
//  CUser.h
//  <#ProjectName#>
//
//  Created by Jonathan Wight on 01/12/11
//  Copyright 2011 toxicsoftware.com. All rights reserved.
//

#import "CJSONObject.h"

@interface CUser : CJSONObject {
}

@property (readwrite, nonatomic, retain) NSString * name;
@property (readwrite, nonatomic, assign) int age;
@property (readwrite, nonatomic, assign) NSArray * tags;

@end
