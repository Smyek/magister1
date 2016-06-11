from datamanager import data_spewer, save_csv
from hashtags import Analyzer

def gold_standard_template(cut=1000):
    analyzer = Analyzer()
    dataListOfLists = []
    for id, originalString in data_spewer(lambda x: True if not "#" in x else False):
        hashtags, onlytext = analyzer.tweet_hashtags(originalString, True)
        dataListOfLists.append([originalString, onlytext, " ".join(hashtags.keys())]*2)
    save_csv("gold_template", dataListOfLists[:cut], ["originalString", "onlytext", "hashtags", "goldString", "goldonlytext", "goldhashtags"])

if __name__ == "__main__":
    gold_standard_template()