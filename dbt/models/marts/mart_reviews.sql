{{ config(materialized='table') }}

select
  id,
  ts,
  text
from {{ ref('stg_raw_reviews') }}
