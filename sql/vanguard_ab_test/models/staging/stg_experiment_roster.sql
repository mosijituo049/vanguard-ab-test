select
    client_id,
    Variation as variation
from {{ source('raw','df_final_experiment_clients') }}