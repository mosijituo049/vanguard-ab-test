SELECT
    jr.client_id,
    jr.variation,
    -- jr.visit_seq,
    jr.step_rank,
    -- jr.next_rank,

    -- next_rank - step_rank AS step_diff,

    -- jr.date_time,

    CASE
        WHEN next_rank IS NULL THEN 'end'
        WHEN next_rank = step_rank THEN 'same_step'
        WHEN next_rank = step_rank + 1 THEN 'forward'
        WHEN next_rank > step_rank + 1 THEN 'skip'
        WHEN next_rank < step_rank THEN 'backward'
    END AS transition_type

FROM {{ ref('int_journey_rank') }} jr