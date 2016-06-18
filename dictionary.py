import pymorphy2
import re
from collections import defaultdict
from datamanager import save_csv

class Dictionary:
    morph = pymorphy2.MorphAnalyzer()
    _dataPath = 'data/'
    _freqDictionaryFile = 'FREQ_DICTIONARY'
    _corporaFilenames = ['corpus_1.txt']

    def __init__(self):
        print('Loading Dictionary...')
        self.freqDictionary = defaultdict(lambda: 1)
        self.engFreqDictionary = defaultdict(lambda: 1)
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