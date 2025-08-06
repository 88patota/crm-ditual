-- Initialize CRM Ditual Database
-- This script runs automatically when PostgreSQL container starts

-- Set timezone
SET timezone = 'America/Sao_Paulo';

-- Create additional databases if needed
CREATE DATABASE IF NOT EXISTS crm_test;

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE crm_db TO crm_user;
GRANT ALL PRIVILEGES ON DATABASE crm_test TO crm_user;

-- Set default search path
ALTER DATABASE crm_db SET search_path TO public;

-- Log the initialization
DO $$
BEGIN
    RAISE NOTICE 'CRM Ditual Database initialized successfully at %', NOW();
END
$$;