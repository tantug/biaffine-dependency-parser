import numpy as np
from collections import Counter
import unicodedata

def is_number(s):
    s = s.replace(',', '') # 10,000 -> 10000
    s = s.replace(':', '') # 5:30 -> 530
    s = s.replace('-', '') # 17-08 -> 1708
    s = s.replace('/', '') # 17/08/1992 -> 17081992
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False

def process_conll(in_path, out_path, lower=True, clean=True, p=0.1):
    word_counts = Counter()
    tag_counts = Counter()
    label_counts = Counter()
    with open(in_path, 'r') as f:
        for line in f:
            fields = line.split()
            if fields:
                word = fields[1].lower() if lower else fields[1]
                tag = fields[3]
                label = fields[7]
                word_counts.update([word])
                tag_counts.update([tag])
                label_counts.update([label])
    with open(out_path + ".words.txt", 'w') as f:
        for word, count in word_counts.most_common():
            processed = word
            if count == 1:
                if is_number(word) and clean:
                    processed = "<num>"
                elif np.random.random() < p:
                    processed = "<unk>"
            print("{} {} {}".format(word, processed, count), file=f)
    with open(out_path + ".tags.txt", 'w') as f:
        for tag, count in tag_counts.most_common():
            print("{} {}".format(tag, count), file=f)
    with open(out_path + ".labels.txt", 'w') as f:
        for label, count in label_counts.most_common():
            print("{} {}".format(label, count), file=f)


def compare_vocabulary(train_path, dev_path, test_path):
    train_vocab = dict()
    dev_vocab = dict()
    test_vocab = dict()

    def read_dict(path, dict):
        with open(path, 'r') as f:
            for line in f:
                word, _, count = line.split()
                dict[word] = int(count)

    read_dict(train_path, train_vocab)
    read_dict(dev_path, dev_vocab)
    read_dict(test_path, test_vocab)

    nwords_train = len(train_vocab)
    ntokens_train = sum(train_vocab.values())
    nwords_dev = len(dev_vocab)
    ntokens_dev = sum(dev_vocab.values())
    nwords_test = len(test_vocab)
    ntokens_test = sum(test_vocab.values())
    unseen_words = list(set(dev_vocab.keys()) - (set(train_vocab.keys()) & set(dev_vocab.keys())))
    num_unseen_tokens = sum([dev_vocab[w] for w in unseen_words])
    with open("vocab/data-statistics.csv", 'w') as g:
        print("dataset,nwords,ntokens", file=g)
        print("train,{},{}".format(nwords_train, ntokens_train), file=g)
        print("dev,{},{}".format(nwords_dev, ntokens_dev), file=g)
        print("test,{},{}".format(nwords_test, ntokens_test), file=g)
        print("unseen,{},{}".format(len(unseen_words), num_unseen_tokens), file=g)
    with open('vocab/unseen.txt', 'w') as f:
        for word in unseen_words:
            print("{} {}".format(word, dev_vocab[word]), file=f)


if __name__ == "__main__":
    # Example usage:
    train_path = "../../stanford-ptb/train-stanford-raw.conll"
    dev_path = "../../stanford-ptb/dev-stanford-raw.conll"
    test_path = "../../stanford-ptb/test-stanford-raw.conll"

    process_conll(train_path, "vocab/train", p=0.5, clean=False)
    process_conll(dev_path, "vocab/dev", p=0.0)
    process_conll(test_path, "vocab/test", p=0.0)
    compare_vocabulary("vocab/train.words.txt", "vocab/dev.words.txt", "vocab/test.words.txt")
