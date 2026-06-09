SELECT jr.client_id,
  jr.variation,
  MAX(CASE WHEN jr.step_rank = 1 THEN 1 ELSE 0 END) AS start,
  MAX(CASE WHEN jr.step_rank = 2 THEN 1 ELSE 0 END) AS step_1,
  MAX(CASE WHEN jr.step_rank = 3 THEN 1 ELSE 0 END) AS step_2,
  MAX(CASE WHEN jr.step_rank = 4 THEN 1 ELSE 0 END) AS step_3,
  MAX(CASE WHEN jr.step_rank = 5 THEN 1 ELSE 0 END) AS confirm
FROM {{ ref('int_journey_rank') }} jr
GROUP BY jr.client_id,jr.variation
ORDER BY jr.client_id,jr.variation