DROP TABLE IF EXISTS sentences CASCADE;

CREATE TABLE sentences_intermediate(
  wikipedia_url text,
  sentence_offset bigint,
  some_vals int[],
  words text[],
  pos_tags text[],
  ner_tags text[],
  lemma text[],
  some_vals2 text[],
  some_vals3 int[],
  some_vals4 text[]
)
CREATE TABLE sentences(
  document_id text,
  sentence text,
  words text[],
  lemma text[],
  pos_tags text[],
  dependencies text[],
  ner_tags text[],
  sentence_offset bigint,
  sentence_id text -- unique identifier for sentences
  );


DROP TABLE IF EXISTS people_mentions CASCADE;
CREATE TABLE people_mentions(
  sentence_id text,
  start_position int,
  length int,
  text text,
  mention_id text  -- unique identifier for people_mentions
  );

DROP TABLE IF EXISTS company_mentions CASCADE;
CREATE TABLE company_mentions(
  sentence_id text,
  start_position int,
  length int,
  text text,
  mention_id text  -- unique identifier for company_mentions
  );


DROP TABLE IF EXISTS is_founder CASCADE;
CREATE TABLE is_founder(
  person_id text,
  company_id text,
  sentence_id text,
  description text,
  is_true boolean,
  relation_id text, -- unique identifier for is_founder
  id bigint   -- reserved for DeepDive
  );

DROP TABLE IF EXISTS is_founder_features CASCADE;
CREATE TABLE is_founder_features(
  relation_id text,
  feature text
  );
