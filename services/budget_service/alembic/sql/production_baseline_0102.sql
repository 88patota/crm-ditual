BEGIN;

-- Garantir a tabela de controle de versão do Alembic
CREATE TABLE IF NOT EXISTS alembic_version (
    version_num VARCHAR(32) NOT NULL,
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);

-- Esquema de budgets (baseline)
CREATE TABLE IF NOT EXISTS budgets (
    id SERIAL NOT NULL,
    order_number VARCHAR NOT NULL,
    client_name VARCHAR NOT NULL,
    client_id INTEGER,
    total_purchase_value FLOAT,
    total_sale_value FLOAT,
    total_sale_with_icms FLOAT,
    total_commission FLOAT,
    commission_percentage_actual FLOAT,
    profitability_percentage FLOAT,
    total_ipi_value FLOAT,
    total_final_value FLOAT,
    total_weight_difference_percentage FLOAT,
    status VARCHAR NOT NULL,
    notes TEXT,
    created_by VARCHAR NOT NULL,
    prazo_medio INTEGER,
    outras_despesas_totais FLOAT,
    freight_type VARCHAR(10) NOT NULL,
    freight_value_total FLOAT,
    payment_condition VARCHAR(50),
    valor_frete_compra FLOAT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
    expires_at TIMESTAMP WITH TIME ZONE,
    PRIMARY KEY (id)
);

CREATE INDEX IF NOT EXISTS ix_budgets_id ON budgets (id);
CREATE UNIQUE INDEX IF NOT EXISTS ix_budgets_order_number ON budgets (order_number);

-- Esquema de budget_items (incluindo total_profitability no estado final)
CREATE TABLE IF NOT EXISTS budget_items (
    id SERIAL NOT NULL,
    budget_id INTEGER NOT NULL,
    description VARCHAR NOT NULL,
    weight FLOAT,
    delivery_time VARCHAR,
    purchase_value_with_icms FLOAT NOT NULL,
    purchase_icms_percentage FLOAT,
    purchase_other_expenses FLOAT,
    purchase_value_without_taxes FLOAT NOT NULL,
    purchase_value_with_weight_diff FLOAT,
    sale_weight FLOAT,
    sale_value_with_icms FLOAT NOT NULL,
    sale_icms_percentage FLOAT,
    sale_value_without_taxes FLOAT NOT NULL,
    weight_difference FLOAT,
    profitability FLOAT,
    total_profitability FLOAT DEFAULT 0 NOT NULL,
    total_purchase FLOAT NOT NULL,
    total_sale FLOAT NOT NULL,
    unit_value FLOAT NOT NULL,
    total_value FLOAT NOT NULL,
    commission_percentage FLOAT,
    commission_percentage_actual FLOAT,
    commission_value FLOAT,
    ipi_percentage FLOAT,
    ipi_value FLOAT,
    total_value_with_ipi FLOAT,
    weight_difference_display TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
    PRIMARY KEY (id)
);

-- Adicionar FK caso ainda não exista (ambiente parcialmente inicializado)
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 
        FROM information_schema.table_constraints tc
        WHERE tc.table_name = 'budget_items'
          AND tc.constraint_type = 'FOREIGN KEY'
          AND tc.constraint_name = 'fk_budget_items_budget_id'
    ) THEN
        ALTER TABLE budget_items 
        ADD CONSTRAINT fk_budget_items_budget_id 
        FOREIGN KEY (budget_id) REFERENCES budgets (id);
    END IF;
END$$;

CREATE INDEX IF NOT EXISTS ix_budget_items_id ON budget_items (id);

-- Caso esteja atualizando a partir da 0100, garantir coluna e popular
ALTER TABLE budget_items ADD COLUMN IF NOT EXISTS total_profitability FLOAT;

UPDATE budget_items
SET total_profitability = 
    CASE
        WHEN total_purchase > 0 THEN ((total_sale / total_purchase) - 1) * 100
        ELSE 0
    END
WHERE total_profitability IS NULL;

ALTER TABLE budget_items
    ALTER COLUMN total_profitability SET DEFAULT 0;

ALTER TABLE budget_items
    ALTER COLUMN total_profitability SET NOT NULL;

-- Fixar versão final do Alembic
DELETE FROM alembic_version;
INSERT INTO alembic_version (version_num) VALUES ('0102');

COMMIT;