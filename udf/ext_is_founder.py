#! /usr/bin/env python

import sys
import csv
import os

# The directory of this UDF file
BASE_DIR = os.path.dirname(os.path.realpath(__file__))

# Load the founder dictionary for distant supervision.
# A person can have founded multiple companies
founders_companies = {}
lines = open(BASE_DIR + '/../data/training-data.tsv').readlines()
for line in lines:
  nameComp, namePers, relation = line.strip().split('\t')
  if relation=="1":
    if nameComp.lower() in founders_companies:
      founders_companies[nameComp.lower()].append(namePers.lower())  # Add a founder-company relation pair
    else:
      founders_companies[nameComp.lower()] = [namePers.lower()]

# The non-founders_companies lists incompatible relations, e.g. board members, directors...

# For each input tuple
for row in sys.stdin:
  parts = row.strip().split('\t')
  sentence_id, pm_id, pm_text, cm_id, cm_text = parts

  pm_text = pm_text.strip()
  cm_text = cm_text.strip()
  pm_text_lower = pm_text.lower()
  cm_text_lower = cm_text.lower()

  # DS rule 1: true if they appear in founders_companies set,
  is_true = '\N'
  if cm_text_lower in founders_companies:
    if pm_text_lower in founders_companies[cm_text_lower]:
      is_true = '1'
    else:
      is_true = '0'

  # Output relation candidates into output table
  print '\t'.join([
    pm_id, cm_id, sentence_id,
    "%s-%s" %(pm_text, cm_text),
    is_true,
    "%s-%s" %(pm_id, cm_id),
    '\N'   # leave "id" blank for system!
    ])
