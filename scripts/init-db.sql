-- Initialize CRM Ditual Database
-- This script runs automatically when PostgreSQL container starts

-- Set timezone
SET timezone = 'America/Sao_Paulo';

-- Create user first (if not exists)
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'crm_user') THEN
        CREATE USER crm_user WITH PASSWORD 'crm_password';
        RAISE NOTICE 'User crm_user created successfully';
    ELSE
        RAISE NOTICE 'User crm_user already exists';
    END IF;
END
$$;

-- Create main database
CREATE DATABASE crm_ditual OWNER crm_user;

-- Create additional databases if needed
CREATE DATABASE crm_test OWNER crm_user;

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