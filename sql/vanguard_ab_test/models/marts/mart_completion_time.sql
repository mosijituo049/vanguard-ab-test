WITH first_start AS (

    SELECT
        client_id,
        variation,
        MIN(date_time) AS first_start_time
    FROM {{ ref('int_journey_rank') }}
    WHERE process_step = 'start'
    GROUP BY
        client_id,
        variation

),

completion_confirm AS (

    SELECT
        s.client_id,
        MIN(j.date_time) AS completion_confirm_time
    FROM first_start s
    JOIN {{ ref('int_journey_rank') }} j
        ON s.client_id = j.client_id
    WHERE j.process_step = 'confirm'
      AND j.date_time > s.first_start_time
    GROUP BY s.client_id

),

calendar_time AS (

    SELECT
        s.client_id,
        s.variation,
        s.first_start_time,
        c.completion_confirm_time,

        TIMESTAMP_DIFF(
            c.completion_confirm_time,
            s.first_start_time,
            SECOND
        ) AS calendar_completion_time_sec

    FROM first_start s
    JOIN completion_confirm c
        ON s.client_id = c.client_id

),

active_time AS (

    SELECT
        d.client_id,

        -- SUM(d.duration_sec) AS active_completion_time_sec
        SUM(
            CASE
                WHEN duration_sec <= 1800
                THEN duration_sec
                ELSE 0
            END
        ) AS active_completion_time_sec

    FROM {{ ref('mart_duration') }} d
    JOIN first_start s
        ON d.client_id = s.client_id
    JOIN completion_confirm c
        ON d.client_id = c.client_id

    WHERE d.date_time >= s.first_start_time
      AND d.date_time < c.completion_confirm_time

    GROUP BY d.client_id

)

SELECT
    ct.client_id,
    ct.variation,
    ct.first_start_time,
    ct.completion_confirm_time,
    ct.calendar_completion_time_sec,
    acti.active_completion_time_sec
FROM calendar_time ct
LEFT JOIN active_time acti
    ON ct.client_id = acti.client_id
