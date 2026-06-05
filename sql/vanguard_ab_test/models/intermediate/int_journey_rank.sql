WITH journey AS (
    
    SELECT
        ej.client_id,
        ej.variation,
        ej.visitor_id,
        ej.visit_id,

        ROW_NUMBER() OVER (
            PARTITION BY ej.client_id, ej.visitor_id, ej.visit_id
            ORDER BY ej.date_time
        ) AS visit_seq,

        ej.process_step,

        LEAD(process_step) OVER (
            PARTITION BY ej.client_id, ej.visitor_id, ej.visit_id
            ORDER BY ej.date_time
        ) AS next_step,

        ej.date_time,

        LEAD(ej.date_time) OVER (
            PARTITION BY ej.client_id, ej.visitor_id, ej.visit_id
            ORDER BY ej.date_time
        ) AS next_time

    FROM {{ ref('int_experiment_journey') }} ej

),

journey_rank AS (

    SELECT
        *,

        TIMESTAMP_DIFF(
            next_time,
            date_time,
            SECOND
        ) AS duration_sec,

        CASE process_step
            WHEN 'start' THEN 1
            WHEN 'step_1' THEN 2
            WHEN 'step_2' THEN 3
            WHEN 'step_3' THEN 4
            WHEN 'confirm' THEN 5
        END AS current_rank,

        CASE next_step
            WHEN 'start' THEN 1
            WHEN 'step_1' THEN 2
            WHEN 'step_2' THEN 3
            WHEN 'step_3' THEN 4
            WHEN 'confirm' THEN 5
        END AS next_rank

    FROM journey

)

SELECT
    *,

    next_rank - current_rank AS step_diff,

    CASE
        WHEN next_step IS NULL THEN 'end'
        WHEN next_rank = current_rank THEN 'same_step'
        WHEN next_rank = current_rank + 1 THEN 'forward'
        WHEN next_rank > current_rank + 1 THEN 'skip'
        WHEN next_rank < current_rank THEN 'backward'
    END AS transition_type

FROM journey_rank