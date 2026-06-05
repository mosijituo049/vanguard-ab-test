SELECT
    cp.*,
    er.variation
FROM {{ ref('stg_client_profiles') }} cp
LEFT JOIN {{ ref('stg_experiment_roster') }} er
    ON cp.client_id = er.client_id