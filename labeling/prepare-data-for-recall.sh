# Database Configuration
export DBNAME=deepdive_founder

export PGUSER=${PGUSER:-`whoami`}
export PGPASSWORD=${PGPASSWORD:-}
export PGPORT=${PGPORT:-5432}
export PGHOST=${PGHOST:-localhost}

psql $DBNAME -c "
COPY (
 SELECT hsi.relation_id
      , s.sentence_id
      , description
      , is_true
      , expectation
      , s.words
      , p.start_position AS p_start
      , p.length AS p_length
      , c.start_position AS c_start
      , c.length AS c_length
   FROM is_founder_is_true_inference hsi
      , sentences s
      , people_mentions p
      , company_mentions c
  WHERE s.sentence_id  = hsi.sentence_id
    AND p.mention_id  = hsi.person_id
    AND c.mention_id  = hsi.company_id
  ORDER BY random() LIMIT 2000
) TO STDOUT WITH CSV HEADER;
" > founder-recall/input.csv
