-- Script SQL para corrigir a coluna status
\echo 'Iniciando correção da coluna status...'

-- Verificar estrutura atual
\echo 'Estrutura atual da coluna status:'
SELECT column_name, data_type, udt_name 
FROM information_schema.columns 
WHERE table_name = 'budgets' AND column_name = 'status';

-- Verificar se enum existe
\echo 'Verificando se enum budgetstatus existe:'
SELECT typname FROM pg_type WHERE typname = 'budgetstatus';

-- Alterar coluna para VARCHAR se necessário
\echo 'Alterando coluna para VARCHAR...'
ALTER TABLE budgets ALTER COLUMN status DROP DEFAULT;
ALTER TABLE budgets ALTER COLUMN status TYPE VARCHAR(20);
ALTER TABLE budgets ALTER COLUMN status SET DEFAULT 'draft';

-- Dropar enum se existir
\echo 'Dropando enum budgetstatus...'
DROP TYPE IF EXISTS budgetstatus CASCADE;

-- Verificar status existentes
\echo 'Status existentes na tabela:'
SELECT DISTINCT status FROM budgets;

-- Corrigir status inválidos
\echo 'Corrigindo status inválidos...'
UPDATE budgets 
SET status = 'draft' 
WHERE status IS NULL 
   OR status NOT IN ('draft', 'pending', 'approved', 'rejected', 'expired');

-- Verificar resultado final
\echo 'Estrutura final da coluna:'
SELECT column_name, data_type, udt_name 
FROM information_schema.columns 
WHERE table_name = 'budgets' AND column_name = 'status';

\echo 'Correção concluída!'
