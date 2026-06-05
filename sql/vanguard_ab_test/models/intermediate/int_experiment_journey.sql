SELECT
    d.*,
    c.variation,
    c.clnt_age,
    c.clnt_tenure_yr,
    c.bal
FROM {{ ref('int_digital_footprints') }} d
INNER JOIN {{ ref('int_client_dimension') }} c
    ON d.client_id = c.client_id
WHERE c.variation IS NOT NULL
  AND c.variation NOT IN ('NA', '')