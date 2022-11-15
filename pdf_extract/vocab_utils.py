# encoding:utf-8

def read_vocab(path):
    ret = set()
    with open(path,mode='r',encoding='utf-8') as rf:
        for line in rf:
            line = line.strip()
            if not line.startswith('#'):
                ret.add(line)
    return ret

def remove_vocab(vocab_a,vocab_b):
    """
    从vocab_a中去除vocab_b，并返回新的vocab_c
    :param vocab_a:
    :param vocab_b:
    :return:
    """
    vocab_c = set()
    for word in vocab_a:
        if word not in vocab_b:
            vocab_c.add(word)
    return vocab_c


if __name__ == '__main__':
    paper_vocab = read_vocab('../data/verbal_advantage_words.txt')
    book_vocab = read_vocab('../data/RL4NLP_words.txt')
    vocab_c = remove_vocab(vocab_a=paper_vocab,vocab_b=book_vocab)
    print(len(vocab_c))
    print(vocab_c)

