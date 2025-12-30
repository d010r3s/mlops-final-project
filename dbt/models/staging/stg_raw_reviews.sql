{{ config(materialized='view') }}

select
  id,
  ts,
  text
from {{ source('sentiment', 'raw_reviews') }}
