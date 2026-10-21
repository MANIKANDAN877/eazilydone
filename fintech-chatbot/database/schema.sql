CREATE TABLE IF NOT EXISTS questions (
    id SERIAL PRIMARY KEY,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    category TEXT NOT NULL,
    keywords TEXT NOT NULL,
    source_url TEXT,
    last_verified_at DATE NOT NULL DEFAULT CURRENT_DATE
);

CREATE INDEX IF NOT EXISTS idx_questions_category
    ON questions (category);

CREATE INDEX IF NOT EXISTS idx_questions_keywords
    ON questions ((lower(keywords)));
