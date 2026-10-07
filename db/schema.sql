CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(120) NOT NULL,
    priority VARCHAR(10) NOT NULL CHECK (priority IN ('low', 'medium', 'high')) DEFAULT 'medium',
    done BOOLEAN DEFAULT FALSE, 
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    CONSTRAINT title_not_empty CHECK (length(trim(title))>0)
);