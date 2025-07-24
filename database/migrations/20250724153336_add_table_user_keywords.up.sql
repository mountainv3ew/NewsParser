CREATE TABLE 
    user_keywords (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid (),
        user_id BIGINT NOT NULL,
        keywords TEXT,
        UNIQUE (user_id)
    );