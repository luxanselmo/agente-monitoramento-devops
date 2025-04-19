CREATE TABLE IF NOT EXISTS metrics (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP,
    host VARCHAR(100),
    rtt_ms FLOAT,
    loss_pct FLOAT,
    http_status INT,
    http_time_ms FLOAT
);