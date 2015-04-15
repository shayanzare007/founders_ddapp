psql $DBNAME -c "
COPY (
 SELECT fi.relation_id
      , s.sentence_id
      , description
      , is_true
      , expectation
      , s.words
      , p.start_position AS p_start
      , p.length AS p_length
      , c.start_position AS c_start
      , c.length AS c_length
      , c.length AS c_length
      -- also include all relevant features with weights
      , features[1:6] -- top 6 features with weights
      , weights[1:6]
   FROM is_founder_is_true_inference fi
      , sentences s
      , people_mentions p
      , company_mentions c
      , ( -- find features relevant TO the relation
         SELECT relation_id
              , ARRAY_AGG(feature ORDER BY abs(weight) DESC) AS features
              , ARRAY_AGG(weight  ORDER BY abs(weight) DESC) AS weights
           FROM is_founder_features f
              , dd_inference_result_variables_mapped_weights wm
          WHERE wm.description = ('foundersFactor-' || f.feature)
          GROUP BY relation_id
        ) f
  WHERE s.sentence_id  = fi.sentence_id
    AND p.mention_id  = fi.person_id
    AND c.mention_id  = fi.company_id
    AND f.relation_id  = fi.relation_id
    AND expectation    > 0.9
  ORDER BY random() LIMIT 100
) TO STDOUT WITH CSV HEADER;
" > inference/is_founder.csv
