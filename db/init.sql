-- Initial SQL script to set up the database schema

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    telegram_id BIGINT UNIQUE NOT NULL,
    username VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE dreams (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    text TEXT NOT NULL,
    analysis TEXT,
    emotions JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE classifications (
    id SERIAL PRIMARY KEY,
    dream_id INTEGER REFERENCES dreams(id) ON DELETE CASCADE,
    emotion VARCHAR(50),
    intensity INTEGER,
    symbol VARCHAR(255)
);

CREATE TABLE chat_histories (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    message TEXT,
    response TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- INDEXES FOR PERFORMANCE OPTIMIZATION
CREATE INDEX idx_dreams_user_id ON dreams(user_id);
CREATE INDEX idx_classifications_dream_id ON classifications(dream_id);
CREATE INDEX idx_chat_histories_user_id ON chat_histories(user_id);
