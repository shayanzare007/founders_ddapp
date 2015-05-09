#number of files of Wikipedia corpus observed, maximum = 47
n=47

#! /usr/bin/env bash
. ./setup_env.sh

# Check the data files
if [ -z "$DATA_DIR" ]; then
    echo "You need to set DATA_DIR variable"
    exit 1
fi

if [ $# = 1 ]; then
  export DBNAME=$1
else
  echo "Usage: bash setup_database DBNAME"
DBNAME=deepdive_founder
fi
echo "Set DB_NAME to ${DBNAME}."
echo "HOST is ${PGHOST}, PORT is ${PGPORT}."

dropdb $DBNAME
createdb $DBNAME

psql -d $DBNAME < $APP_HOME/schema.sql

psql -d $DBNAME -c \
"""
DROP TABLE IF EXISTS sentences_intermediate CASCADE;
CREATE TABLE sentences_intermediate(
  wikipedia_url text,
  sentence_offset bigint,
  word_ids int[],
  words text[],
  pos_tags text[],
  ner_tags text[],
  lemma text[],
  dependency_labels text[],
  dependency_parents int[],
  provenances text
);
"""

for i in $(seq 0 $n)
do
  echo $i
  ghead -n -1 $DATA_DIR/sentences-$i.tsv | ./filter | psql -d $DBNAME -c "copy sentences_intermediate from STDIN;"
done

psql -d $DBNAME -c \
"""
INSERT INTO sentences
SELECT DISTINCT
        substring(wikipedia_url from 36 for char_length(wikipedia_url)-36+1),
        array_to_string(words,' '),
        words,
        lemma,
        pos_tags,
        dependency_labels,
        dependency_parents,
        ner_tags,
        sentence_offset,
        substring(wikipedia_url from 36 for char_length(wikipedia_url)-36+1)||'@'||CAST(sentence_offset AS text)
FROM sentences_intermediate;
"""
