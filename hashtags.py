import re
import math
from dictionary import DICTIONARY



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


def _sense_segment(hashtag):
  def sub(w):
    if len(w) == 0:
      yield []
    for i in range(1, len(w) + 1):
      for s in sub(w[i:]):
        if not DICTIONARY.word_in_dic(''.join(w[:i])):
            break
        yield [''.join(w[:i])] + s
  result = list(sub(hashtag))
  if DICTIONARY.word_in_dic(hashtag) or (result == []): result.append([hashtag])
  print(len(result))
  return result

def _sense_segment_DELETE(hashtag):
    print("ONLY SENSIBLE SEGMENTS")
    segmentations = [[hashtag], ] + _sense_segment(hashtag)
    for preSegmentChunk in segmentations:
        for preSegm in preSegmentChunk:
            if not DICTIONARY.word_in_dic(preSegm):
                segmentations.remove(preSegmentChunk)
                break
    return segmentations

def maximum_match(hashtag):
    segments_scores = []
    for segments in _sense_segment(hashtag):
        length = len(segments)
        score = 0.0
        for word in segments:
            score += len(word)**2
        score = math.pow(score, 1/length)
        segments_scores.append((segments, score))
    #print(sorted(segments_scores, key=lambda x: x[1], reverse=True))
    return max(segments_scores, key=lambda x: x[1])[0]

'''унифицирует вид обработанного хэштега'''
def hashtag_wrapper(hashtag):
    hashtag = hashtag.replace("#", "#[") + "]"
    return hashtag

def camel_segmentation(hashtag):
    camelCasePattern = re.compile("([A-ZА-ЯЁ][a-zа-яё]+)")
    hashtag = camelCasePattern.sub("\\1 ", hashtag)
    return hashtag.strip()

def segmentation(hashtag, htDic):
    print("SEGMENTATION")
    if len(hashtag) > 30: return hashtag_wrapper("#" + hashtag)
    refinedHashtag = hashtag[1:]
    if htDic["viewType"] == "CamelCase":
        refinedHashtag = camel_segmentation(hashtag)
    elif htDic["viewType"] == "regular":
        print("regular")
        refinedHashtag = " ".join(maximum_match(hashtag))
        print(hashtag, refinedHashtag)

    return hashtag_wrapper("#" + refinedHashtag)

if __name__ == "__main__":
    an = Analyzer()
    print(maximum_match('слонматрос'))
    print(maximum_match('яреальнолюблюлюдейокружающихменя'))
    # print(maximum_match('попятницамносимчерное'))
    # for i in "йцукенгшщзхъфывапролджэячсмитьбю":
    #     print(i, word_in_dic(i))
    print(an.tweet_hashtags("#хехеhashHEAD #hashHEAD2 rrr #hashBODY rrr r rrrr #hashBODY2 #hashBODY3 r rrr rrr rr #hashTAIL #hashTAIL2"))