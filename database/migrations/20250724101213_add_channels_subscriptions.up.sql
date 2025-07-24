CREATE TABLE
    channels_subscriptions (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid (),
        user_id BIGINT NOT NULL,
        channel VARCHAR(40) NOT NULL,
        UNIQUE (user_id, channel)
    );