#! /usr/bin/env bash

# Check the data files
if ! [ -d data ] \
  || ! [ -f data/training-data.tsv ] \
  || ! [ -f data/sentences_dump.csv ] \
  || ! [ -f data/sentences_dump_large.csv ]; then
  echo "ERROR: Data files do not exist. Get the founder training dataset ! setup"
  exit 1;
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

export APP_HOME=`cd $(dirname $0)/; pwd`

psql -d $DBNAME < $APP_HOME/schema.sql
psql -d $DBNAME -c "copy sentences from STDIN CSV;" < $APP_HOME/data/sentences_dump_large.csv