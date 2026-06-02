DESCRIBE digital_footprints_1;
DESCRIBE digital_footprints_2;

SELECT COUNT(*) FROM digital_footprints_1;

SELECT COUNT(*) FROM digital_footprints_2;

SELECT COUNT(DISTINCT client_id)
FROM digital_footprints_1;

SELECT COUNT(DISTINCT client_id)
FROM digital_footprints_2;

SELECT COUNT(DISTINCT client_id)
FROM (
    SELECT client_id FROM digital_footprints_1
    UNION
    SELECT client_id FROM digital_footprints_2
) t;

DROP TABLE IF EXISTS digital_footprints;

CREATE TABLE digital_footprints AS
SELECT * FROM digital_footprints_1
UNION ALL
SELECT * FROM digital_footprints_2;

SELECT COUNT(*)
FROM digital_footprints;

ALTER TABLE digital_footprints
ADD COLUMN df_id BIGINT UNSIGNED
AUTO_INCREMENT PRIMARY KEY FIRST;

SELECT COUNT(*)
FROM digital_footprints d
LEFT JOIN client_dimension c
  ON d.client_id = c.client_id
WHERE c.client_id IS NULL;

SELECT COUNT(DISTINCT d.client_id)
FROM digital_footprints d
LEFT JOIN client_dimension c
  ON d.client_id = c.client_id
WHERE c.client_id IS NULL;

SELECT DISTINCT d.client_id
FROM digital_footprints d
LEFT JOIN client_dimension c
  ON d.client_id = c.client_id
WHERE c.client_id IS NULL
LIMIT 20;

SELECT COUNT(*)
FROM digital_footprints
WHERE client_id IS NULL;

SELECT COUNT(DISTINCT client_id)
FROM digital_footprints;

SELECT COUNT(DISTINCT d.client_id)
FROM digital_footprints d
INNER JOIN client_dimension c
ON d.client_id = c.client_id;