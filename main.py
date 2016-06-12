from hashtags import Analyzer, segmentation
from textprocessor import text_normalize
from datamanager import data_spewer
from collections import defaultdict, OrderedDict
import json

analyzer = Analyzer()

"""Основная функция нормализации. Получает на вход json_load().
Записывает дополнительные поля в словари refinedString, refinedOnlyText
и к каждому хэштегу поле refinedHT"""
def post_process(tweetsList):
    for tweet in tweetsList:
        '''получаем обработанну строку без хэштегов и со старыми хэштегами (чтобы их заменить на новые в конце'''
        refinedOnlyText, preRefinedOriginalString = text_normalize(tweet['originalString'],
                                                                   tweet['hashtags'].keys())


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

def json_load():
    with open("data/output/db_output.json", "r", encoding="utf-8") as file_in:
        tweetsList = json.loads(file_in.read(), encoding="utf-8")
    #print(tweetsList)
    return tweetsList

if __name__ == "__main__":
    json_all_dump()
    dic = defaultdict(int)
    for tweet in json_load():
        hashtagsDic = tweet['hashtags']
        for ht in hashtagsDic:
            if hashtagsDic[ht]['viewType'] == 'CamelCase':
                print(ht)
                dic[ht] += 1

    dic = OrderedDict(OrderedDict(sorted(dic.items(), key=lambda t: t[1])))
    for i in dic:
        print(i, dic[i])