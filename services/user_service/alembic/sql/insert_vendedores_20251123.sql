BEGIN;
CREATE EXTENSION IF NOT EXISTS pgcrypto;

INSERT INTO users (email, username, full_name, hashed_password, role, is_active, created_at, updated_at)
VALUES ('aline@ditualsp.com.br', 'aline', 'Aline Andrade', crypt('ditual102030', gen_salt('bf', 12)), 'vendas', TRUE, now(), now())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (email, username, full_name, hashed_password, role, is_active, created_at, updated_at)
VALUES ('adriana@ditualsp.com.br', 'adriana', 'Adriana Andrade', crypt('ditual102030', gen_salt('bf', 12)), 'vendas', TRUE, now(), now())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (email, username, full_name, hashed_password, role, is_active, created_at, updated_at)
VALUES ('aldo@ditualsp.com.br', 'aldo', 'Aldo Medeiros', crypt('ditual102030', gen_salt('bf', 12)), 'vendas', TRUE, now(), now())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (email, username, full_name, hashed_password, role, is_active, created_at, updated_at)
VALUES ('laura@ditualsp.com.br', 'laura', 'Laura Garcia', crypt('ditual102030', gen_salt('bf', 12)), 'vendas', TRUE, now(), now())
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (email, username, full_name, hashed_password, role, is_active, created_at, updated_at)
VALUES ('luciana@ditualsp.com.br', 'luciana', 'Luciana Lucas', crypt('ditual102030', gen_salt('bf', 12)), 'vendas', TRUE, now(), now())
ON CONFLICT (email) DO NOTHING;

COMMIT;

