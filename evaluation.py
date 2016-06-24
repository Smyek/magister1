from datamanager import save_csv#, open_csv
from testmodule import timestamp
from main import json_load
import json
import re
punctuation = "\"!$%&'()*+,…\-./:;<=>?@[\]^_`{|}~"
htPattern = re.compile("#([^# " + punctuation + "]+)")

def advanced_hashtag_wrapper(string):
    return htPattern.sub("#[\\1]", string)

def gold_standard_template(cut=1000):
    dataListOfLists = []
    tweets = json_load(filename="data/output/db_RESULT.json")
    for tweet in tweets:
        hashtags = advanced_hashtag_wrapper(" ".join(tweet['hashtags'].keys()))
        refhashtags = " ".join([tweet['hashtags'][ht]['refinedHT'] for ht in tweet['hashtags']])
        originalString = advanced_hashtag_wrapper(tweet['originalString'])
        csvRow = [originalString, tweet['onlyText'], hashtags] + [tweet['refinedString'], tweet['refinedOnlyText'], refhashtags]
        dataListOfLists.append(csvRow)
    save_csv("gold_template", dataListOfLists[:cut], ["originalString", "onlytext", "hashtags", "goldString", "goldonlytext", "goldhashtags"]) # "refinedString", "refinedOnlyText", "refinedhashtags",

def gold_standard_template(tweetsList):
    for tweet in tweetsList:
        for hashtag in tweet['hashtags']:
            htDic = tweet['hashtags'][hashtag]
            htDic['goldHT'] = htDic['refinedHT']
        tweet['goldOnlyText'], tweet['goldString'] = tweet['refinedOnlyText'], tweet['refinedString']
    with open("data/output/gold_template_%s.json" % timestamp(), "w", encoding="utf-8") as file_output:
        file_output.write(json.dumps(tweetsList, sort_keys=True, ensure_ascii=False, indent=4, separators=(',', ': ')))

def gold_standard_template(tweetsList):
    template = []
    for tweet in tweetsList:
        template_tweet = {}
        template_tweet['tweetID'] = tweet['tweetID']
        template_tweet['goldOnlyText'], template_tweet['goldString'] = tweet['refinedOnlyText'], tweet['refinedString']
        template_tweet['originalString'] = tweet['originalString']
        template_tweet['hashtags'] = {}
        for hashtag in tweet['hashtags']:
            htDic = tweet['hashtags'][hashtag]
            template_tweet['hashtags'][hashtag] = {}
            template_tweet['hashtags'][hashtag]['goldHT'] = htDic['refinedHT']
        template.append(template_tweet)
    with open("data/output/gold_template_%s.json" % timestamp(), "w", encoding="utf-8") as file_output:
        file_output.write(json.dumps(template, sort_keys=True, ensure_ascii=False, indent=4, separators=(',', ': ')))

def make_gold_evaluation(_last_gold_id="Noid"):
    tweets = json_load(filename="data/output/db_RESULT.json")
    tweetsGold = json_load(filename="data/output/gold_template.json")
    tweetsResult = []
    COUNT_GOLD = 1
    print(len(tweets), len(tweetsGold))
    for tweet in tweetsGold:
        COUNT_GOLD += 1
        if tweet['tweetID'] == _last_gold_id: break
        for twRef in tweets:
            if twRef['tweetID'] == tweet['tweetID']:
                tweet['refinedString'] = twRef['refinedString']
                tweet['refinedOnlyText'] = twRef['refinedOnlyText']
                tweet['onlyText'] = twRef['onlyText']
                for hashtag in tweet['hashtags']:
                    htDic = tweet['hashtags'][hashtag]
                    htDic['refinedHT'] = twRef['hashtags'][hashtag]['refinedHT']
        tweetsResult.append(tweet)
    print("Number of gold tweets:", COUNT_GOLD)
    with open("data/output/gold_evaluation.json", "w", encoding="utf-8") as file_output:
        file_output.write(json.dumps(tweetsResult, sort_keys=True, ensure_ascii=False, indent=4, separators=(',', ': ')))

def write_log(filestream, elements):
    string = "[%s]\tgold\n[%s]\trefined\n\n" % elements
    filestream.write(string)

def stat_morph(stats, dataTuple, dtType, filestream=None):

    origin, refined, gold = dataTuple
    origin, refined, gold = origin.strip(), refined.strip(), gold.strip()
    if origin == gold:
        if origin == refined:
            stats[dtType]["TP"] += 1
        else:

            stats[dtType]["FP"] += 1
    else:
        if gold == refined:
            stats[dtType]["TN"] += 1
        else:
            if filestream: write_log(filestream, (gold, refined))
            stats[dtType]["FN"] += 1
    return stats

def precision_recall(stats, dtType):
    TP, FP, FN = float(stats[dtType]["TP"]), stats[dtType]["FP"], stats[dtType]["FN"]
    precision = TP/(TP+FP)
    recall = TP/(TP+FN)
    f1 = 2 * ((precision*recall)/(precision+recall))
    print("precision", precision)
    print("recall", recall)
    print("f1", f1)
    return precision, recall, f1

def evaluation():
    f = open("data/output/eval_log.txt", "w", encoding="utf-8")
    tweets = json_load(filename="data/output/gold_evaluation.json")
    stats = {"originalString": {}, "onlyText": {}, "hashtags": {}}
    for st in stats: stats[st] = {"TP": 0, "FP": 0, "TN": 0, "FN": 0}
    for tweet in tweets:
        for hashtag in tweet['hashtags']:
            htDic = tweet['hashtags'][hashtag]
            stats = stat_morph(stats, (advanced_hashtag_wrapper(hashtag), htDic['refinedHT'], htDic['goldHT']) , "hashtags")
        stats = stat_morph(stats, (advanced_hashtag_wrapper(tweet['originalString']), tweet['refinedString'], tweet['goldString']) , "originalString", filestream=f)
        stats = stat_morph(stats, (tweet['onlyText'], tweet['refinedOnlyText'], tweet['goldOnlyText']) , "onlyText")
    for cat in stats:
        print(cat, stats[cat])
        precision_recall(stats, cat)
    f.close()
    return stats
if __name__ == "__main__":
    tweets = json_load(filename="data/output/db_RESULT.json")
    #gold_standard_template(tweets)
    #evaluation()
    make_gold_evaluation("408917349853827072")
    evaluation()