import re

class Analyzer:
    """regular expressions"""
    placeTypes = [(re.compile("^(#[^# ]+ )"), "head"),
                  (re.compile("(#[^# ]+)$"), "tail"),
                  (re.compile("(#[^# ]+ )"), "body")]

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
    def tweet_hashtags(self, tweet):
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
        return hashtags

if __name__ == "__main__":
    an = Analyzer()
    print(an.tweet_hashtags("#хехеhashHEAD #hashHEAD2 rrr #hashBODY rrr r rrrr #hashBODY2 #hashBODY3 r rrr rrr rr #hashTAIL #hashTAIL2"))