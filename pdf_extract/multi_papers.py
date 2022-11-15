# encoding:utf-8
import pdfplumber
from nltk import word_tokenize, FreqDist
import nltk
import re


import sys
import os

from pdf_extract.word_utils import get_valid_words_in_freq_dist


def get_chapter_freq(paper_name, paper_path):
    full_tokens = []
    with pdfplumber.open(paper_path) as pdf:
        print('chapter name', paper_name, 'page path:', paper_path)
        for page in pdf.pages:
            text = page.extract_text(x_tolerance=1)  # 提取文本
            tokens = word_tokenize(text)
            full_tokens.extend(tokens)
    freq_dist_nltk = FreqDist(full_tokens)
    return paper_name, freq_dist_nltk


def get_all_pdf_files(paper_dir):
    """
    获取当前目录下所有文件(特殊:当前目录为pdf文件名，直接返回)
    :param paper_dir:
    :return:
    """
    if paper_dir.endswith(".pdf"):
        yield paper_dir
    else:
        dir_names = os.listdir(paper_dir)
        for dir_name in dir_names:
            dir_path =os.path.join(paper_dir,dir_name)
            if os.path.isdir(dir_path):
                for dir_path in get_all_pdf_files(dir_path):
                    yield dir_path
            elif dir_path.endswith('.pdf'):
                yield dir_path


def get_all_paper_freq(paper_dir):
    ret = []
    for pdf_file_path in get_all_pdf_files(paper_dir):
        paper_name,page_freq = get_chapter_freq(os.path.split(pdf_file_path)[-1],pdf_file_path)
        ret.append((paper_name, page_freq))
    return ret




if __name__ == '__main__':
    all_chapter_freq_dist = get_all_paper_freq(paper_dir='data/papers')
    with open('data/paper_words.txt', mode='w', encoding='utf-8') as wf:
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
