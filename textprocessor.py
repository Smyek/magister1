import re

def delete_hashtags(tweetString, hashtags):
    hashtags = sorted(hashtags, key=lambda x: len(x), reverse=True)
    for ht in hashtags:
        tweetString = re.sub(ht, '', tweetString)
        tweetString = re.sub('\s{2,}', ' ', tweetString)
    return tweetString

def text_normalize(originalString, hashtagsList):
    preRefinedOriginalString = originalString
    refinedOnlyText = originalString
    return refinedOnlyText, preRefinedOriginalString
