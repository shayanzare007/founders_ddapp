#! /usr/bin/env python

# Sample input data (piped into STDIN):
'''
118238@10	Sen.~^~Barack~^~Obama~^~and~^~his~^~wife~^~,~^~Michelle~^~Obama~^~,~^~have~^~released~^~eight~^~years~^~of~^~joint~^~returns~^~.	O~^~PERSON~^~PERSON~^~O~^~O~^~O~^~O~^~PERSON~^~PERSON~^~O~^~O~^~O~^~DURATION~^~DURATION~^~O~^~O~^~O~^~O
118238@12	During~^~the~^~2004~^~presidential~^~campaign~^~,~^~we~^~urged~^~Teresa~^~Heinz~^~Kerry~^~,~^~the~^~wealthy~^~wife~^~of~^~Sen.~^~John~^~Kerry~^~,~^~to~^~release~^~her~^~tax~^~returns~^~.	O~^~O~^~DATE~^~O~^~O~^~O~^~O~^~O~^~PERSON~^~PERSON~^~PERSON~^~O~^~O~^~O~^~O~^~O~^~O~^~PERSON~^~PERSON~^~O~^~O~^~O~^~O~^~O~^~O~^~O

For companies, the key extracted is ORGANIZATION (instead of PERSON).
'''
import os
import sys

ARR_DELIM = '~^~'
names_file = os.getcwd()+'/app/founders_ddapp/data/names.tsv'
# read names.tsv and put them into a set
names = set() 
with open(names_file) as f:
  for i,name in enumerate(f):
    names.add(name.rstrip())

# For-loop for each row in the input query
for row in sys.stdin:
  # Find phrases that are continuous words tagged with ORGANIZATION.
  sentence_id, words_str, ner_tags_str = row.strip().split('\t')
  words = words_str.split(ARR_DELIM)
  ner_tags = ner_tags_str.split(ARR_DELIM)
  start_index = 0
  phrases = []

  while start_index < len(words):
    # Checking if there is a ORGANIZATION phrase starting from start_index
    index = start_index
    while index < len(words) and ner_tags[index] == "ORGANIZATION":
      index += 1
    if index != start_index:   # found a person from "start_index" to "index"
      length = index - start_index
      start_index_bis=start_index +1
      while start_index_bis<index and words[start_index_bis] != words[start_index]:
        start_index_bis +=1
      length_bis = min(start_index_bis - start_index, index - start_index_bis)
      if start_index_bis<index and words[start_index:(start_index + length_bis)]==words[start_index_bis:(start_index_bis+ length_bis)]:
        text = ' '.join(words[start_index:(start_index + length_bis)])
        #if text in names: phrases.append((start_index, length_bis, text))
        phrases.append((start_index, length_bis, text))
      else:
        text = ' '.join(words[start_index:index])
        #if text in names: phrases.append((start_index, length, text))
        phrases.append((start_index, length, text))
    start_index = index + 1

  # Output a tuple for each ORGANIZATION phrase
  for start_position, length, text in phrases:
    print '\t'.join(
      [ str(x) for x in [
        sentence_id,
        start_position,   # start_position
        length, # length
        text,  # text
        '%s_%d' % (sentence_id, start_position)        # mention_id
      ]])
