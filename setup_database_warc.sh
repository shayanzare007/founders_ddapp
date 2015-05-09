#! /usr/bin/env bash
. ./setup_env.sh

#number of files of Wikipedia corpus observed, maximum = 5148
n=5148

DBNAME=deepdive_founder

dropdb $DBNAME
createdb $DBNAME

psql -d $DBNAME < $APP_HOME/schema.sql

psql -d $DBNAME -c \
"""
DROP TABLE IF EXISTS sentences_intermediate_warc CASCADE;
CREATE TABLE sentences_intermediate_warc(
  wikipedia_url text,
  sentence_offset bigint,
  words text[],
  lemma text[],
  pos_tags text[],
  ner_tags text[],
  dependency_parents int[],
  dependency_labels text[],
  provenances text
);
"""

for i in $(seq 1 $n)
do
  echo $i
  cat $DATA_DIR/task_$i.warc | ./filter_warc | psql -d $DBNAME -c "copy sentences_intermediate_warc from STDIN;"
done

psql -d $DBNAME -c \
"""
INSERT INTO sentences
SELECT DISTINCT
        substring(wikipedia_url from 37 for char_length(wikipedia_url)-37),
        array_to_string(words,' '),
        words,
        lemma,
        pos_tags,
        dependency_labels,
        dependency_parents,
        ner_tags,
        sentence_offset,
        substring(wikipedia_url from 37 for char_length(wikipedia_url)-37)||'@'||CAST(sentence_offset AS text)
FROM sentences_intermediate_warc;
"""
