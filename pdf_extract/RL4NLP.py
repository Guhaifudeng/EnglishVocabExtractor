# encoding:utf-8
import pdfplumber
from nltk import word_tokenize, FreqDist
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
import sys

from pdf_extract.word_utils import get_valid_words_in_freq_dist


def get_chapter_freq(chapter, start_page, end_page):
    full_tokens = []
    page_range = list(range(start_page, end_page, 1))
    with pdfplumber.open('data/RL4NLP_2022.pdf', pages=page_range) as pdf:
        print('chapter name', chapter, 'page size:', end_page - start_page + 1)
        for page in pdf.pages:
            text = page.extract_text(x_tolerance=1)  # 提取文本
            tokens = word_tokenize(text)
            full_tokens.extend(tokens)
    freq_dist_nltk = FreqDist(full_tokens)
    return chapter, freq_dist_nltk


def get_all_chapter_freq(chapter_page_indexes):
    ret = []
    for index in range(len(chapter_page_indexes) - 1):
        now_chapter_start = chapter_page_indexes[index][1]
        now_chapter = chapter_page_indexes[index][0]
        next_chapter_start = chapter_page_indexes[index + 1][1]
        chapter_name, freq_dist_nltk = get_chapter_freq(now_chapter, now_chapter_start, next_chapter_start - 1)
        print(chapter_name)
        print(freq_dist_nltk)
        ret.append((chapter_name, freq_dist_nltk))
    return ret


if __name__ == '__main__':
    # 配置数据
    chapter_page_indexes = [
        ('preface', 1),
        ('content', 13),
        ('Acronyms', 18),
        ('1-Representation Learning and NLP', 25),
        ('2-Word Representation', 37),
        ('3-Compositional Semantics', 67),
        ('4-Sentence Representation', 83),
        ('5-Document Representation', 115),
        ('6-Sememe Knowledge Representation', 137),
        ('7-World Knowledge Representation', 177),
        ('8-Network Representation', 233),
        ('9-Cross-Modal Representation', 301),
        ('10-Resources', 337),
        ('11-Outlook', 347),
        ('end', 352)
    ]
    print(chapter_page_indexes)
    all_chapter_freq_dist = get_all_chapter_freq(chapter_page_indexes)
    with open('data/RL4NLP_words.txt', mode='w', encoding='utf-8') as wf:
        has_output_words = set()
        for chapter_name,chapter_freq_dist in all_chapter_freq_dist:
            this_chapter_valid_words = get_valid_words_in_freq_dist(chapter_freq_dist)
            wf.write('#'+chapter_name)
            wf.write('\n')
            for word in this_chapter_valid_words:
                if word in has_output_words or len(word) <= 2:
                    continue
                has_output_words.add(word)

                wf.write(word)
                wf.write('\n')
        wf.flush()
        wf.close()
