SELECT jr.client_id,
    jr.variation,
    jr.process_step,
    TIMESTAMP_DIFF(
            next_time,
            date_time,
            SECOND
        ) AS duration_sec
FROM {{ ref('int_journey_rank') }} jr
ORDER BY jr.client_id,jr.variation