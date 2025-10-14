-- Initialize CRM Ditual Database
-- This script runs automatically when PostgreSQL container starts

-- Set timezone
SET timezone = 'America/Sao_Paulo';

-- Create user first (if not exists) - Using environment variable password
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'crm_user') THEN
        -- Password will be set by POSTGRES_PASSWORD environment variable
        CREATE USER crm_user;
        RAISE NOTICE 'User crm_user created successfully';
    ELSE
        RAISE NOTICE 'User crm_user already exists';
        -- Update password to match environment variable
        ALTER USER crm_user WITH PASSWORD 'crm_strong_password_2024';
        RAISE NOTICE 'User crm_user password updated';
    END IF;
END
$$;

-- Ensure user has correct password (matching .env.prod)
ALTER USER crm_user WITH PASSWORD 'crm_strong_password_2024';

-- Create main database (if not exists)
SELECT 'CREATE DATABASE crm_ditual OWNER crm_user'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'crm_ditual')\gexec

-- Create additional databases if needed
SELECT 'CREATE DATABASE crm_test OWNER crm_user'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'crm_test')\gexec

-- Connect to crm_ditual to create extensions
\c crm_ditual;

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Grant permissions - Use correct database name from .env.prod
GRANT ALL PRIVILEGES ON DATABASE crm_ditual TO crm_user;
GRANT ALL PRIVILEGES ON DATABASE crm_test TO crm_user;

-- Grant schema permissions
GRANT ALL PRIVILEGES ON SCHEMA public TO crm_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO crm_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO crm_user;

-- Set default search path
ALTER DATABASE crm_ditual SET search_path TO public;

-- Log the initialization
DO $$
BEGIN
    RAISE NOTICE 'CRM Ditual Database initialized successfully at %', NOW();
    RAISE NOTICE 'Database crm_ditual created with owner crm_user';
    RAISE NOTICE 'Extensions uuid-ossp and pg_trgm installed';
END
$$;