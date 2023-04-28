CREATE TABLE IF NOT EXISTS api_keys (
    id SERIAL PRIMARY KEY, 
    binance_key TEXT NOT NULL UNIQUE,
    binance_secret TEXT NOT NULL UNIQUE, 
    name TEXT NOT NULL
);
