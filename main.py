from hashtags import Analyzer, segmentation
from textprocessor import text_normalize
from datamanager import data_spewer
from collections import defaultdict, OrderedDict
from dictionary import DICTIONARY
import testmodule
import json

analyzer = Analyzer()

"""Доп функция нормализации. Получает на вход json_load().
-предобрабатывает CamelCase хэштеги
"""
def pre_process(tweetsList):
    """GATHER"""
    for tweet in tweetsList:
        for hashtag in tweet['hashtags']:
            hashtagLower = hashtag.lower()
            if hashtagLower != hashtag:
                DICTIONARY._hashtags_forms[hashtagLower][hashtag] = tweet['hashtags'][hashtag]

    """APPLY"""
    for hasht in DICTIONARY._hashtags_forms:
        if len(DICTIONARY._hashtags_forms[hasht].keys()) < 2: continue
        print(hasht)
        print(DICTIONARY._hashtags_forms[hasht])
    exit()
    with open("data/output/db_RESULT_%s.json" % testmodule.timestamp(), "w", encoding="utf-8") as file_output:
        file_output.write(json.dumps(tweetsList, sort_keys=True, ensure_ascii=False, indent=4, separators=(',', ': ')))

"""Основная функция нормализации. Получает на вход json_load().
Записывает дополнительные поля в словари refinedString, refinedOnlyText
и к каждому хэштегу поле refinedHT"""
def post_process(tweetsList):
    counter = 0
    for tweet in tweetsList:
        counter += 1
        if counter%50 == 0: print(counter, tweet['originalString'])
        '''Проходимся по хэштегам'''
        hashtagsOldNew = {}
        for hashtag in tweet['hashtags']:
            htDic = tweet['hashtags'][hashtag]
            htDic['refinedHT'] = segmentation(hashtag, htDic)
            hashtagsOldNew[hashtag] = htDic['refinedHT']
        '''получаем обработанну строку без хэштегов и со старыми хэштегами (чтобы их заменить на новые в конце hashtagsOldNew = OrderedDict(sorted(dic.items(), key=lambda t: len(t[0])))'''
        tweet['refinedOnlyText'], tweet['refinedString'] = text_normalize(tweet['originalString'], hashtagsOldNew)
    with open("data/output/db_RESULT_%s.json" % testmodule.timestamp(), "w", encoding="utf-8") as file_output:
        file_output.write(json.dumps(tweetsList, sort_keys=True, ensure_ascii=False, indent=4, separators=(',', ': ')))

def json_all_dump():
    tweetsList = []
    for id, tweet in data_spewer(lambda x: True if not "#" in x else False):
        hashtagsDic, onlyText = analyzer.tweet_hashtags(tweet, True)
        tweetDic = {"originalString": tweet,
                    "onlyText": onlyText,
                    "tweetID": id,
                    "hashtags": hashtagsDic}
        tweetsList.append(tweetDic)
    with open("data/output/db_output.json", "w", encoding="utf-8") as file_output:
        file_output.write(json.dumps(tweetsList, sort_keys=True, ensure_ascii=False, indent=4, separators=(',', ': ')))

def json_load(start=0, limit=-1, filename="data/output/db_output.json"):
    with open(filename, "r", encoding="utf-8") as file_in:
        tweetsList = json.loads(file_in.read(), encoding="utf-8")
    #print(tweetsList)
    return tweetsList[start:limit]

def get_all_hashtag_type(htType, htCategory='viewType', ):
    json_all_dump()
    dic = defaultdict(int)
    for tweet in json_load():
        hashtagsDic = tweet['hashtags']
        for ht in hashtagsDic:
            if hashtagsDic[ht][htCategory] == htType:
                dic[ht] += 1
    dic = OrderedDict(sorted(dic.items(), key=lambda t: t[1]))
    return dic

@testmodule.timer
def MAIN(start=0, limit=-1):
    tweets = json_load(start, limit)
    print("preprocess...")
    pre_process(tweets)
    print("preprocess done")

    print("postprocess...")
    post_process(tweets)
    print("postprocess done")

# @testmodule.timer
if __name__ == "__main__":
    # dic = get_all_hashtag_type('regular')
    # print(len('ДИРЕКШИОНЕРФОЛЛОВЬДИРЕКШИОНЕРА'))
    # #dic = OrderedDict(sorted(dic.items(), key=lambda t: len(t[0]), reverse=True))
    # for i in dic:
    #     print(i, dic[i])
    MAIN(0, 500)
