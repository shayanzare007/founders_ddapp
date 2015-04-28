#! /usr/bin/env python

import sys
import json

for line in sys.stdin:
    row = json.loads(line)
    if len(row.keys()) != 10:
        print >>sys.stderr, 'Failed to parse row:', row
        continue

    dependency_strings = []
    # print >>sys.stderr, row['dependency_parents']
    try:
        for i, label in enumerate(row['dependency_labels']):
            parent_idx = int(row['dependency_parents'][i])
            dependency_string = '{0}({1}-{2}, {3}-{4})'.format(label,
                                                               row['words'][parent_idx],
                                                               parent_idx,
                                                               row['words'][i],
                                                               i)
            dependency_strings.append(dependency_string)
    except IndexError:
        dependency_strings = None

    print json.dumps({'document_id': row['document_id'],
           'sentence': row['sentence'],
           'words': row['words'],
           'lemma': row['lemma'],
           'pos_tags': row['pos_tags'],
           'dependencies': dependency_strings,
           'ner_tags': row['ner_tags'],
           'sentence_offset': row['sentence_offset'],
           'sentence_id': row['sentence_id']
           })


