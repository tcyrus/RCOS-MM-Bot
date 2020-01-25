CREATE TABLE IF NOT EXISTS rcos_creds (
    uid TEXT NOT NULL,
    password bytea,
    PRIMARY KEY (uid)
);
CREATE EXTENSION IF NOT EXISTS pgcrypto;
