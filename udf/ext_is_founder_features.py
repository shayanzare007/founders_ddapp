#! /usr/bin/env python

import sys
import ddlib     # DeepDive python utility

ARR_DELIM = '~^~'
nbWordsBetweenPeopleCompanyConsidered = 5

# For each input tuple
for row in sys.stdin:
  parts = row.strip().split('\t')
  if len(parts) != 7: 
    print >>sys.stderr, 'Failed to parse row:', row
    continue
  
  # Get all fields from a row
  words = parts[0].split(ARR_DELIM)
  relation_id = parts[1]
  p2_text = parts[2]
  p1_start, p1_length, p2_start, p2_length = [int(x) for x in parts[3:]]

  # Unpack input into tuples.
  span1 = ddlib.Span(begin_word_id=p1_start, length=p1_length)
  span2 = ddlib.Span(begin_word_id=p2_start, length=p2_length)

  # Features for this pair come in here
  features = set()
  
  # Feature 1: Bag of words between the two phrases
  words_between = ddlib.tokens_between_spans(words, span1, span2)
  count = 1
  for word in words_between.elements:
    if count < nbWordsBetweenPeopleCompanyConsidered:
      features.add("word_between=" + word)
    count +=1
    

  # Feature 2: Number of words between the two phrases
  features.add("num_words_between=%s" % len(words_between.elements))

  # Feature 3: Is the last name of the founder included in the name of the company?
  last_word_left = ddlib.materialize_span(words, span1)[-1]
  if (last_word_left in p2_text):
    features.add("potential_last_name_match")

  for feature in features:  
    print str(relation_id) + '\t' + feature 

