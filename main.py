from hashtags import Analyzer
from datamanager import data_spewer
import json

analyzer = Analyzer()

def json_all_dump():
    tweetsList = []
    for id, tweet in data_spewer(lambda x: True if not "#" in x else False):
        hashtagsDic = analyzer.tweet_hashtags(tweet)
        tweetDic = {"originalString": tweet,
                    "tweetID": id,
                    "hashtags": hashtagsDic}
        tweetsList.append(tweetDic)
    with open("db_output.json", "w", encoding="utf-8") as file_output:
        file_output.write(json.dumps(tweetsList, sort_keys=True, ensure_ascii=False, indent=4, separators=(',', ': ')))

def json_load():
    with open("db_output.json", "r", encoding="utf-8") as file_in:
        tweetsList = json.loads(file_in.read(), encoding="utf-8")
    #print(tweetsList)
    return tweetsList

if __name__ == "__main__":
    json_all_dump()
    # for tweet in json_load():
    #     print(tweet)