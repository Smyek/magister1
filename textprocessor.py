import re
from collections import OrderedDict
from spellcheck import split_on_words

def delete_n_swap_hashtags(tweetString, hashtags):
    hashtags = OrderedDict(sorted(hashtags.items(), key=lambda x: len(x[0]), reverse=True))
    refinedOnlyText, refinedString = tweetString, tweetString
    for ht in hashtags:
        refinedString = re.sub(ht, hashtags[ht], refinedString) #заменяем старый хэштег на сегментированный
        refinedOnlyText = re.sub(ht, '', refinedOnlyText) #удаляем хэштег для строки "только текст"
        refinedOnlyText = re.sub('\s{2,}', ' ', refinedOnlyText)
    return refinedOnlyText, refinedString

def separate_hashtags(originalString, hashtagsOldNewDict):
    # print("SEPARATING!")
    delimiter = '&>'
    for ht in hashtagsOldNewDict:
        originalString = re.sub("(%s)([ ]|$)" % ht, "%s\\1%s" % (delimiter, delimiter), originalString)
    return originalString.split(delimiter)

def to_spellcheck(splitPart, hashtags):
    if splitPart in hashtags:
        return False
    if "http" in splitPart:
        return False
    return True

def spellchecker(originalString, hashtagsOldNewDict):
    splittedStrng = separate_hashtags(originalString, hashtagsOldNewDict)
    resultString = []
    for part in splittedStrng:
        if not part: continue
        if to_spellcheck(part, hashtagsOldNewDict):
            part = split_on_words(part)
        resultString.append(part)

    originalString = " ".join(resultString)
    # print(originalString, "spellchecker DONE")
    refinedOnlyText, refinedString = delete_n_swap_hashtags(originalString, hashtagsOldNewDict)
    # print(refinedOnlyText, "refinedOnlyText\n", refinedString, "refinedString")
    return refinedOnlyText, refinedString

def text_normalize(originalString, hashtagsOldNewDict):
    refinedOnlyText, refinedString = spellchecker(originalString, hashtagsOldNewDict)
    return refinedOnlyText, refinedString

if __name__ == '__main__':
    sentence = '#жесть Смертность малодых росиян, #мда в последнее- дисятилетие; последовательнно уменьшилась! #россияздесьисегодня'
