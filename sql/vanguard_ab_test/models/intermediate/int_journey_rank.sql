WITH base AS (

    SELECT
        ej.*,

        CASE process_step
            WHEN 'start' THEN 1
            WHEN 'step_1' THEN 2
            WHEN 'step_2' THEN 3
            WHEN 'step_3' THEN 4
            WHEN 'confirm' THEN 5
        END AS step_rank

    FROM {{ ref('int_experiment_journey') }} ej

)

-- journey AS (

    SELECT
        *,

        ROW_NUMBER() OVER (
            -- PARTITION BY client_id, visitor_id, visit_id
            PARTITION BY client_id
            ORDER BY date_time, step_rank
        ) AS visit_seq,

        /*CASE LEAD(process_step) OVER (
            -- PARTITION BY client_id, visitor_id, visit_id
            PARTITION BY client_id
            ORDER BY date_time, step_rank
        )
            WHEN 'start' THEN 1
            WHEN 'step_1' THEN 2
            WHEN 'step_2' THEN 3
            WHEN 'step_3' THEN 4
            WHEN 'confirm' THEN 5
        END AS next_rank,*/

        LEAD(step_rank) OVER (
            -- PARTITION BY client_id, visitor_id, visit_id
            PARTITION BY client_id
            ORDER BY date_time, step_rank
        ) AS next_rank,

        /*LEAD(process_step) OVER (
            PARTITION BY client_id, visitor_id, visit_id
            ORDER BY date_time, step_rank
        ) AS next_step,*/

        LEAD(date_time) OVER (
            PARTITION BY client_id, visitor_id, visit_id
            -- PARTITION BY client_id
            ORDER BY date_time, step_rank
        ) AS next_time

    FROM base
-- )

-- journey_rank AS (

    /*SELECT
        *,
        
        --move duration_sec to mart duration
        TIMESTAMP_DIFF(
            next_time,
            date_time,
            SECOND
        ) AS duration_sec,*/

        -- step_rank AS current_rank,

        /*CASE next_step
            WHEN 'start' THEN 1
            WHEN 'step_1' THEN 2
            WHEN 'step_2' THEN 3
            WHEN 'step_3' THEN 4
            WHEN 'confirm' THEN 5
        END AS next_rank*/

    -- FROM journey

-- )

-- move to mart_transition
/*SELECT
    *,

    next_rank - current_rank AS step_diff,

    CASE
        WHEN next_step IS NULL THEN 'end'
        WHEN next_rank = current_rank THEN 'same_step'
        WHEN next_rank = current_rank + 1 THEN 'forward'
        WHEN next_rank > current_rank + 1 THEN 'skip'
        WHEN next_rank < current_rank THEN 'backward'
    END AS transition_type

FROM journey_rank*/