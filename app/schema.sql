-- User Table: one account per user
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,   -- Unique identifier for each user
    full_name TEXT NOT NULL,                -- Full name of user
    username TEXT NOT NULL UNIQUE,          -- Unique username for user
    email TEXT NOT NULL UNIQUE,             -- Unique email address for user
    password_hash TEXT NOT NULL             -- Scrambled password for user
);

-- Subscriptions Table: one row per subscription associated to user
CREATE TABLE IF NOT EXISTS subscriptions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,   -- Unique identifier for each subscription
    user_id INTEGER NOT NULL,               -- Identifier of user who owns subscription
    name TEXT NOT NULL,                     -- Name of subscription
    price REAL NOT NULL,                    -- Cost per billing cycle of subscription
    billing_cycle TEXT NOT NULL,            -- Billing cycle of subscription
    category TEXT NOT NULL,                 -- Category of subscription
    next_billing_date TEXT NOT NULL,        -- Next billing date of subscription
    cancellation_url TEXT,                  -- URL to cancel subscription

    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE    -- Ensures that if a user is deleted, all their subscriptions are also deleted
);