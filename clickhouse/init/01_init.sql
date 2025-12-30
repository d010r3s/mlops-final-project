CREATE DATABASE IF NOT EXISTS sentiment;

CREATE TABLE IF NOT EXISTS sentiment.predictions
(
  ts DateTime DEFAULT now(),
  text String,
  label String,
  score Float32
)
ENGINE = MergeTree
ORDER BY ts;
