-- Users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    company_description TEXT DEFAULT ''
);

-- Projects table
CREATE TABLE IF NOT EXISTS projects (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(150) NOT NULL,
    description TEXT,
    current_step NUMERIC DEFAULT 0,
    risk_score_threshold NUMERIC DEFAULT 0.1
);

-- Risks table
CREATE TYPE risk_type AS ENUM ('threat', 'opportunity');

CREATE TABLE IF NOT EXISTS risks (
    id SERIAL PRIMARY KEY,
    project_id INT NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    kind risk_type NOT NULL,
    probability NUMERIC,
    impact NUMERIC,
    contingency TEXT,
    fallback TEXT
);
