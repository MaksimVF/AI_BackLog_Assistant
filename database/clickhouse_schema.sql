

-- ClickHouse schema for logs and metrics storage

-- Create database
CREATE DATABASE IF NOT EXISTS ai_backlog_admin;

-- Logs table
CREATE TABLE IF NOT EXISTS ai_backlog_admin.logs
(
    timestamp DateTime64(3, 'UTC') CODEC(Delta, ZSTD(1)),
    level LowCardinality(String) CODEC(ZSTD(1)),
    source LowCardinality(String) CODEC(ZSTD(1)),
    message String CODEC(ZSTD(1)),
    metadata Map(String, String) CODEC(ZSTD(1)),
    agent_id LowCardinality(String) CODEC(ZSTD(1)),
    session_id UUID CODEC(ZSTD(1))
)
ENGINE = MergeTree()
PARTITION BY toYYYYMM(timestamp)
ORDER BY (timestamp, level)
TTL timestamp + INTERVAL 6 MONTH
SETTINGS index_granularity = 8192;

-- Metrics table
CREATE TABLE IF NOT EXISTS ai_backlog_admin.metrics
(
    timestamp DateTime64(3, 'UTC') CODEC(Delta, ZSTD(1)),
    metric_name LowCardinality(String) CODEC(ZSTD(1)),
    value Float64 CODEC(ZSTD(1)),
    tags Map(String, String) CODEC(ZSTD(1)),
    agent_id LowCardinality(String) CODEC(ZSTD(1)),
    session_id UUID CODEC(ZSTD(1))
)
ENGINE = MergeTree()
PARTITION BY toYYYYMM(timestamp)
ORDER BY (timestamp, metric_name)
TTL timestamp + INTERVAL 2 YEAR
SETTINGS index_granularity = 8192;

-- Events table
CREATE TABLE IF NOT EXISTS ai_backlog_admin.events
(
    timestamp DateTime64(3, 'UTC') CODEC(Delta, ZSTD(1)),
    event_type LowCardinality(String) CODEC(ZSTD(1)),
    source LowCardinality(String) CODEC(ZSTD(1)),
    details String CODEC(ZSTD(1)),
    metadata Map(String, String) CODEC(ZSTD(1)),
    agent_id LowCardinality(String) CODEC(ZSTD(1)),
    session_id UUID CODEC(ZSTD(1))
)
ENGINE = MergeTree()
PARTITION BY toYYYYMM(timestamp)
ORDER BY (timestamp, event_type)
TTL timestamp + INTERVAL 1 YEAR
SETTINGS index_granularity = 8192;

-- Materialized view for common log queries
CREATE MATERIALIZED VIEW IF NOT EXISTS ai_backlog_admin.logs_by_level
ENGINE = AggregatingMergeTree()
PARTITION BY toYYYYMM(timestamp)
ORDER BY (timestamp, level)
POPULATE AS
SELECT
    toStartOfMinute(timestamp) AS minute,
    level,
    count() AS count
FROM ai_backlog_admin.logs
GROUP BY minute, level;

-- Materialized view for metrics aggregations
CREATE MATERIALIZED VIEW IF NOT EXISTS ai_backlog_admin.metrics_hourly
ENGINE = AggregatingMergeTree()
PARTITION BY toYYYYMM(timestamp)
ORDER BY (timestamp, metric_name)
POPULATE AS
SELECT
    toStartOfHour(timestamp) AS hour,
    metric_name,
    avg(value) AS avg_value,
    max(value) AS max_value,
    min(value) AS min_value
FROM ai_backlog_admin.metrics
GROUP BY hour, metric_name;

