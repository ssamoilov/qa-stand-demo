CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Тестовые данные для QA стенда
INSERT INTO users (name, email) VALUES 
('QA Test User 1', 'qa1@test.com'),
('QA Test User 2', 'qa2@test.com'),
('Auto Test User', 'auto@test.com')
ON CONFLICT (email) DO NOTHING;