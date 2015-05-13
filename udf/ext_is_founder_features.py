#! /usr/bin/env python

import sys, os
import ddlib     # DeepDive python utility
from itertools import combinations

ARR_DELIM = '~^~'
WORDS_BETWEEN_BUCKETS = [(0,1),(1,2),(2,3),(3,5), (5,10), (10,15), (15,sys.maxint)]

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
stop_words_fp = open(BASE_DIR + '/../udf/dicts/stop_words.txt')
stop_words = set()
for line in stop_words_fp:
    stop_words.add(line.strip())

punctuation_fp = open(BASE_DIR + '/../udf/dicts/punctuation.txt')
punctuation = set()
for line in punctuation_fp:
    punctuation.add(line.strip())


def get_bucket(num_words_between):
    for i, bucket in enumerate(WORDS_BETWEEN_BUCKETS):
        if num_words_between >= bucket[0] and num_words_between < bucket[1]:
            return i

# For each input tuple
for row in sys.stdin:
    parts = row.strip().split('\t')

    # Get all fields from a row
    words = parts[0].split(ARR_DELIM)
    lemmas = parts[1].split(ARR_DELIM)
    poses = parts[2].split(ARR_DELIM)
    dependencies = parts[3].split(ARR_DELIM)
    ners = parts[4].split(ARR_DELIM)
    relation_id = parts[5]
    p_start, p_length, c_start, c_length = [int(x) for x in parts[6:]]

  # Skip lines with empty dependency paths
    if len(dependencies) == 0:
        print >>sys.stderr, str(relation_id) + '\t' + 'DEP_PATH_EMPTY'
        continue

  # Get a sentence from ddlib -- array of "Word" objects
    try:
        sentence = ddlib.get_sentence(
            [0, ] * len(words),  [0, ] * len(words), words, lemmas, poses,
            dependencies, ners)
    except:
        print >>sys.stderr, dependencies
        continue

    # Create two spans of person mentions
    span1 = ddlib.Span(begin_word_id=p_start, length=p_length)
    span2 = ddlib.Span(begin_word_id=c_start, length=c_length)

    # Features for this pair come in here
    features = set()

    words_between = ddlib.tokens_between_spans(words, span1, span2)
    features.add("num_words_between_bucket=%s" % get_bucket(len(words_between.elements)))

    # Get generic features generated by ddlib
    for feature in ddlib.get_generic_features_relation(sentence, span1, span2):
        if 'POS_SEQ' in feature or feature.startswith('BETW') or feature.startswith('INV_BETW') or feature.startswith('NGRAM')\
            or feature.startswith('INV_NGRAM'):
            parts = feature[feature.find('[')+1: feature.find(']')].split(' ')
            reject = False
            for part in parts:
                if part in punctuation:
                    reject = True
                    break
            if reject == False and len(parts) == 1 and parts[0] in stop_words:
                reject = True

            if not reject:
                features.add(feature)

    pairs = set()
    # for pair in combinations(features, 2):
    #     pairs.add(','.join(sorted(pair)))

    for feature in features.union(pairs):
        print str(relation_id) + '\t' + feature
