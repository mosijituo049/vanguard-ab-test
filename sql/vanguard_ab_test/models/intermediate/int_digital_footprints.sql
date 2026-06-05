SELECT * FROM {{ ref('stg_digital_footprints1') }}

UNION DISTINCT

SELECT * FROM {{ ref('stg_digital_footprints2') }}