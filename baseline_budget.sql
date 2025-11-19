BEGIN;

CREATE TABLE alembic_version (
    version_num VARCHAR(32) NOT NULL, 
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);

-- Running upgrade  -> 0100

CREATE TABLE budgets (
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

CREATE INDEX ix_budgets_id ON budgets (id);

CREATE UNIQUE INDEX ix_budgets_order_number ON budgets (order_number);

CREATE TABLE budget_items (
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

ALTER TABLE budget_items ADD CONSTRAINT fk_budget_items_budget_id FOREIGN KEY(budget_id) REFERENCES budgets (id);

CREATE INDEX ix_budget_items_id ON budget_items (id);

INSERT INTO alembic_version (version_num) VALUES ('0100') RETURNING alembic_version.version_num;

COMMIT;

