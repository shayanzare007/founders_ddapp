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
cat $DATA_DIR/sentences-0.tsv | psql -d $DBNAME -c "copy sentences_intermediate from STDIN;"

offset_url = 36
SELECT  substring(wikipedia_url from offset_url for char_length(wikipedia_url)-offset_url+1),
        array_to_string(words,' '),
        words,
        lemma,
       pos_tags,
        NULL,
        ner_tags,
        sentence_offset,
        substring(wikipedia_url from offset_url for char_length(wikipedia_url)-offset_url+1)||'@'||CAST(sentence_offset AS text)
FROM sentences_intermediate) | sentences

