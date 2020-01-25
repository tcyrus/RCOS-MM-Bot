CREATE TABLE IF NOT EXISTS rcos_creds (
    uid TEXT NOT NULL,
    password bytea NOT NULL,
    PRIMARY KEY (uid)
);
CREATE EXTENSION IF NOT EXISTS pgcrypto;
