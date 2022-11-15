# encoding:utf-8
import nltk
import re
# 依赖数据
words = set(nltk.corpus.words.words())
print(len(words))
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer

lemmatizer = WordNetLemmatizer()
porter_stemmer = PorterStemmer()
lemma_pos_list = ['n', 'v', 's', 'r', 'a']


def get_valid_word_by_lemma_and_stem(word, words):
    word = word.lower()

    for lemma_pos in lemma_pos_list:
        lemma_word = lemmatizer.lemmatize(word, pos=lemma_pos)
        if lemma_word in words:
            return lemma_word
    if word in words:
        return word
    stem_word = porter_stemmer.stem(word)
    if stem_word in words:
        return stem_word
    return None

def get_valid_words_in_freq_dist(freq_dist_nltk):
    print(list(freq_dist_nltk.items())[:10])
    word_re = re.compile('^[a-zA-Z-]+$')
    index = 0
    out_vocab = set()
    for word, freq in freq_dist_nltk.items():
        if word_re.match(word):
            valid_word = get_valid_word_by_lemma_and_stem(word, words)
            index += 1
            if valid_word:
                # print(index, 'good', word, valid_word)
                out_vocab.add(valid_word)
            else:
                pass
                # print(index, 'bad ', word)
    out_vocab = sorted(out_vocab)
    return out_vocab

def get_sorted_words_by_freq_in_freq_dist(freq_dist_nltk):
    print(list(freq_dist_nltk.items())[:10])
    word_re = re.compile('^[a-zA-Z-]+$')
    index = 0
    out_vocab = dict()
    for word, freq in freq_dist_nltk.items():
        if word_re.match(word):
            valid_word = get_valid_word_by_lemma_and_stem(word, words)
            index += 1
            if valid_word:
                # print(index, 'good', word, valid_word)
                out_vocab[valid_word] = freq
            else:
                pass
                # print(index, 'bad ', word)

    out_vocab = sorted(out_vocab.items(),key=lambda key:key[1],reverse=True)
    out_vocab = [e[0] for e in out_vocab]
    return out_vocab