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
