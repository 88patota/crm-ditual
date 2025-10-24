--
-- PostgreSQL database dump
--

\restrict wxlohkN8JhoFqcluffhVDacY5XgFTkIcMmJeTeNeUUsGmn3BHg38KYP7yh3pudd

-- Dumped from database version 14.19 (Debian 14.19-1.pgdg13+1)
-- Dumped by pg_dump version 14.19 (Debian 14.19-1.pgdg13+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: userrole; Type: TYPE; Schema: public; Owner: crm_user
--

CREATE TYPE public.userrole AS ENUM (
    'ADMIN',
    'VENDAS'
);


ALTER TYPE public.userrole OWNER TO crm_user;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: crm_user
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO crm_user;

--
-- Name: budget_items; Type: TABLE; Schema: public; Owner: crm_user
--

CREATE TABLE public.budget_items (
    id integer NOT NULL,
    budget_id integer NOT NULL,
    description character varying NOT NULL,
    weight double precision,
    delivery_time character varying,
    purchase_value_with_icms double precision NOT NULL,
    purchase_icms_percentage double precision,
    purchase_other_expenses double precision,
    purchase_value_without_taxes double precision NOT NULL,
    purchase_value_with_weight_diff double precision,
    sale_weight double precision,
    sale_value_with_icms double precision NOT NULL,
    sale_icms_percentage double precision,
    sale_value_without_taxes double precision NOT NULL,
    weight_difference double precision,
    profitability double precision,
    total_purchase double precision NOT NULL,
    total_sale double precision NOT NULL,
    unit_value double precision NOT NULL,
    total_value double precision NOT NULL,
    commission_percentage double precision,
    commission_percentage_actual double precision,
    commission_value double precision,
    dunamis_cost double precision,
    ipi_percentage double precision,
    ipi_value double precision,
    total_value_with_ipi double precision,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now(),
    weight_difference_display text
);


ALTER TABLE public.budget_items OWNER TO crm_user;

--
-- Name: budget_items_id_seq; Type: SEQUENCE; Schema: public; Owner: crm_user
--

CREATE SEQUENCE public.budget_items_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.budget_items_id_seq OWNER TO crm_user;

--
-- Name: budget_items_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: crm_user
--

ALTER SEQUENCE public.budget_items_id_seq OWNED BY public.budget_items.id;


--
-- Name: budgets; Type: TABLE; Schema: public; Owner: crm_user
--

CREATE TABLE public.budgets (
    id integer NOT NULL,
    order_number character varying NOT NULL,
    client_name character varying NOT NULL,
    client_id integer,
    total_purchase_value double precision,
    total_sale_value double precision,
    total_sale_with_icms double precision,
    total_commission double precision,
    markup_percentage double precision,
    profitability_percentage double precision,
    total_ipi_value double precision,
    total_final_value double precision,
    status character varying NOT NULL,
    notes text,
    created_by character varying NOT NULL,
    prazo_medio integer,
    outras_despesas_totais double precision,
    freight_type character varying(10) NOT NULL,
    payment_condition character varying(50),
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now(),
    expires_at timestamp with time zone,
    freight_value_total double precision,
    valor_frete_compra double precision
);


ALTER TABLE public.budgets OWNER TO crm_user;

--
-- Name: COLUMN budgets.prazo_medio; Type: COMMENT; Schema: public; Owner: crm_user
--

COMMENT ON COLUMN public.budgets.prazo_medio IS 'Prazo médio em dias';


--
-- Name: COLUMN budgets.outras_despesas_totais; Type: COMMENT; Schema: public; Owner: crm_user
--

COMMENT ON COLUMN public.budgets.outras_despesas_totais IS 'Outras despesas do pedido';


--
-- Name: COLUMN budgets.payment_condition; Type: COMMENT; Schema: public; Owner: crm_user
--

COMMENT ON COLUMN public.budgets.payment_condition IS 'Condições de pagamento';


--
-- Name: budgets_id_seq; Type: SEQUENCE; Schema: public; Owner: crm_user
--

CREATE SEQUENCE public.budgets_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.budgets_id_seq OWNER TO crm_user;

--
-- Name: budgets_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: crm_user
--

ALTER SEQUENCE public.budgets_id_seq OWNED BY public.budgets.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: crm_user
--

CREATE TABLE public.users (
    id integer NOT NULL,
    email character varying NOT NULL,
    username character varying NOT NULL,
    full_name character varying NOT NULL,
    hashed_password character varying NOT NULL,
    role public.userrole NOT NULL,
    is_active boolean,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.users OWNER TO crm_user;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: crm_user
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO crm_user;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: crm_user
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: budget_items id; Type: DEFAULT; Schema: public; Owner: crm_user
--

ALTER TABLE ONLY public.budget_items ALTER COLUMN id SET DEFAULT nextval('public.budget_items_id_seq'::regclass);


--
-- Name: budgets id; Type: DEFAULT; Schema: public; Owner: crm_user
--

ALTER TABLE ONLY public.budgets ALTER COLUMN id SET DEFAULT nextval('public.budgets_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: crm_user
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: crm_user
--

COPY public.alembic_version (version_num) FROM stdin;
1f4f4176aeb7
\.


--
-- Data for Name: budget_items; Type: TABLE DATA; Schema: public; Owner: crm_user
--

COPY public.budget_items (id, budget_id, description, weight, delivery_time, purchase_value_with_icms, purchase_icms_percentage, purchase_other_expenses, purchase_value_without_taxes, purchase_value_with_weight_diff, sale_weight, sale_value_with_icms, sale_icms_percentage, sale_value_without_taxes, weight_difference, profitability, total_purchase, total_sale, unit_value, total_value, commission_percentage, commission_percentage_actual, commission_value, dunamis_cost, ipi_percentage, ipi_value, total_value_with_ipi, created_at, updated_at, weight_difference_display) FROM stdin;
1	1	Teste	1000	1	3.22	0.12	0	2.571492	2.571492	1000	5.55	0.18	4.130033	0	60.608399999999996	2571.492	4130.033	0.00413	4130.033	0	0.04	222	\N	0.05	277.5	5827.5	2025-10-16 19:40:37.385777+00	2025-10-16 19:40:37.385777+00	\N
2	2	teste	1000	0	6.9	0.18	0	5.134635	5.134635	1000	9.3	0.18	6.920595	0	34.7826	5134.635	6920.595	0.006921	6920.595	0	0.015	139.5	\N	0.05	465	9765	2025-10-16 20:24:24.265289+00	2025-10-16 20:24:24.265289+00	\N
4	3	item	300	1	2.11	0.15	0	1.627601	1.627601	300	5	0.18	3.72075	0	128.6033	488.2803	1116.225	0.012403	1116.225	0	0.05	75	\N	0.0325	48.75	1548.75	2025-10-22 02:33:20.527311+00	2025-10-22 02:33:20.527311+00	\N
5	4	item	100	1	2.11	0.12	0	1.685046	1.685046	100	4.5	0.18	3.348675	0	98.729	168.5046	334.8675	0.033487	334.8675	0	0.05	22.5	\N	0.0325	14.63	464.63	2025-10-23 01:54:03.336562+00	2025-10-23 01:54:03.336562+00	\N
41	5	teste	1000	0	3.11	0.18	0	2.664307	2.537435	1050	5.33	0.18	3.96632	50	48.8687	2664.307	4164.636	0.003777	4164.636	0	0.03	167.89	\N	0.0325	181.89	5778.39	2025-10-23 14:08:52.005697+00	2025-10-23 14:08:52.005697+00	\N
42	6	item	100	0	2.11	0.18	0	2.120157	1.413438	150	5.33	0.18	3.96632	50	87.0767	212.0157	594.948	0.026442	594.948	0	0.05	39.98	\N	0.0325	25.98	825.48	2025-10-23 14:34:18.377716+00	2025-10-23 14:34:18.377716+00	\N
43	7	Item com diferença de peso	10	15	1000	0.18	0.5	749.65	624.708333	12	1500	0.17	1129.8375	2	50.7153	7496.5	13558.05	94.153125	13558.05	0	0.05	900	\N	0	0	18000	2025-10-23 15:40:22.335807+00	2025-10-23 15:40:22.335807+00	\N
45	9	Item com diferença de peso	10	15	1000	0.18	0.5	749.65	624.708333	12	1500	0.17	1129.8375	2	50.7153	7496.5	13558.05	94.153125	13558.05	0	0.05	900	\N	0	0	18000	2025-10-23 15:54:41.116896+00	2025-10-23 15:54:41.116896+00	\N
47	11	Item com diferença de peso	10	15	1000	0.18	0.5	749.65	624.708333	12	1500	0.17	1129.8375	2	50.7153	7496.5	13558.05	94.153125	13558.05	0	0.05	900	\N	0	0	18000	2025-10-23 17:00:35.116778+00	2025-10-23 17:00:35.116778+00	\N
49	13	Item com diferença de peso	10	15	1000	0.18	0.5	749.65	624.708333	12	1500	0.17	1129.8375	2	50.7153	7496.5	13558.05	94.153125	13558.05	0	0.05	900	\N	0	0	18000	2025-10-23 17:01:45.91385+00	2025-10-23 17:01:45.91385+00	\N
59	23	item	100	0	3.11	0.18	0	2.314307	1.542871	150	7.11	0.18	5.290907	50	128.6173	231.4307	793.63605	0.035273	793.63605	0	0.05	53.33	\N	0	0	1066.5	2025-10-23 19:02:04.932511+00	2025-10-23 19:02:04.932511+00	\N
60	24	item	100	0	3.11	0.18	0	2.314307	1.780236	130	8.11	0.18	6.035057	30	160.7717	231.4307	784.55741	0.046424	784.55741	0	0.05	52.72	\N	0	0	1054.3	2025-10-23 19:03:21.751459+00	2025-10-23 19:37:46.325587+00	{"has_difference": true, "absolute_difference": 30.0, "percentage_difference": 30.0, "formatted_display": "Diferen\\u00e7a de Peso: 30.00 kg (30.0%)"}
67	25	item	120	2	2.33	0.15	0	2.630637	2.391488	132	7.33	0.18	5.45462	12	128.0848	315.67644	720.00984	0.041323	720.00984	0	0.05	48.38	\N	0.0325	31.45	999.24	2025-10-24 02:18:32.14324+00	2025-10-24 02:18:32.14324+00	{"has_difference": true, "absolute_difference": 12.0, "percentage_difference": 10.0, "formatted_display": "10.0%"}
\.


--
-- Data for Name: budgets; Type: TABLE DATA; Schema: public; Owner: crm_user
--

COPY public.budgets (id, order_number, client_name, client_id, total_purchase_value, total_sale_value, total_sale_with_icms, total_commission, markup_percentage, profitability_percentage, total_ipi_value, total_final_value, status, notes, created_by, prazo_medio, outras_despesas_totais, freight_type, payment_condition, created_at, updated_at, expires_at, freight_value_total, valor_frete_compra) FROM stdin;
1	PED-0001	Cliente Teste	\N	2571.492	4130.033	5550	222	60.60843276976946	60.60843276976946	277.5	5827.5	draft	\N	admin	\N	\N	FOB	À vista	2025-10-16 19:40:37.385777+00	2025-10-16 19:40:37.385777+00	\N	\N	\N
2	PED-0002	Cliente Teste	\N	5134.635	6920.595	9300	139.5	34.78260869565217	34.78260869565217	465	9765	draft	\N	admin	\N	\N	FOB	À vista	2025-10-16 20:24:24.265289+00	2025-10-16 20:24:24.265289+00	\N	\N	\N
3	PED-0003	Cliente Teste	\N	488.2803	1116.225	1500	75	128.60332477062863	128.60332477062863	48.75	1548.75	draft	\N	epatekoski	\N	\N	FOB	À vista	2025-10-20 01:41:54.218949+00	2025-10-20 01:41:54.218949+00	\N	\N	\N
4	PED-0004	Cliente Teste	\N	168.5046	334.8675	450	22.5	98.72899612236104	98.72899612236104	14.63	464.63	draft	\N	admin	\N	\N	CIF	7	2025-10-23 01:54:03.336562+00	2025-10-23 01:54:03.336562+00	\N	\N	0
5	PED-0005	teste	\N	3014.307	4164.636	5596.5	167.89	38.16230397235585	38.16230397235585	181.89	6128.39	pending	\N	admin	\N	\N	FOB	À vista	2025-10-23 03:32:23.79126+00	2025-10-23 14:08:52.005697+00	\N	350	0.35
6	PED-0006	teste	\N	267.01570000000004	594.948	799.5	39.98	122.81386450309846	122.81386450309846	25.98	880.48	draft	\N	admin	\N	\N	FOB	À vista	2025-10-23 14:34:18.377716+00	2025-10-23 14:34:18.377716+00	\N	55	0.55
7	TEST-WD-20251023124022	Cliente Teste Diferença Peso	\N	7546.5	13558.05	18000	900	79.66010733452593	79.66010733452593	0	18050	draft	Teste para verificar exibição de diferença de peso	admin	15	100	FOB	30 dias	2025-10-23 15:40:22.335807+00	2025-10-23 15:40:22.335807+00	\N	50	5
9	TEST-WD-20251023125441	Cliente Teste Diferença Peso	\N	7546.5	13558.05	18000	900	79.66010733452593	79.66010733452593	0	18050	draft	Teste para verificar exibição de diferença de peso	admin	15	100	FOB	30 dias	2025-10-23 15:54:41.116896+00	2025-10-23 15:54:41.116896+00	\N	50	5
11	TEST-WD-20251023140035	Cliente Teste Diferença Peso	\N	7546.5	13558.05	18000	900	79.66010733452593	79.66010733452593	0	18050	draft	Teste para verificar exibição de diferença de peso	admin	15	100	FOB	30 dias	2025-10-23 17:00:35.116778+00	2025-10-23 17:00:35.116778+00	\N	50	5
13	TEST-WD-20251023140145	Cliente Teste Diferença Peso	\N	7546.5	13558.05	18000	900	79.66010733452593	79.66010733452593	0	18050	draft	Teste para verificar exibição de diferença de peso	admin	15	100	FOB	30 dias	2025-10-23 17:01:45.91385+00	2025-10-23 17:01:45.91385+00	\N	50	5
23	PED-0007	Cliente Teste	\N	231.4307	793.63605	1066.5	53.33	242.92600333490756	242.92600333490756	0	1066.5	draft	\N	admin	\N	\N	FOB	À vista	2025-10-23 19:02:04.932511+00	2025-10-23 19:02:04.932511+00	\N	\N	0
24	PED-0008	Cliente Teste	\N	231.4307	784.55741	1054.3	52.72	239.00317027948321	239.00317027948321	0	1054.3	draft	\N	admin	\N	\N	FOB	À vista	2025-10-23 19:03:21.751459+00	2025-10-23 19:03:21.751459+00	\N	\N	0
25	PED-0009	Cliente Teste 2	\N	415.67644	720.00984	967.56	48.38	73.21401232169906	73.21401232169906	31.45	1099.24	draft	\N	admin	\N	\N	FOB	À vista	2025-10-23 20:36:51.705579+00	2025-10-24 02:18:32.14324+00	\N	100	0.833333
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: crm_user
--

COPY public.users (id, email, username, full_name, hashed_password, role, is_active, created_at, updated_at) FROM stdin;
1	admin@crmditual.com	admin	Administrador do Sistema	$2b$12$BNCPs2EYvM1/lxq7inY6LOSl9dNvUCrkbK1k1p7.xyffQNAWd1Xve	ADMIN	t	2025-10-16 17:51:37.938886+00	2025-10-16 17:51:37.938886+00
2	ep@loen.digital	epatekoski	Erik Patekoski	$2b$12$eEqN8MbUir4Y/w27gb7vFundxg4Qab0RcojhLBwl/DWhSJtYHLt6e	VENDAS	t	2025-10-20 01:40:06.775984+00	2025-10-20 01:42:20.512553+00
\.


--
-- Name: budget_items_id_seq; Type: SEQUENCE SET; Schema: public; Owner: crm_user
--

SELECT pg_catalog.setval('public.budget_items_id_seq', 67, true);


--
-- Name: budgets_id_seq; Type: SEQUENCE SET; Schema: public; Owner: crm_user
--

SELECT pg_catalog.setval('public.budgets_id_seq', 25, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: crm_user
--

SELECT pg_catalog.setval('public.users_id_seq', 2, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: crm_user
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: budget_items budget_items_pkey; Type: CONSTRAINT; Schema: public; Owner: crm_user
--

ALTER TABLE ONLY public.budget_items
    ADD CONSTRAINT budget_items_pkey PRIMARY KEY (id);


--
-- Name: budgets budgets_pkey; Type: CONSTRAINT; Schema: public; Owner: crm_user
--

ALTER TABLE ONLY public.budgets
    ADD CONSTRAINT budgets_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: crm_user
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: ix_budget_items_id; Type: INDEX; Schema: public; Owner: crm_user
--

CREATE INDEX ix_budget_items_id ON public.budget_items USING btree (id);


--
-- Name: ix_budgets_id; Type: INDEX; Schema: public; Owner: crm_user
--

CREATE INDEX ix_budgets_id ON public.budgets USING btree (id);


--
-- Name: ix_budgets_order_number; Type: INDEX; Schema: public; Owner: crm_user
--

CREATE UNIQUE INDEX ix_budgets_order_number ON public.budgets USING btree (order_number);


--
-- Name: ix_users_email; Type: INDEX; Schema: public; Owner: crm_user
--

CREATE UNIQUE INDEX ix_users_email ON public.users USING btree (email);


--
-- Name: ix_users_id; Type: INDEX; Schema: public; Owner: crm_user
--

CREATE INDEX ix_users_id ON public.users USING btree (id);


--
-- Name: ix_users_username; Type: INDEX; Schema: public; Owner: crm_user
--

CREATE UNIQUE INDEX ix_users_username ON public.users USING btree (username);


--
-- Name: budget_items budget_items_budget_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: crm_user
--

ALTER TABLE ONLY public.budget_items
    ADD CONSTRAINT budget_items_budget_id_fkey FOREIGN KEY (budget_id) REFERENCES public.budgets(id);


--
-- PostgreSQL database dump complete
--

\unrestrict wxlohkN8JhoFqcluffhVDacY5XgFTkIcMmJeTeNeUUsGmn3BHg38KYP7yh3pudd

