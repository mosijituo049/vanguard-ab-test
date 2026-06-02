USE vanguard_ab_test;

SELECT * FROM client_profiles;

-- clean column name
ALTER TABLE experiment_roster
RENAME COLUMN Variation TO variation;

SHOW TABLES;

-- check duplicates
SELECT count(*)
FROM client_profiles
GROUP BY client_id
HAVING COUNT(*) > 1;

SELECT count(*)
FROM digital_footprints_1
GROUP BY client_id
HAVING COUNT(*) > 1;

SELECT count(*)
FROM digital_footprints_1
GROUP BY visitor_id
HAVING COUNT(*) > 1;

-- check null 
SELECT COUNT(*)
FROM client_profiles
WHERE client_id IS NULL;

SELECT COUNT(*) total_rows,
       COUNT(DISTINCT client_id) unique_clients
FROM experiment_roster;

DROP TABLE IF EXISTS client_dimension;
CREATE TABLE client_dimension AS
SELECT
    cp.*,
    er.variation
FROM client_profiles cp
LEFT JOIN experiment_roster er
    ON cp.client_id = er.client_id;
    
SHOW CREATE TABLE client_dimension;

SELECT COUNT(*) AS total_rows,
       COUNT(DISTINCT client_id) AS unique_clients
FROM client_dimension;

ALTER TABLE client_dimension
ADD PRIMARY KEY (client_id);

SELECT variation, COUNT(*)
FROM client_dimension
GROUP BY variation;
