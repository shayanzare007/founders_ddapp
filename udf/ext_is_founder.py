#! /usr/bin/env python

import sys
import csv
import os

# The directory of this UDF file
BASE_DIR = os.path.dirname(os.path.realpath(__file__))

# Load the founder dictionary for distant supervision.
# A person can have founded multiple companies
founders_companies = set()
non_founders_companies = set()
lines = open(BASE_DIR + '/../data/training-data.tsv').readlines()
for line in lines:
  name1, name2, relation = line.strip().split('\t')
  if relation=="1":
    founders_companies.add((name2.lower(), name1.lower()))  # Add a founder-company relation pair
  else:
    non_founders_companies.add((name2.lower(), name1.lower()))

# The non-founders_companies lists incompatible relations, e.g. board members, directors...

# For each input tuple
for row in sys.stdin:
  parts = row.strip().split('\t')
  sentence_id, p1_id, p1_text, p2_id, p2_text = parts

  p1_text = p1_text.strip()
  p2_text = p2_text.strip()
  p1_text_lower = p1_text.lower()
  p2_text_lower = p2_text.lower()

  # DS rule 1: true if they appear in founders_companies set,
  is_true = '\N'
  if (p1_text_lower, p2_text_lower) in founders_companies:
    is_true = '1'
  # DS rule 2: false if they appear in non-founders_companies KB
  elif (p1_text_lower, p2_text_lower) in non_founders_companies:
    is_true = '0'

  # Output relation candidates into output table
  print '\t'.join([
    p1_id, p2_id, sentence_id,
    "%s-%s" %(p1_text, p2_text),
    is_true,
    "%s-%s" %(p1_id, p2_id),
    '\N'   # leave "id" blank for system!
    ])
