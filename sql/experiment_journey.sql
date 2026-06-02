DROP TABLE IF EXISTS experiment_journey;

CREATE TABLE experiment_journey AS
SELECT
    d.*,
    c.variation,
    c.clnt_age,
    c.clnt_tenure_yr,
    c.bal
FROM digital_footprints d
INNER JOIN client_dimension c
    ON d.client_id = c.client_id
WHERE c.variation IS NOT NULL;