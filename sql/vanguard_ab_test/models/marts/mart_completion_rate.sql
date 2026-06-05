  SELECT jr.client_id,
    jr.variation,
    MAX(
      CASE
        WHEN jr.process_step = 'confirm'
        THEN 1
        ELSE 0
      END
    ) AS completed
  FROM `ironhack-497023.vanguard_ab_test.int_journey_rank` jr
  -- WHERE jr.process_step = "confirm" 
  GROUP BY jr.client_id,jr.variation
  -- HAVING completion_time = 0
  ORDER BY jr.client_id
)
SELECT variation,
  COUNT(*) AS total_clients,
  SUM(completed) AS completed_clients,
  ROUND(SUM(completed)/COUNT(*),4) AS completion_rate
FROM completed_list
GROUP BY variation