import pymorphy2
import re
from collections import defaultdict
from datamanager import save_csv, json_load

class Dictionary:
    morph = pymorphy2.MorphAnalyzer()
    _dataPath = 'data/'
    _freqDictionaryFile = 'FREQ_DICTIONARY'
    _freqDictionaryTwitterFile = 'FREQ_DICTIONARY_TWITTER'
    _corporaFilenames = ['corpus_1.txt']

    def __init__(self):
        print('Loading Dictionary...')
        self.freqDictionary = defaultdict(lambda: 1)
        self.freqDictionaryTwitter = defaultdict(lambda: 0)
        self.engFreqDictionary = defaultdict(lambda: 0)
        self.engWordsList = []
        self.rusalphabet = 'абвгдеёжзийклмнопрстуфхцчшщьъыэюя'
        self._load_freq_dict()
        self._load_english_dict()

        self._hashtags_refined = {}
        self._words_refined = {}

        self._hashtags_forms = defaultdict(lambda: {})
        print('Loaded.')

    def word_in_dic(self, word, lang='ru'):
        # if word in "енгыплджэч": return False
        if lang=="ru" and (self.morph.word_is_known(word)):
            return True
        if lang=="en" and (word in self.engFreqDictionary):
            return True
        return False

    def _make_freq_dict(self):
        for fName in self._corporaFilenames:
            with open(self._dataPath + fName, "r", encoding="utf-8") as f:
                tokens = re.findall('[a-zа-я]+', f.read().lower())
                for w in tokens:
                    self.freqDictionary[w] += 1
        save_csv(self._freqDictionaryFile, self.freqDictionary, ['token', 'freq'], islist=False)

    def _make_freq_dict_twitter(self):
        tweets = json_load()
        for tweet in tweets:
            tokens = re.findall('[а-я]+', tweet["onlyText"].lower())
            for w in tokens:
                if w in self.freqDictionary:
                    self.freqDictionary[w] += 1
                else:
                    self.freqDictionaryTwitter[w] += 1
        dKeys = list(self.freqDictionaryTwitter.keys())
        for w in dKeys:
            if self.freqDictionaryTwitter[w] == 1:
                del self.freqDictionaryTwitter[w]
        save_csv(self._freqDictionaryTwitterFile, self.freqDictionaryTwitter, ['token', 'freq'], islist=False)

    def _load_english_dict(self):
        with open(self._dataPath + "eng_words.txt", "r", encoding="utf-8") as f:
            tokens = f.read().split('\n')
            for w in tokens:
                self.engFreqDictionary[w] += 1


    def _load_freq_dict(self):
        self.freqDictionary = defaultdict(lambda: 1)
        with open(self._dataPath + 'output/' + self._freqDictionaryFile + ".csv", "r", encoding="utf-8") as f:
            next(f)
            for line in f:
                token, freq = line.strip().split('\t')
                self.freqDictionary[token] = int(freq)

DICTIONARY = Dictionary()

if __name__ == "__main__":
    exit()
    DICTIONARY._make_freq_dict()