import re
import pymorphy2

class Analyzer:
    """regular expressions"""
    punctuation = "\"!$%&'()*+,…\-./:;<=>?@[\]^_`{|}~"
    htPattern = "#[^# " + punctuation + "]+"

    placeTypes = [(re.compile("^(" + htPattern + " )"), "head"),
                  (re.compile("(" + htPattern + ")$"), "tail"),
                  (re.compile("(" + htPattern + " )"), "body")]

    viewTypes = [(re.compile("([A-ZА-ЯЁ][a-zа-яё]+){2,}"), "CamelCase"),
                 (re.compile("([A-Z][А-ЯЁ]+)"), "CAPS")]

    hashtagsLang = [(re.compile("[А-Яа-яЁё]"), "ru"),
                    (re.compile("[A-Za-z]"), "en")]

    def __init__(self):
        pass

    """возвращает тип вида хэштега: """
    def hashtag_view(self, hashtag):
        for vTypeReg, vType in self.viewTypes:
            if vTypeReg.search(hashtag):
                return vType
        return "regular"

    """возвращает код языка хэштега"""
    def hashtag_lang(self, hashtag):
        language = ""
        for langReg, lang in self.hashtagsLang:
            if langReg.search(hashtag):
                language += lang
        return (lambda lang: lang if language != "ruen" else "mixed")(language)


    """возвращает хэштеги твита"""
    def tweet_hashtags(self, tweet, text_without_hashtags=False):
        print(tweet)
        hashtags = {}
        for compiledRegular, placeType in self.placeTypes:
            hashtagSearch = compiledRegular.search(tweet)
            while hashtagSearch:
                hashtag = hashtagSearch.group(1)
                tweet = re.sub(re.escape(hashtag), "", tweet).strip(" ") ##отчищаем от найденного хэштега
                hashtagSearch = compiledRegular.search(tweet)
                hashtags[hashtag.strip()] = {"placeType": placeType,
                                             "viewType": self.hashtag_view(hashtag),
                                             "lang": self.hashtag_lang(hashtag)}
        #возвращаем вторым значением только текст, если нужно
        if text_without_hashtags:
            return hashtags, tweet
        return hashtags

'''унифицирует вид обработанного хэштега'''
def hashtag_wrapper(hashtag):
    hashtag = hashtag.replace("#", "#[") + "]"
    return hashtag

def camel_segmentation(hashtag):
    camelCasePattern = re.compile("([A-ZА-ЯЁ][a-zа-яё]+)")
    hashtag = camelCasePattern.sub("\\1 ", hashtag)
    return hashtag_wrapper(hashtag.strip())

def segmentation(hashtag, htDic):
    refinedHashtag = hashtag
    if htDic["viewType"] == "CamelCase":
        refinedHashtag = camel_segmentation(hashtag)

    return refinedHashtag

if __name__ == "__main__":
    an = Analyzer()
    print(an.tweet_hashtags("#хехеhashHEAD #hashHEAD2 rrr #hashBODY rrr r rrrr #hashBODY2 #hashBODY3 r rrr rrr rr #hashTAIL #hashTAIL2"))