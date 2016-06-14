import re
from dictionary import DICTIONARY

####regcompilers
onlyChars = '((?:\W|[A-Za-z])+)'
punct = re.compile(onlyChars, re.UNICODE)
punct_left = re.compile('^%s' % onlyChars, re.UNICODE)
punct_right = re.compile('%s$' % onlyChars, re.UNICODE)
engl = re.compile('[A-Za-z]', re.UNICODE)
puncInsideWord = re.compile("([,.:;])([А-Яа-я])")

def edits1(word):
   splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
   deletes = [a + b[1:] for a, b in splits if b]
   transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
   replaces = [a + c + b[1:] for a, b in splits for c in DICTIONARY.rusalphabet if b]
   inserts = [a + c + b for a, b in splits for c in DICTIONARY.rusalphabet]
   return set(deletes + transposes + replaces + inserts)

def known_edits2(word):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if DICTIONARY.word_in_dic(e2))

def known(words): return set(w for w in words if DICTIONARY.word_in_dic(w))

def correct(word):
    candidates = known([word]) or known(edits1(word)) or known_edits2(word) or [word]
    return max(candidates, key=lambda c: DICTIONARY.freqDictionary.get(c, 0))

def save_punct(word):
    left, right = '', ''
    lSearch, rSearch = punct_left.search(word), punct_right.search(word),
    if lSearch: left = lSearch.group(1)
    if rSearch: right = rSearch.group(1)
    word = punct.sub("", word)
    if not word:
        right = ''
    return left, word, right

def sentence_refine(sentence):
    sentence = puncInsideWord.sub("\\1 \\2", sentence)
    return sentence

def split_on_words(sentence):
    sentence = sentence_refine(sentence)
    words = sentence.split(' ')
    correct_words = []
    for word in words:
        left, word, right = save_punct(word)
        if not word:
            if not left or right:
                continue
        else:
            word = correct(word)
        correct_words.append("".join([left, word, right]))
    return ' '.join(list(correct_words))

if __name__ == '__main__':
    print(save_punct("!мама,"))
    sentence = 'Смертность малодых росиян, в последнее- дисятилетие; последовательнно уменьшилась!'
    sentence2 = 'Дима и Игорь савсем выбелись из ссил с этай сссесией...'
    print(split_on_words(sentence))
    print(split_on_words(sentence2))