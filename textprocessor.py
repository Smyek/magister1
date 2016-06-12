import re
from collections import OrderedDict

def delete_n_swap_hashtags(tweetString, hashtags):
    hashtags = OrderedDict(sorted(hashtags.items(), key=lambda x: len(x[0]), reverse=True))
    refinedOnlyText, refinedString = tweetString, tweetString
    for ht in hashtags:
        refinedString = re.sub(ht, hashtags[ht], refinedString) #заменяем старый хэштег на сегментированный
        refinedOnlyText = re.sub(ht, '', refinedOnlyText) #удаляем хэштег для строки "только текст"
        refinedOnlyText = re.sub('\s{2,}', ' ', refinedOnlyText)
    return refinedOnlyText, refinedString

def spellchecker(originalString, hashtagsOldNewDict):
    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    refinedOnlyText, refinedString = delete_n_swap_hashtags(originalString, hashtagsOldNewDict)
    return refinedOnlyText, refinedString

def text_normalize(originalString, hashtagsOldNewDict):
    refinedOnlyText, refinedString = spellchecker(originalString, hashtagsOldNewDict)
    return refinedOnlyText, refinedString
