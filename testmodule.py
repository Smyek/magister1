import time, datetime

def timer(function_to_decorate):
        def tmp(*args, **kwargs):
            t_begin = time.time()
            res = function_to_decorate(*args, **kwargs)
            t_end = time.time()
            print("Time of function's implementation: %f" % (t_end - t_begin))
            return res
        return tmp

def timestamp():
    return datetime.datetime.now().strftime("%H.%M.%S-%d.%m.%Y")


def test_pymorphy_word_known():
    @timer
    def words_check():
        for w in words:
            DICTIONARY.morph.word_is_known(w)
    from dictionary import DICTIONARY
    import random
    words = []
    wordsD = list(DICTIONARY.freqDictionary.keys())
    while len(words) < 1000000:
        words.append(random.choice(wordsD))
    print (len(words))
    print("words 1000 complete")
    words_check()

if __name__ == "__main__":
    print(timestamp())
