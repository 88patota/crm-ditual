--
-- PostgreSQL database dump
--

\restrict uR4e1xqCCwGeLEFXQosCRL63n4ea2OIN7POrmNfI5Y6d50f6OoULUI8hocByHR8

-- Dumped from database version 14.20 (Debian 14.20-1.pgdg13+1)
-- Dumped by pg_dump version 14.20 (Debian 14.20-1.pgdg13+1)

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
-- Name: pg_trgm; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS pg_trgm WITH SCHEMA public;


--
-- Name: EXTENSION pg_trgm; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION pg_trgm IS 'text similarity measurement and index searching based on trigrams';


--
-- Name: pgcrypto; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS pgcrypto WITH SCHEMA public;


--
-- Name: EXTENSION pgcrypto; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION pgcrypto IS 'cryptographic functions';


--
-- Name: uuid-ossp; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA public;


--
-- Name: EXTENSION "uuid-ossp"; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION "uuid-ossp" IS 'generate universally unique identifiers (UUIDs)';


--
-- Name: userrole; Type: TYPE; Schema: public; Owner: crm_user
--

CREATE TYPE public.userrole AS ENUM (
    'admin',
    'vendas'
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
-- Name: alembic_version_user; Type: TABLE; Schema: public; Owner: crm_user
--

CREATE TABLE public.alembic_version_user (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version_user OWNER TO crm_user;

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
    weight_difference_display text,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now(),
    total_profitability double precision DEFAULT 0 NOT NULL
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
    origem character varying(50),
    outras_despesas_totais double precision,
    freight_type character varying(10) NOT NULL,
    freight_value_total double precision,
    payment_condition character varying(50),
    valor_frete_compra double precision,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now(),
    expires_at timestamp with time zone,
    commission_percentage_actual double precision DEFAULT 0.0,
    total_weight_difference_percentage double precision DEFAULT 0.0
);


ALTER TABLE public.budgets OWNER TO crm_user;

--
-- Name: COLUMN budgets.origem; Type: COMMENT; Schema: public; Owner: crm_user
--

COMMENT ON COLUMN public.budgets.origem IS 'Prazo médio em dias';


--
-- Name: COLUMN budgets.outras_despesas_totais; Type: COMMENT; Schema: public; Owner: crm_user
--

COMMENT ON COLUMN public.budgets.outras_despesas_totais IS 'Outras despesas do pedido';


--
-- Name: COLUMN budgets.freight_value_total; Type: COMMENT; Schema: public; Owner: crm_user
--

COMMENT ON COLUMN public.budgets.freight_value_total IS 'Valor total do frete';


--
-- Name: COLUMN budgets.payment_condition; Type: COMMENT; Schema: public; Owner: crm_user
--

COMMENT ON COLUMN public.budgets.payment_condition IS 'Condições de pagamento';


--
-- Name: COLUMN budgets.valor_frete_compra; Type: COMMENT; Schema: public; Owner: crm_user
--

COMMENT ON COLUMN public.budgets.valor_frete_compra IS 'Valor do frete por kg (Valor Frete Total / Peso Total)';


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
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
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
0104
\.


--
-- Data for Name: alembic_version_user; Type: TABLE DATA; Schema: public; Owner: crm_user
--

COPY public.alembic_version_user (version_num) FROM stdin;
512
\.


--
-- Data for Name: budget_items; Type: TABLE DATA; Schema: public; Owner: crm_user
--

COPY public.budget_items (id, budget_id, description, weight, delivery_time, purchase_value_with_icms, purchase_icms_percentage, purchase_other_expenses, purchase_value_without_taxes, purchase_value_with_weight_diff, sale_weight, sale_value_with_icms, sale_icms_percentage, sale_value_without_taxes, weight_difference, profitability, total_purchase, total_sale, unit_value, total_value, commission_percentage, commission_percentage_actual, commission_value, dunamis_cost, ipi_percentage, ipi_value, total_value_with_ipi, weight_difference_display, created_at, updated_at, total_profitability) FROM stdin;
1035	111	80 X 80 X 2,65 X 6000 - 30 BR	1200	3	6.13	0.18	0	4.56164	4.56164	1200	7.97	0.18	5.930876	0	30.016309923623957	5473.968	7117.0512	0.004942	7117.0512	0.015	0.015	143.46	\N	0.05	478.2	10043.999999999998	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-11 18:08:04.832861+00	2025-12-11 18:08:04.832861+00	30.016309923623965
567	58	viga I 572 4"2ª alma	156	0	7.5	0.12	0	5.9895	5.9895	156	9.75	0.12	7.78635	0	30	934.362	1214.6706	0.049913	1214.6706	0.015	0.015	22.81	\N	0	0	1521	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-03 16:31:23.399295+00	2025-12-03 16:31:23.399295+00	30.000000000000004
568	58	chapa 572 12,7 2000x1200	245	0	8	0.18	0	5.9532	5.9532	245	10.4	0.18	7.73916	0	30	1458.534	1896.0942	0.031588	1896.0942	0.015	0.015	38.22	\N	0.0325	82.81	2631.3	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-03 16:31:23.399295+00	2025-12-03 16:31:23.399295+00	29.999999999999982
569	58	chapa 572 4mm 3000x1200	115	0	8.5	0.18	0	6.325275	6.325275	115	11.05	0.18	8.222858	0	30.00000790479465	727.406625	945.62867	0.071503	945.62867	0.015	0.015	19.06	\N	0.0325	41.3	1312.15	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-03 16:31:23.399295+00	2025-12-03 16:31:23.399295+00	30.000007904794668
570	58	80x40x3,00	33	0	5.37	0.12	0	4.288482	4.288482	33	7.56	0.18	5.625774	0	31.183341797866937	141.519906	185.650542	0.170478	185.650542	0.015	0.015	3.74	\N	0.05	12.47	262.02000000000004	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-03 16:31:23.399295+00	2025-12-03 16:31:23.399295+00	31.183341797866948
571	58	cantoneira 3x1/4	45	0	7.1	0.12	0	5.67006	5.67006	45	8.9	0.12	7.10754	0	25.352112676056336	255.1527	319.8393	0.157945	319.8393	0.01	0.01	4.01	\N	0	0	400.5	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-03 16:31:23.399295+00	2025-12-03 16:31:23.399295+00	25.352112676056326
572	58	80x80x3,00	570	0	5.37	0.12	0	4.288482	4.288482	570	7.56	0.18	5.625774	0	31.183341797866937	2444.43474	3206.69118	0.00987	3206.69118	0.015	0.015	64.64	\N	0.05	215.46	4525.8	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-03 16:31:23.399295+00	2025-12-03 16:31:23.399295+00	31.183341797866927
433	42	120x60x3,00 - 60 BRS	3060	3	6.15	0.18	0	4.576523	4.520387	3098	7.9	0.18	5.878785	38	30.05048019118717	14004.16038	18212.47593	0.001898	18212.47593	0.015	0.015	367.11	\N	0.05	1223.71	25713.4	{"has_difference": true, "absolute_difference": 38.0, "percentage_difference": 1.2418300653594772, "formatted_display": "1.2%"}	2025-12-02 20:32:50.383862+00	2025-12-02 20:32:50.383862+00	30.050466688528466
919	100	50x25x1,50 15 brs	158	3	7.02	0.12	0	5.606172	5.434204	163	9.75	0.18	7.255463	5	33.51473371260998	885.775176	1182.640469	0.044512	1182.640469	0.015	0.015	23.84	\N	0.05	79.46	1669.1200000000001	{"has_difference": true, "absolute_difference": 5.0, "percentage_difference": 3.1645569620253164, "formatted_display": "3.2%"}	2025-12-10 16:35:08.773602+00	2025-12-10 16:35:08.773602+00	33.51474516824797
920	100	chato 1x1/4 10 brs	76	3	6.5	0.12	0	5.1909	5.0578	78	8	0.12	6.3888	2	26.31578947368421	394.5084	498.3264	0.081908	498.3264	0.01	0.01	6.24	\N	0	0	624	{"has_difference": true, "absolute_difference": 2.0, "percentage_difference": 2.6315789473684212, "formatted_display": "2.6%"}	2025-12-10 16:35:08.773602+00	2025-12-10 16:35:08.773602+00	26.315789473684205
599	59	TUBO REDONDO 38,10X4,25X6000	4	0	135.96	0.12	0	108.577656	108.577656	4	192	0.18	142.8768	0	31.58950493460643	434.310624	571.5072	35.7192	571.5072	0.015	0.015	11.52	\N	0.0325	24.96	792.96	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-03 17:33:31.816248+00	2025-12-03 17:33:31.816248+00	31.58950493460644
1174	118	CANTONEIRA 4"X1/4X6000	300	2	7.75	0.12	0	6.18915	6.18915	300	10.08	0.12	8.049888	0	30.06451612903226	1856.745	2414.9664	0.026833	2414.9664	0.015	0.015	45.36	\N	0	0	3024	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-12 17:20:28.322926+00	2025-12-12 17:20:28.322926+00	30.06451612903225
166	28	50 x 30 x 1,20 x 6000 - 45 br	407	1	6.17	0.12	0	4.927362	4.927362	407	8.87	0.18	6.600611	0	33.95831278481264	2005.436334	2686.448677	0.016218	2686.448677	0.015	0.015	54.15	\N	0.05	180.5	3789.17	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-11-28 16:43:31.99682+00	2025-11-28 16:43:31.99682+00	33.95831278481263
167	28	50 x 20 x 0,90 x 6000 - 45 br	267	1	6.27	0.12	0	5.007222	5.007222	267	9	0.18	6.69735	0	33.753806002609835	1336.928274	1788.19245	0.025084	1788.19245	0.015	0.015	36.05	\N	0.05	120.15	2523.1499999999996	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-11-28 16:43:31.99682+00	2025-11-28 16:43:31.99682+00	33.75380600260982
61	12	galv 30x20x1,25x6000	58	1	6.7	0.12	0	5.35062	5.35062	58	9.57	0.18	7.121516	0	33.09702427008459	310.33596	413.04792799999996	0.122785	413.04792799999996	0.015	0.015	8.33	\N	0.05	27.75	582.9000000000001	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-11-24 18:06:48.9645+00	2025-11-24 18:06:48.9645+00	33.09702427008459
600	59	TUBO QUADRADO 60X60X4,25X6000	6	0	284.28	0.12	0	227.026008	227.026008	6	401	0.18	298.40415	0	31.440513194417797	1362.156048	1790.4249	49.734025	1790.4249	0.015	0.015	36.09	\N	0.05	120.3	2526.3	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-03 17:33:31.816248+00	2025-12-03 17:33:31.816248+00	31.440513194417786
1189	116	60 X 40 X 3,00 X 6000	24	1	5.37	0.12	0	4.288482	4.288482	24	8	0.18	5.9532	0	38.8183511088539	102.923568	142.8768	0.24805	142.8768	0.015	0.015	2.88	\N	0.05	9.6	201.60000000000002	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-12 17:23:31.284003+00	2025-12-12 17:23:31.284003+00	38.818351108853896
1190	116	100 X 50 X 3,00 X 6000	39	1	5.9	0.12	0	4.71174	4.71174	39	8.47	0.18	6.302951	0	33.771197052468935	183.75786	245.815089	0.161614	245.815089	0.015	0.015	4.95	\N	0.05	16.52	346.71000000000004	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-12 17:23:31.284003+00	2025-12-12 17:23:31.284003+00	33.771197052468935
1205	121	TUBO 4" SCH80 X 6000 SEM COSTURA (114,30X8,58) - 4 BRS GALVANIZADO	552	7	12.3	0.18	2.19	11.343045	11.343045	552	22.99	0.18	17.108009	0	50.82377791853951	6261.36084	9443.620968	0.030993	9443.620968	0.03	0.03	380.71	\N	0	0	12690.48	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-12 17:58:16.523963+00	2025-12-12 17:58:16.523963+00	50.82377791853949
447	54	TUBO RETANGULAR 70X30X1,20X6000 - 27 BRS	334	3	6.44	0.12	0	5.142984	5.142984	334	9.06	0.18	6.741999	0	31.091191417278374	1717.756656	2251.827666	0.020186	2251.827666	0.015	0.015	45.39	\N	0.05	151.3	3176.34	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-03 12:18:41.651975+00	2025-12-03 12:18:41.651975+00	31.091191417278385
306	14	TB NBR 5580 GALV BSP RIR 4'' X 3,75 X 6000	100	7	620.95	0.12	0	495.89067	495.89067	100	847.77	0.18	630.868046	0	27.219180389096653	49589.067	63086.8046	6.30868	63086.8046	0.01	0.01	847.77	\N	0.0325	2755.25	87532	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-02 14:42:40.664681+00	2025-12-02 14:42:40.664681+00	27.219180389096653
307	14	LUVA GALV BSP 4'' 	200	7	168.83	0.18	0	125.634845	125.634845	200	215.77	0.18	160.565246	0	27.803115449380307	25126.969	32113.0492	0.802826	32113.0492	0.01	0.01	431.54	\N	0	0	43154	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-02 14:42:40.664681+00	2025-12-02 14:42:40.664681+00	27.8031154493803
309	46	PERFIL UE 100X40X17X3,00X6000 - 4 BRS	112	0	5.3	0.12	0	4.23258	4.23258	112	7.45	0.18	5.543918	0	30.982001521530606	474.04896	620.918816	0.049499	620.918816	0.015	0.015	12.52	\N	0	0	834.4	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-02 14:46:28.780604+00	2025-12-02 14:46:28.780604+00	30.982001521530588
310	46	TUBO QUADRADO 50X50X3,00X6000 - 3 BRS	81	0	5.37	0.12	0	4.288482	4.288482	81	7.55	0.18	5.618333	0	31.009830518118065	347.367042	455.084973	0.069362	455.084973	0.015	0.015	9.17	\N	0.05	30.58	642.3299999999999	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-02 14:46:28.780604+00	2025-12-02 14:46:28.780604+00	31.009830518118054
311	36	TUBO REDONDO 12,70X1,55 GALVANIZADO - 30 BRS	93	5	8.4	0.18	1.52	7.77086	7.77086	93	14.7	0.18	10.939005	0	40.76955446372731	722.68998	1017.327465	0.117624	1017.327465	0.025	0.025	34.18	\N	0.0325	44.43	1411.74	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-02 14:46:57.067656+00	2025-12-02 14:46:57.067656+00	40.769554463727296
312	16	TUBO RETANGULAR 80X50X4,25X6000	200	3	6.29	0.12	0	5.023194	5.023194	200	8.64	0.18	6.429456	0	27.995375054198586	1004.6388	1285.8912	0.032147	1285.8912	0.01	0.01	17.28	\N	0.05	86.4	1814	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-02 14:47:24.826949+00	2025-12-02 14:47:24.826949+00	27.9953750541986
313	35	TUBO RETANGULAR 40X30X2,00X6000 - 4 PÇS	52	0	5.56	0.12	0	4.440216	4.440216	52	7.85	0.18	5.841578	0	31.560671823172566	230.891232	303.76205600000003	0.112338	303.76205600000003	0.015	0.015	6.12	\N	0.05	20.41	428.48	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-02 14:47:48.816969+00	2025-12-02 14:47:48.816969+00	31.56067182317257
314	19	TUBO RETANGULAR 30X30X1,50X6000 - 5 BRS	45	1	6.19	0.12	0	4.943334	4.943334	45	9.14	0.18	6.801531	0	37.58995447202233	222.45003	306.068895	0.151145	306.068895	0.015	0.015	6.17	\N	0.05	20.57	432	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-02 14:48:37.5703+00	2025-12-02 14:48:37.5703+00	37.58995447202231
315	19	CANTONEIRA 1"X1/8X6000 - 1 BR	8	1	6.5	0.12	0	5.1909	5.1909	8	8.45	0.12	6.74817	0	30	41.5272	53.98536	0.843521	53.98536	0.015	0.015	1.01	\N	0	0	67.6	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-02 14:48:37.5703+00	2025-12-02 14:48:37.5703+00	30.000000000000004
316	19	CANTONEIRA 2"X1/8X6000 - 1 BR	16	1	6.5	0.12	0	5.1909	5.1909	16	8.45	0.12	6.74817	0	30	83.0544	107.97072	0.421761	107.97072	0.015	0.015	2.03	\N	0	0	135.2	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-02 14:48:37.5703+00	2025-12-02 14:48:37.5703+00	30.000000000000004
672	60	TUBO RETANGULAR 180X100X6,30X6000 - 12 BRS	954	7	6.59	0.12	0	5.262774	2.631387	1908	8.56	0.18	6.369924	954	142.074768933646	5020.686396	12153.814992	0.003339	12153.814992	0.05	0.05	816.62	\N	0.05	816.62	17152.920000000002	{"has_difference": true, "absolute_difference": 954.0, "percentage_difference": 100.0, "formatted_display": "100.0%"}	2025-12-04 17:17:10.173868+00	2025-12-04 17:17:10.173868+00	142.074768933646
1036	77	CHAPA AÇO CARBONO GALVNIZADA LISA - #0,65 X 1500 X 3000 - 400 PÇ	9200	7	8.1	0.18	0	6.027615	6.027615	9200	10.77	0.18	8.014496	0	32.96297125811785	55454.058	73733.36319999999	0.000871	73733.36319999999	0.015	0.015	1486.26	\N	0.0325	3220.23	102304	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-11 18:14:57.602767+00	2025-12-11 18:14:57.602767+00	32.96297125811785
317	24	TUBO RETANGULAR 120X60X2,00X6000 - 30 brs	1020	5	6.19	0.12	0	4.943334	4.943334	1020	8.71	0.18	6.481547	0	31.116914212149126	5042.20068	6611.17794	0.006354	6611.17794	0.015	0.015	133.26	\N	0.05	444.21	9333	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-02 14:50:40.075862+00	2025-12-02 14:50:40.075862+00	31.116914212149126
318	24	TUBO QUADRADO 120X120X2,65X6000 - 5 brs	295	0	6.27	0.12	0	5.007222	5.007222	295	8.82	0.18	6.563403	0	31.07872988255763	1477.13049	1936.2038850000001	0.022249	1936.2038850000001	0.015	0.015	39.03	\N	0.05	130.1	2731.7	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-02 14:50:40.075862+00	2025-12-02 14:50:40.075862+00	31.078729882557642
320	25	VIGA I 3" 1° ALMA X6000 - 8 BRS	420	2	7.5	0.12	0	5.9895	5.9895	420	9.38	0.12	7.490868	0	25.066666666666666	2515.59	3146.16456	0.017835	3146.16456	0.01	0.01	39.4	\N	0	0	3939.6000000000004	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-02 14:51:57.155988+00	2025-12-02 14:51:57.155988+00	25.06666666666666
101	18	02 - CHAPAS DE 3000 X 1500 X 20MM  ASTM A572 GR50	1455	5	9.5	0.18	0	7.069425	7.069425	1455	11.8	0.12	9.42348	0	33.29910141206675	10286.013375	13711.1634	0.006477	13711.1634	0.015	0.015	257.53	\N	0.0325	557.99	17721.899999999998	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-11-27 17:23:46.360739+00	2025-11-27 17:23:46.360739+00	33.29910141206673
321	25	VIGA U 3" 1° ALMA X6000 - 4 BRS	147	2	7.5	0.12	0	5.9895	5.9895	147	9.38	0.12	7.490868	0	25.066666666666666	880.4565	1101.157596	0.050958	1101.157596	0.01	0.01	13.79	\N	0	0	1378.8600000000001	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-02 14:51:57.155988+00	2025-12-02 14:51:57.155988+00	25.06666666666666
322	25	BARRA QUADRADA 3/8 X 6000 - 1 BR	5	2	7.85	0.12	0	6.26901	6.26901	5	9.96	0.12	7.954056	0	26.878980891719745	31.34505	39.77028	1.590811	39.77028	0.01	0.01	0.5	\N	0	0	49.800000000000004	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-02 14:51:57.155988+00	2025-12-02 14:51:57.155988+00	26.87898089171974
323	25	PERFIL U  50X25X3,00X6000 - 3 BRS	40	0	6.2	0.18	0	4.61373	4.61373	40	8.06	0.12	6.436716	0	39.51219512195122	184.5492	257.46864	0.160918	257.46864	0.015	0.015	4.84	\N	0	0	322.40000000000003	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-02 14:51:57.155988+00	2025-12-02 14:51:57.155988+00	39.51219512195121
106	20	CANT 3X3/16X6000MM	236	3	7.1	0.12	2.17	7.84006	7.84006	236	13	0.12	10.3818	0	32.41990494970702	1850.25416	2450.1048	0.043991	2450.1048	0.015	0.015	46.02	\N	0	0	3068	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-11-27 17:51:45.148826+00	2025-11-27 17:51:45.148826+00	32.41990494970703
215	32	70 X 50 X 2,00 X 6000 - 15 BR	338	1	6.24	0.12	0	4.983264	4.953951	340	8.67	0.18	6.451781	2	30.235058844950224	1684.343232	2193.60554	0.018976	2193.60554	0.015	0.015	44.22	\N	0.05	147.39	3094	{"has_difference": true, "absolute_difference": 2.0, "percentage_difference": 0.591715976331361, "formatted_display": "0.6%"}	2025-12-01 14:48:17.594987+00	2025-12-01 14:48:17.594987+00	30.235067195615393
574	61	TUBO REDONDO 26,70X2,65X6000 - 6 BRS	63	0	5.99	0.12	0	4.783614	4.783614	63	8.4	0.12	6.70824	0	40.23372287145242	301.367682	422.61912	0.10648	422.61912	0.025	0.025	13.23	\N	0	0	529.2	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-03 16:36:38.061209+00	2025-12-03 16:36:38.061209+00	40.233722871452414
601	59	TUBO QUADRADO 60X40X3,00X6000	2	0	145.53	0.12	0	116.220258	116.220258	2	205	0.18	152.55075	0	31.260033857436454	232.440516	305.1015	76.275375	305.1015	0.015	0.015	6.15	\N	0.05	20.5	430.5	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-03 17:33:31.816248+00	2025-12-03 17:33:31.816248+00	31.260033857436454
602	59	TUBO QUADRADO 50X50X2,65XX6000	2	0	128.88	0.12	0	102.923568	102.923568	2	182	0.18	135.4353	0	31.588228655267763	205.847136	270.8706	67.71765	270.8706	0.015	0.015	5.46	\N	0.05	18.2	382.2	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-03 17:33:31.816248+00	2025-12-03 17:33:31.816248+00	31.58822865526778
1037	23	70 X 70 X 3,00 X 6000 - 329 BR	12840	4	6.13	0.18	0	4.56164	4.519054	12961	7.9	0.18	5.878785	121	30.088841602689413	58571.4576	76194.932385	0.000454	76194.932385	0.015	0.015	1535.88	\N	0.05	5119.6	107576.3	{"has_difference": true, "absolute_difference": 121.0, "percentage_difference": 0.942367601246106, "formatted_display": "0.9%"}	2025-12-11 18:36:23.902031+00	2025-12-11 18:36:23.902031+00	30.088844476699506
216	32	70 X 70 X 2,00 X 6000 - 10 BR	267	1	5.47	0.12	0	4.368342	4.368342	267	7.85	0.18	5.841578	0	33.72528982391946	1166.347314	1559.701326	0.021879	1559.701326	0.015	0.015	31.44	\N	0.05	104.8	2200.08	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-01 14:48:17.594987+00	2025-12-01 14:48:17.594987+00	33.72528982391947
129	17	Perfil U 60x25x2,00x6000 - 20 br	207	5	8.5	0.18	0	6.325275	6.234914	210	10.17	0.12	8.121762	3	30.262614688831313	1309.331925	1705.57002	0.038675	1705.57002	0.015	0.015	32.04	\N	0	0	2135.7	{"has_difference": true, "absolute_difference": 3.0, "percentage_difference": 1.4492753623188406, "formatted_display": "1.4%"}	2025-11-28 11:37:23.958373+00	2025-11-28 11:37:23.958373+00	30.262616181149028
130	17	Chato 3/4 x 1/8 - 5 br	15	1	6.5	0.12	0	5.1909	5.089118	15.3	8.32	0.12	6.644352	0.3000000000000007	30.559990945385824	77.8635	101.6585856	0.434271	101.6585856	0.015	0.015	1.91	\N	0	0	127.296	{"has_difference": true, "absolute_difference": 0.3, "percentage_difference": 2.0, "formatted_display": "2.0%"}	2025-11-28 11:37:23.958373+00	2025-11-28 11:37:23.958373+00	30.559999999999988
131	17	Chato 2'' x 1/8 - 2 br	16	1	6.5	0.12	0	5.1909	5.095362	16.3	8.32	0.12	6.644352	0.3000000000000007	30.39999905796683	83.0544	108.30293759999999	0.407629	108.30293759999999	0.015	0.015	2.03	\N	0	0	135.616	{"has_difference": true, "absolute_difference": 0.3, "percentage_difference": 1.875, "formatted_display": "1.9%"}	2025-11-28 11:37:23.958373+00	2025-11-28 11:37:23.958373+00	30.399999999999984
132	17	100 x 050 x 2,00 x 6000 - 2 br	56	1	5.98	0.12	0	4.775628	4.691845	57	7.67	0.12	6.125262	1	30.551243700505875	267.435168	349.13993400000004	0.107461	349.13993400000004	0.015	0.015	6.56	\N	0.05	21.86	458.85	{"has_difference": true, "absolute_difference": 1.0, "percentage_difference": 1.7857142857142858, "formatted_display": "1.8%"}	2025-11-28 11:37:23.958373+00	2025-11-28 11:37:23.958373+00	30.551242236024876
133	17	Perfil U 200x50x3,00x6000 - 2 br	75	1	5.29	0.12	0	4.224594	4.169007	76	6.95	0.12	5.55027	1	33.1317025852919	316.84455	421.82052000000004	0.07303	421.82052000000004	0.015	0.015	7.92	\N	0	0	528.2	{"has_difference": true, "absolute_difference": 1.0, "percentage_difference": 1.3333333333333333, "formatted_display": "1.3%"}	2025-11-28 11:37:23.958373+00	2025-11-28 11:37:23.958373+00	33.131695022054195
134	17	Perfil U 50x25x3,00x6000 - 30 br	340	5	6.59	0.18	0	4.903949	4.846926	344	7.9	0.12	6.30894	4	30.163736768417753	1667.34266	2170.27536	0.01834	2170.27536	0.015	0.015	40.76	\N	0	0	2717.6	{"has_difference": true, "absolute_difference": 4.0, "percentage_difference": 1.1764705882352942, "formatted_display": "1.2%"}	2025-11-28 11:37:23.958373+00	2025-11-28 11:37:23.958373+00	30.163727712694644
135	17	80 x 80 x 2,00 x 6000 - 9 br	266	1	5.88	0.12	0	4.695768	4.643399	269	7.57	0.12	6.045402	3	30.193463882815152	1249.074288	1626.213138	0.022474	1626.213138	0.015	0.015	30.54	\N	0.05	101.82	2138.55	{"has_difference": true, "absolute_difference": 3.0, "percentage_difference": 1.1278195488721805, "formatted_display": "1.1%"}	2025-11-28 11:37:23.958373+00	2025-11-28 11:37:23.958373+00	30.19346836478953
308	15	100 X 050 X 2,00 X 6000 - 9 BR	249	1	5.98	0.12	0	4.775628	4.645044	256	8.35	0.18	6.213653	7	33.769518652568195	1189.131372	1590.695168	0.024272	1590.695168	0.015	0.015	32.06	\N	0.05	106.88	2245.12	{"has_difference": true, "absolute_difference": 7.0, "percentage_difference": 2.8112449799196786, "formatted_display": "2.8%"}	2025-12-02 14:43:11.823545+00	2025-12-02 14:43:11.823545+00	33.769506503273035
1038	23	70 X 70 X 4,75 X 6000 - 108 BR	6536	4	6.19	0.18	0	4.606289	4.561622	6600	7.97	0.18	5.930876	64	30.01682296341082	30106.704904	39143.781599999995	0.000899	39143.781599999995	0.015	0.015	789.03	\N	0.05	2630.1	55241.99999999999	{"has_difference": true, "absolute_difference": 64.0, "percentage_difference": 0.9791921664626683, "formatted_display": "1.0%"}	2025-12-11 18:36:23.902031+00	2025-12-11 18:36:23.902031+00	30.016824241696828
616	53	26,70 X 2,00 X 6000 - 4 BR	30	1	5.98	0.12	0	4.775628	4.775628	30	8.7	0.18	6.474105	0	35.56552143508665	143.26884	194.22315	0.215804	194.22315	0.015	0.015	3.92	\N	0.0325	8.48	269.40000000000003	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-03 18:55:28.433542+00	2025-12-03 18:55:28.433542+00	35.565521435086644
1041	112	cantoneira 2 x 1/4	218	3	6.5	0.12	0	5.1909	5.09737	222	8.35	0.12	6.66831	4	30.81863784657578	1131.6162	1480.36482	0.030037	1480.36482	0.015	0.015	27.81	\N	0	0	1853.6999999999998	{"has_difference": true, "absolute_difference": 4.0, "percentage_difference": 1.834862385321101, "formatted_display": "1.8%"}	2025-12-11 20:16:26.664131+00	2025-12-11 20:16:26.664131+00	30.818630910374047
142	21	TB RED 42,40X2,65X6000MM	5600	3	6.57	0.12	0	5.246802	5.246802	5600	9.2	0.18	6.84618	0	30.482911304829113	29382.0912	38338.608	0.001223	38338.608	0.015	0.015	772.8	\N	0.0325	1674.4	53200	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-11-28 12:13:41.59574+00	2025-11-28 12:13:41.59574+00	30.48291130482912
1042	112	SCH 40 S/C 8" X 5800MM	1032	3	14.75	0.18	0	10.976213	10.808637	1048	19.75	0.18	14.696963	16	35.97424911207583	11327.451816	15402.417224	0.014024	15402.417224	0.015	0.015	310.47	\N	0	0	20698	{"has_difference": true, "absolute_difference": 16.0, "percentage_difference": 1.550387596899225, "formatted_display": "1.6%"}	2025-12-11 20:16:26.664131+00	2025-12-11 20:16:26.664131+00	35.97424623112606
395	44	15,87 X 0,90 X 6000 - 100 BR 	205	1	6.43	0.12	0	5.134998	5.134998	205	8.37	0.12	6.684282	0	30.171073094867808	1052.67459	1370.2778099999998	0.032606	1370.2778099999998	0.015	0.015	25.74	\N	0.0325	55.77	1771.2	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-02 19:39:49.954513+00	2025-12-02 19:39:49.954513+00	30.171073094867772
933	101	Tubo Aço Galv.20x20x1,25 (250brs)	1120	5	7.55	0.12	0	6.02943	5.821519	1160	9.6	0.12	7.66656	40	31.69346351012511	6752.9616	8893.2096	0.006609	8893.2096	0.015	0.015	167.04	\N	0.05	556.8	11692.8	{"has_difference": true, "absolute_difference": 40.0, "percentage_difference": 3.5714285714285716, "formatted_display": "3.6%"}	2025-12-10 17:32:44.694601+00	2025-12-10 17:32:44.694601+00	31.693472090823093
258	41	20 X 20 X 1,20 X 6000 - 23 BR	104	1	5.98	0.12	0	4.775628	4.775628	104	8.57	0.18	6.377366	0	33.539840205309126	496.665312	663.246064	0.061321	663.246064	0.015	0.015	13.37	\N	0.05	44.56	936	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-01 17:50:50.961007+00	2025-12-01 17:50:50.961007+00	33.53984020530913
259	37	TB 100X100X3X6000MM	180	1	6.31	0.18	0	4.695587	4.695587	180	8.2	0.18	6.10203	0	29.952442580661376	845.20566	1098.3654	0.0339	1098.3654	0.01	0.01	14.76	\N	0.05	73.8	1549.8	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-01 18:02:49.818273+00	2025-12-01 18:02:49.818273+00	29.952442580661366
260	37	TB 040X040X3X6000MM	306	1	5.85	0.12	0	4.67181	4.67181	306	8.2	0.18	6.10203	0	30.61383061383061	1429.57386	1867.22118	0.019941	1867.22118	0.015	0.015	37.64	\N	0.05	125.46	2634.66	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-01 18:02:49.818273+00	2025-12-01 18:02:49.818273+00	30.613830613830608
261	37	TB 080X080X3X6000MM	451	1	6.31	0.18	0	4.695587	4.695587	451	8.2	0.18	6.10203	0	29.952442580661376	2117.709737	2752.01553	0.01353	2752.01553	0.01	0.01	36.98	\N	0.05	184.91	3883.1099999999997	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-01 18:02:49.818273+00	2025-12-01 18:02:49.818273+00	29.952442580661366
262	31	02-TB RET 120X80X3,75X6000MM	141	0	6.35	0.12	0	5.07111	5.07111	141	8.9	0.18	6.622935	0	30.601288475304223	715.02651	933.833835	0.046971	933.833835	0.015	0.015	18.82	\N	0.05	62.75	1318.35	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-01 18:04:18.270341+00	2025-12-01 18:04:18.270341+00	30.601288475304212
263	31	02-TB RET 100X80X3,75X6000MM	127	0	6.4	0.12	0	5.11104	5.11104	127	8.9	0.18	6.622935	0	29.58096590909091	649.10208	841.112745	0.052149	841.112745	0.01	0.01	11.3	\N	0.05	56.52	1187.45	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-01 18:04:18.270341+00	2025-12-01 18:04:18.270341+00	29.580965909090917
264	33	TB QD50X50X1,25X6000MM	460	3	6.68	0.12	0	5.334648	5.334648	460	9.3	0.18	6.920595	0	29.729178007621123	2453.93808	3183.4737	0.015045	3183.4737	0.01	0.01	42.78	\N	0.05	213.9	4494.2	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-01 18:04:52.01562+00	2025-12-01 18:04:52.01562+00	29.729178007621137
265	33	TB QD20X20X1,25	520	3	7.55	0.18	0	5.618333	5.618333	520	9.81	0.18	7.300112	0	29.933772170499683	2921.53316	3796.0582400000003	0.014039	3796.0582400000003	0.01	0.01	51.01	\N	0.05	255.06	5356	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-01 18:04:52.01562+00	2025-12-01 18:04:52.01562+00	29.933772170499708
266	33	TB QD30X30X1,25	500	3	6.7	0.12	0	5.35062	5.35062	500	8.7	0.18	6.474105	0	20.997286295793756	2675.31	3237.0525	0.012948	3237.0525	0.01	0.01	43.5	\N	0.05	217.5	4570	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-01 18:04:52.01562+00	2025-12-01 18:04:52.01562+00	20.99728629579376
267	33	PUDC 75X40X2X6000MM	750	3	5.38	0.12	0	4.296468	4.296468	750	7.55	0.18	5.618333	0	30.766317821987737	3222.351	4213.74975	0.007491	4213.74975	0.015	0.015	84.94	\N	0.05	283.13	5947.5	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-01 18:04:52.01562+00	2025-12-01 18:04:52.01562+00	30.766317821987734
268	38	127 X 2,00 GALV ELET 02 brs	76	5	7.3	0.18	1.59	7.022295	6.842236	78	12.45	0.18	9.264668	2	35.40409889398728	533.69442	722.644104	0.118778	722.644104	0.015	0.015	14.57	\N	0.0325	31.56	1002.3	{"has_difference": true, "absolute_difference": 2.0, "percentage_difference": 2.6315789473684212, "formatted_display": "2.6%"}	2025-12-01 18:05:50.231882+00	2025-12-01 18:05:50.231882+00	35.40409584945632
396	44	15,87 X 0,75 X 6000 - 250 BR	432	1	6.68	0.12	0	5.334648	5.334648	432	8.7	0.12	6.94782	0	30.239520958083833	2304.567936	3001.45824	0.016083	3001.45824	0.015	0.015	56.38	\N	0.0325	122.15	3879.36	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-02 19:39:49.954513+00	2025-12-02 19:39:49.954513+00	30.239520958083844
397	44	15 X 15 X 0,75 X 6000 - 395 BR 	807	1	7.12	0.18	0	5.298348	5.298348	807	8.67	0.12	6.923862	0	30.67963825705673	4275.766836	5587.556634	0.00858	5587.556634	0.015	0.015	104.95	\N	0.05	349.83	7343.7	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-02 19:39:49.954513+00	2025-12-02 19:39:49.954513+00	30.67963825705673
326	48	TUBO QUADRADO 40X40X3,00X6000 - 10 BRS	220	0	5.99	0.12	0	4.783614	4.783614	220	7.78	0.12	6.213108	0	29.883138564273793	1052.39508	1366.88376	0.028241	1366.88376	0.01	0.01	17.12	\N	0.05	85.58	1797.4	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-02 16:35:40.41065+00	2025-12-02 16:35:40.41065+00	29.883138564273782
327	48	CANTONEIRA 2"X1/8X6000 - 10 BRS	370	2	6.59	0.12	0	5.262774	5.262774	370	8.57	0.12	6.844002	0	30.045523520485585	1947.22638	2532.2807399999997	0.018497	2532.2807399999997	0.015	0.015	47.56	\N	0	0	3170.9	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-02 16:35:40.41065+00	2025-12-02 16:35:40.41065+00	30.045523520485574
683	70	200X100X3,00	5	0	512.4	0.12	0	409.20264	409.20264	5	722	0.12	576.5892	0	40.905542544886806	2046.0132	2882.946	115.31784	2882.946	0.025	0.025	90.25	\N	0.05	180.5	3790.5	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-04 18:06:21.54332+00	2025-12-04 18:06:21.54332+00	40.905542544886785
684	70	200x150x3,00	19	0	941	0.18	0	700.24515	700.24515	19	1140	0.12	910.404	0	30.012182162204194	13304.65785	17297.676	47.916	17297.676	0.015	0.015	324.9	\N	0	0	21660	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-04 18:06:21.54332+00	2025-12-04 18:06:21.54332+00	30.012182162204205
576	52	F CHT 3X1/4X600MM	1	0	7.1	0.12	2.41	8.08006	8.08006	1	13.2	0.12	10.54152	0	30.463387648111524	8.08006	10.54152	10.54152	10.54152	0.015	0.015	0.2	\N	0	0	13.2	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-03 17:08:25.087873+00	2025-12-03 17:08:25.087873+00	30.46338764811154
577	52	F CHT 4X1/4X600MM	1	0	7.1	0.12	2.41	8.08006	8.08006	1	13.2	0.12	10.54152	0	30.463387648111524	8.08006	10.54152	10.54152	10.54152	0.015	0.015	0.2	\N	0	0	13.2	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-03 17:08:25.087873+00	2025-12-03 17:08:25.087873+00	30.46338764811154
578	52	F CHT 3X1/4X60-0MM	1	0	7.1	0.12	2.41	8.08006	8.08006	1	13.2	0.12	10.54152	0	30.463387648111524	8.08006	10.54152	10.54152	10.54152	0.015	0.015	0.2	\N	0	0	13.2	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-03 17:08:25.087873+00	2025-12-03 17:08:25.087873+00	30.46338764811154
687	68	80X40X3,00	25	0	161.1	0.12	0	128.65446	128.65446	25	230	0.18	171.1545	0	33.03425314598499	3216.3615	4278.8625	6.84618	4278.8625	0.015	0.015	86.25	\N	0.05	287.5	6037.5	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-04 18:37:29.286653+00	2025-12-04 18:37:29.286653+00	33.034253145985005
688	68	cantoneira 1.1/4x1/8	5	0	58.5	0.12	0	46.7181	46.7181	5	73	0.12	58.2978	0	24.786324786324787	233.5905	291.48900000000003	11.65956	291.48900000000003	0.01	0.01	3.65	\N	0	0	365	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-04 18:37:29.286653+00	2025-12-04 18:37:29.286653+00	24.78632478632481
1477	129	30-tb 120120x3x60000mm	2049	4	6.21	0.12	0	4.959306	4.959306	2049	8.1	0.12	6.46866	0	30.434782608695656	10161.617994	13254.28434	0.003157	13254.28434	0.015	0.015	248.95	\N	0.05	829.85	17436.989999999998	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-18 11:47:01.853355+00	2025-12-18 11:47:01.853355+00	30.434782608695656
1478	129	30-tb 100x100x3x6000mm	1700	4	6.19	0.12	0	4.943334	4.943334	1700	8.1	0.12	6.46866	0	30.8562197092084	8403.6678	10996.722	0.003805	10996.722	0.015	0.015	206.55	\N	0.05	688.5	14467	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-18 11:47:01.853355+00	2025-12-18 11:47:01.853355+00	30.8562197092084
539	56	TUBO REDONDO 25,40X1,20X6000	250	0	6.27	0.12	0	5.007222	5.007222	250	8.83	0.18	6.570845	0	31.227355208137364	1251.8055	1642.71125	0.026283	1642.71125	0.015	0.015	33.11	\N	0.0325	71.74	2280	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-03 14:15:45.090005+00	2025-12-03 14:15:45.090005+00	31.227355208137375
540	56	TUBO REDONDO 50,80X1,90X6000	600	5	0.01	0.12	0	0.007986	0.007986	600	0.02	0.18	0.014883	0	86.36363636363636	4.7916	8.9298	2.5e-05	8.9298	0.05	0.05	0.6	\N	0.0325	0.39	12	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-03 14:15:45.090005+00	2025-12-03 14:15:45.090005+00	86.36363636363637
541	51	TUBO REDONDO 25,40X1,50X6000 - 30 BRS	180	0	9.8	0.18	0	7.29267	7.29267	180	12.74	0.18	9.480471	0	30	1312.6806	1706.48478	0.052669	1706.48478	0.05	0.05	114.66	\N	0.0325	74.53	2367	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-03 14:16:03.045455+00	2025-12-03 14:16:03.045455+00	30.000000000000004
542	34	CHAPA XADREZ 1200 X 2000 X 6,30 - 1 PÇ	127	2	6.75	0.18	0	5.023013	5.023013	127	8.1	0.12	6.46866	0	28.780474985830217	637.922651	821.51982	0.050934	821.51982	0.01	0.01	10.29	\N	0.0325	33.43	1061.72	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-03 14:16:44.152783+00	2025-12-03 14:16:44.152783+00	28.780474985830228
543	34	TUBO 50X30X4,75X6000 - 2 PÇS	68	0	6.36	0.12	0	5.079096	5.079096	68	8.9	0.12	7.10754	0	39.937106918238996	345.378528	483.31272	0.104523	483.31272	0.015	0.015	9.08	\N	0.05	30.26	635.8	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-03 14:16:44.152783+00	2025-12-03 14:16:44.152783+00	39.937106918238996
545	57	TUBO REDONDO NBR 5580 1.1/2 X 3,00 X 6000	315	0	6.51	0.18	0	4.844417	4.844417	315	8.27	0.18	6.154121	0	27.035327470777187	1525.991355	1938.548115	0.019537	1938.548115	0.01	0.01	26.05	\N	0.0325	84.66	2690.1	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-03 14:19:27.740776+00	2025-12-03 14:19:27.740776+00	27.03532747077717
269	38	101,60 X 2,00 GALV ELET 02 brs	60	5	5.46	0.18	1.59	5.653059	5.470702	62	12.45	0.18	9.264668	2	69.3506244719599	339.18354	574.409416	0.14943	574.409416	0.04	0.04	30.88	\N	0.0325	25.09	796.6999999999999	{"has_difference": true, "absolute_difference": 2.0, "percentage_difference": 3.3333333333333335, "formatted_display": "3.3%"}	2025-12-01 18:05:50.231882+00	2025-12-01 18:05:50.231882+00	69.35061648333524
270	38	76,20 X 2,00 GALV ELET 01 br	23	5	5.46	0.18	1.59	5.653059	5.653059	23	12.45	0.18	9.264668	0	63.887693370969586	130.020357	213.087364	0.402812	213.087364	0.04	0.04	11.45	\N	0.0325	9.31	295.55	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-01 18:05:50.231882+00	2025-12-01 18:05:50.231882+00	63.88769337096962
691	72	TUBO REDONDO 88,90X3,35X6000 GALVANIZADO SEM ROSCA	1000	7	6.4	0.18	2.19	6.95256	6.95256	1000	11.57	0.18	8.609816	0	23.836629960762654	6952.56	8609.816	0.00861	8609.816	0.01	0.01	115.7	\N	0.0325	376.03	11950	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-04 18:38:07.201957+00	2025-12-04 18:38:07.201957+00	23.836629960762657
692	72	TUBO SCHEDULE 021,30 X 02,77 X 6000 S/C	500	3	20	0.18	0	14.883	14.883	500	24.6	0.18	18.30609	0	23	7441.5	9153.045	0.036612	9153.045	0.01	0.01	123	\N	0.0325	399.75	12700	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-04 18:38:07.201957+00	2025-12-04 18:38:07.201957+00	23
334	50	1045 REDONDO LAMINADO 95.25 x 6800 - 10 BRS	3807	5	8.9	0.12	0	7.10754	7.10754	3807	11.57	0.12	9.239802	0	30	27058.40478	35175.926214	0.002427	35175.926214	0.05	0.05	2202.35	\N	0	0	44046.99	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-02 17:15:56.669164+00	2025-12-02 17:15:56.669164+00	29.999999999999982
335	50	 4140 REDONDO LAMINADO 95.00 x 6300 - 10 BRS	3509	5	10.15	0.12	0	8.10579	8.10579	3509	13.19	0.12	10.533534	0	29.95073891625616	28443.21711	36962.170806	0.003002	36962.170806	0.01	0.01	462.84	\N	0.0325	1504.22	47792.579999999994	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-02 17:15:56.669164+00	2025-12-02 17:15:56.669164+00	29.95073891625615
696	73	TUBO QUADRADO 50X50X3,00X6000 - 10 BRS	278	5	5.39	0.12	0	4.304454	4.304454	278	7.99	0.18	5.945759	0	38.1303877332642	1196.638212	1652.921002	0.021388	1652.921002	0.015	0.015	33.32	\N	0.05	111.06	2332.42	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-04 19:11:22.272654+00	2025-12-04 19:11:22.272654+00	38.13038773326418
697	73	TUBO QUADRADO 80X80X6,35X6000 - 5 BRS	458	0	6.51	0.18	0	4.844417	4.844417	458	9.09	0.18	6.764324	0	39.63133231511656	2218.742986	3098.0603920000003	0.014769	3098.0603920000003	0.015	0.015	62.45	\N	0.05	208.16	4369.32	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-04 19:11:22.272654+00	2025-12-04 19:11:22.272654+00	39.63133231511655
280	43	TB 20X20X1,254X6000MM GAL	138	1	7.55	0.12	0	6.02943	6.02943	138	9.9	0.12	7.90614	0	31.125827814569533	832.06134	1091.04732	0.057291	1091.04732	0.015	0.015	20.49	\N	0.05	68.31	1435.2	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-02 13:40:11.487938+00	2025-12-02 13:40:11.487938+00	31.12582781456952
698	73	TUBO RETANGULAR 80X60X6,35X6000 - 5 BRS	396	5	6.18	0.12	0	4.935348	4.935348	396	9.36	0.18	6.965244	0	41.1297440423654	1954.397808	2758.236624	0.017589	2758.236624	0.025	0.025	92.66	\N	0.05	185.33	3892.68	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-04 19:11:22.272654+00	2025-12-04 19:11:22.272654+00	41.1297440423654
807	75	25,40 X 2,00 X 6000 	900	1	5.57	0.12	0	4.448202	4.448202	900	7.85	0.18	5.841578	0	31.324476721156095	4003.3818	5257.4202000000005	0.006491	5257.4202000000005	0.015	0.015	105.98	\N	0.0325	229.61	7298.999999999999	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-09 17:51:38.383867+00	2025-12-09 17:51:38.383867+00	31.324476721156103
1497	148	CHAPA #32MM X 2500 X 3000 - 1 PÇ	1884	4	7.8	0.18	0	5.80437	5.801291	1885	9.7	0.12	7.74642	1	33.52924374936544	10935.43308	14602.001699999999	0.00411	14602.001699999999	0.015	0.015	274.27	\N	0.0325	594.25	18887.7	{"has_difference": true, "absolute_difference": 1.0, "percentage_difference": 0.05307855626326964, "formatted_display": "0.1%"}	2025-12-18 13:08:23.983071+00	2025-12-18 13:08:23.983071+00	33.529249305231886
937	102	13- TB 114,30X2,65X6000MM	585	3	5.39	0.12	0	4.304454	4.304454	585	7.55	0.18	5.618333	0	30.523708698013728	2518.10559	3286.724805	0.009604	3286.724805	0.015	0.015	66.25	\N	0.0325	143.54	4563	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-10 17:35:21.473194+00	2025-12-10 17:35:21.473194+00	30.523708698013728
1191	119	140 x 140 x 6,35 x 6000 - 3 BR	500	7	6.59	0.12	0	5.262774	5.262774	500	8.77	0.12	7.003722	0	33.0804248861912	2631.387	3501.861	0.014007	3501.861	0.015	0.015	65.77	\N	0.05	219.25	4605	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-12 17:35:32.133928+00	2025-12-12 17:35:32.133928+00	33.08042488619118
1192	119	120 X 120 X 6,35 X 6000 - 3 BR 	430	7	6.59	0.12	0	5.262774	5.262774	430	8.77	0.12	7.003722	0	33.0804248861912	2262.99282	3011.60046	0.016288	3011.60046	0.015	0.015	56.57	\N	0.05	188.56	3960.3	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-12 17:35:32.133928+00	2025-12-12 17:35:32.133928+00	33.08042488619121
934	101	Tubo Aço Galv.30x30x1,25(250brs)	1710	5	7.1	0.12	0	5.67006	5.540459	1750	9.3	0.12	7.42698	40	34.04990452957056	9695.8026	12997.215	0.004244	12997.215	0.015	0.015	244.13	\N	0.05	813.75	17097.5	{"has_difference": true, "absolute_difference": 40.0, "percentage_difference": 2.3391812865497075, "formatted_display": "2.3%"}	2025-12-10 17:32:44.694601+00	2025-12-10 17:32:44.694601+00	34.04991351618483
935	101	Tubo Aço Galv.40x40x1,25(250brs)	2300	5	7.1	0.12	0	5.67006	5.573136	2340	9.3	0.12	7.42698	40	33.26392896207808	13041.138	17379.1332	0.003174	17379.1332	0.015	0.015	326.43	\N	0.05	1088.1	22861.8	{"has_difference": true, "absolute_difference": 40.0, "percentage_difference": 1.7391304347826086, "formatted_display": "1.7%"}	2025-12-10 17:32:44.694601+00	2025-12-10 17:32:44.694601+00	33.2639314145744
936	101	Perfil U enrijecido Galv.75 x 40 x 1,25(80Brs)	710	5	10.3	0.18	0	7.664745	7.404039	735	12.1	0.12	9.66306	25	30.510657763958292	5441.96895	7102.349099999999	0.013147	7102.349099999999	0.015	0.015	133.4	\N	0.0325	289.04	9180.15	{"has_difference": true, "absolute_difference": 25.0, "percentage_difference": 3.5211267605633805, "formatted_display": "3.5%"}	2025-12-10 17:32:44.694601+00	2025-12-10 17:32:44.694601+00	30.510650929017125
1193	119	120 X 80 X 6,35 X 6000 - 1 BR	119	7	6.13	0.12	0	4.895418	4.895418	119	8.27	0.12	6.604422	0	34.91027732463296	582.554742	785.926218	0.055499	785.926218	0.015	0.015	14.76	\N	0.05	49.21	1032.92	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-12 17:35:32.133928+00	2025-12-12 17:35:32.133928+00	34.91027732463294
1194	119	100 X 50 X 6,35 X 6000 - 4 BR	358	7	6.13	0.12	0	4.895418	4.895418	358	8.27	0.12	6.604422	0	34.91027732463296	1752.559644	2364.383076	0.018448	2364.383076	0.015	0.015	44.41	\N	0.05	148.03	3107.44	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-12 17:35:32.133928+00	2025-12-12 17:35:32.133928+00	34.910277324632965
579	52	F CHT 4X1/4X6000MM	1	0	7.1	0.12	2.41	8.08006	8.08006	1	13.2	0.12	10.54152	0	30.463387648111524	8.08006	10.54152	10.54152	10.54152	0.015	0.015	0.2	\N	0	0	13.2	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-03 17:08:25.087873+00	2025-12-03 17:08:25.087873+00	30.46338764811154
580	52	F CHT 2X3/8X6000MM	1	0	7.1	0.12	2.41	8.08006	8.08006	1	13.2	0.12	10.54152	0	30.463387648111524	8.08006	10.54152	10.54152	10.54152	0.015	0.015	0.2	\N	0	0	13.2	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-03 17:08:25.087873+00	2025-12-03 17:08:25.087873+00	30.46338764811154
581	52	F CHT 3X3/8X6000MM	1	0	7.1	0.12	2.41	8.08006	8.08006	1	13.2	0.12	10.54152	0	30.463387648111524	8.08006	10.54152	10.54152	10.54152	0.015	0.015	0.2	\N	0	0	13.2	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-03 17:08:25.087873+00	2025-12-03 17:08:25.087873+00	30.46338764811154
582	52	F CHT 2X5/16X6000MM	1	0	7.1	0.12	2.41	8.08006	8.08006	1	13.2	0.18	9.82278	0	21.568156672103918	8.08006	9.82278	9.82278	9.82278	0.01	0.01	0.13	\N	0	0	13.2	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-03 17:08:25.087873+00	2025-12-03 17:08:25.087873+00	21.56815667210392
583	52	F CHT 2X5/8X6000MM	1	0	7.1	0.12	2.41	8.08006	8.08006	1	13.2	0.12	10.54152	0	30.463387648111524	8.08006	10.54152	10.54152	10.54152	0.015	0.015	0.2	\N	0	0	13.2	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-03 17:08:25.087873+00	2025-12-03 17:08:25.087873+00	30.46338764811154
584	52	F CHT 2X3/4X6000MM	1	0	7.1	0.12	2.41	8.08006	8.08006	1	13.2	0.18	9.82278	0	21.568156672103918	8.08006	9.82278	9.82278	9.82278	0.01	0.01	0.13	\N	0	0	13.2	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-03 17:08:25.087873+00	2025-12-03 17:08:25.087873+00	21.56815667210392
585	52	F CHT 3X5/16X6000MM	1	0	7.1	0.12	2.41	8.08006	8.08006	1	13.2	0.12	10.54152	0	30.463387648111524	8.08006	10.54152	10.54152	10.54152	0.015	0.015	0.2	\N	0	0	13.2	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-03 17:08:25.087873+00	2025-12-03 17:08:25.087873+00	30.46338764811154
1195	119	120 X 80 X 6,3 X 6000 - 9 BR	1076	7	6.13	0.12	0	4.895418	4.895418	1076	8.27	0.12	6.604422	0	34.91027732463296	5267.469768	7106.358071999999	0.006138	7106.358071999999	0.015	0.015	133.48	\N	0.05	444.93	9339.68	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-12 17:35:32.133928+00	2025-12-12 17:35:32.133928+00	34.91027732463294
1196	119	80 X 80 X 6,35 X 6000 - 10 BR	957	7	6.55	0.12	0	5.23083	5.23083	957	8.77	0.12	7.003722	0	33.89312977099237	5005.90431	6702.561954	0.007318	6702.561954	0.015	0.015	125.89	\N	0.05	419.64	8813.970000000001	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-12 17:35:32.133928+00	2025-12-12 17:35:32.133928+00	33.89312977099237
1197	119	120 X 80 X 6,35 X 6000 - 10 BR	1196	7	6.13	0.12	0	4.895418	4.895418	1196	8.27	0.12	6.604422	0	34.91027732463296	5854.919928	7898.888712	0.005522	7898.888712	0.015	0.015	148.36	\N	0.05	494.55	10381.279999999999	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-12 17:35:32.133928+00	2025-12-12 17:35:32.133928+00	34.91027732463294
1198	117	152,40 X 3,00 3 BRS	201	3	5.38	0.12	0	4.296468	4.296468	201	7.9	0.18	5.878785	0	36.82832037850625	863.590068	1181.635785	0.029248	1181.635785	0.015	0.015	23.82	\N	0.0325	51.61	1640.16	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-12 17:39:38.794015+00	2025-12-12 17:39:38.794015+00	36.82832037850625
1199	117	40X40X2,00 - 03 BRS	45	3	5.58	0.12	0	4.456188	4.456188	45	8.24	0.18	6.131796	0	37.60182469859889	200.52846	275.93082	0.136262	275.93082	0.015	0.015	5.56	\N	0.05	18.54	389.25	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-12 17:39:38.794015+00	2025-12-12 17:39:38.794015+00	37.6018246985989
1347	45	120 -TB 70X70X3X6000MM	4712	4	5.37	0.18	0	4.199614	4.199614	4712	7	0.12	5.5902	0	33.11223364814004	19788.581168	26341.0224	0.001186	26341.0224	0.015	0.015	494.76	\N	0.05	1649.2	34633.2	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-16 16:31:10.577727+00	2025-12-16 16:31:10.577727+00	33.11223364814004
1348	45	116- TB RED 50.80X3X6000MM	2535	4	5.46	0.12	0	4.563884	4.563884	2535	7.3	0.12	5.82978	0	27.737251867050084	11569.44594	14778.492300000002	0.0023	14778.492300000002	0.01	0.01	185.06	\N	0.05	925.28	19443.45	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-16 16:31:10.577727+00	2025-12-16 16:31:10.577727+00	27.737251867050094
517	55	CANTONEIRA 2"X3/8 X 6000 - 6 BRS	252	3	6.45	0.12	0	5.15097	5.15097	252	8.19	0.12	6.540534	0	26.976744186046513	1298.04444	1648.214568	0.025955	1648.214568	0.01	0.01	20.64	\N	0	0	2063.8799999999997	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-03 14:03:29.66989+00	2025-12-03 14:03:29.66989+00	26.97674418604652
586	52	F CHT 4X5/16X6000MM	1	0	7.1	0.12	2.41	8.08006	8.08006	1	13.2	0.12	10.54152	0	30.463387648111524	8.08006	10.54152	10.54152	10.54152	0.015	0.015	0.2	\N	0	0	13.2	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-03 17:08:25.087873+00	2025-12-03 17:08:25.087873+00	30.46338764811154
587	52	F CHT 2X1/28X6000MM	1	0	7.1	0.12	2.41	8.08006	8.08006	1	13.2	0.12	10.54152	0	30.463387648111524	8.08006	10.54152	10.54152	10.54152	0.015	0.015	0.2	\N	0	0	13.2	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-03 17:08:25.087873+00	2025-12-03 17:08:25.087873+00	30.46338764811154
588	52	F CHT 3X1/2X6000MM	1	0	7.1	0.12	2.41	8.08006	8.08006	1	13.2	0.12	10.54152	0	30.463387648111524	8.08006	10.54152	10.54152	10.54152	0.015	0.015	0.2	\N	0	0	13.2	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-03 17:08:25.087873+00	2025-12-03 17:08:25.087873+00	30.46338764811154
589	52	F CHT 3X3/4X6000MM	1	0	7.1	0.12	2.41	8.08006	8.08006	1	13.2	0.18	9.82278	0	21.568156672103918	8.08006	9.82278	9.82278	9.82278	0.01	0.01	0.13	\N	0	0	13.2	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-03 17:08:25.087873+00	2025-12-03 17:08:25.087873+00	21.56815667210392
590	52	F CHT 4X3/4X6000MM	1	0	7.1	0.12	2.41	8.08006	8.08006	1	13.2	0.18	9.82278	0	21.568156672103918	8.08006	9.82278	9.82278	9.82278	0.01	0.01	0.13	\N	0	0	13.2	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-03 17:08:25.087873+00	2025-12-03 17:08:25.087873+00	21.56815667210392
591	52	F CHT 4X1X6000MM	1	0	7.1	0.12	2.41	8.08006	8.08006	1	13.2	0.18	9.82278	0	21.568156672103918	8.08006	9.82278	9.82278	9.82278	0.01	0.01	0.13	\N	0	0	13.2	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-03 17:08:25.087873+00	2025-12-03 17:08:25.087873+00	21.56815667210392
592	52	F CHT1 X3X6000MM	1	0	7.1	0.12	2.41	8.08006	8.08006	1	13.2	0.18	9.82278	0	21.568156672103918	8.08006	9.82278	9.82278	9.82278	0.01	0.01	0.13	\N	0	0	13.2	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-03 17:08:25.087873+00	2025-12-03 17:08:25.087873+00	21.56815667210392
938	99	TB 70XX70X3X6000MM-120	4712	2	5.37	0.12	0	4.288482	4.288482	4712	7	0.12	5.5902	0	30.353817504655495	20207.327184	26341.0224	0.001186	26341.0224	0.015	0.015	494.76	\N	0.05	1649.2	34633.2	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-10 17:56:07.214713+00	2025-12-10 17:56:07.214713+00	30.35381750465549
711	62	203,20 X 4,75 X 6000 - 14 BR	2010	5	6.55	0.12	0	5.23083	5.23083	2010	9.27	0.19	6.814145	0	30.268905699477905	10513.9683	13696.43145	0.00339	13696.43145	0.015	0.015	279.49	\N	0.0325	605.56	19235.7	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-05 16:59:08.419245+00	2025-12-05 16:59:08.419245+00	30.268905699477887
943	104	50X50X1,50	3	2	87	0.12	0	69.4782	69.4782	3	121.8	0.12	97.26948	0	40	208.4346	291.80844	32.42316	291.80844	0.05	0.05	18.27	\N	0.05	18.27	383.67	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-10 20:41:31.435524+00	2025-12-10 20:41:31.435524+00	40.000000000000014
717	78	Tubo RT 70x30x2,00	218	3	5.47	0.12	0	4.368342	4.251333	224	8.1	0.18	6.027615	6	41.78176586026077	952.298556	1350.18576	0.026909	1350.18576	0.025	0.025	45.36	\N	0.05	90.72	1906.24	{"has_difference": true, "absolute_difference": 6.0, "percentage_difference": 2.7522935779816513, "formatted_display": "2.8%"}	2025-12-05 17:15:53.932118+00	2025-12-05 17:15:53.932118+00	41.78177122007525
718	78	Tubo QD 30x30x1,20	27	3	6.17	0.12	0	4.927362	4.751385	28	8.5	0.18	6.325275	1	33.124867801704134	133.038774	177.10770000000002	0.225903	177.10770000000002	0.015	0.015	3.57	\N	0.05	11.9	250.04	{"has_difference": true, "absolute_difference": 1.0, "percentage_difference": 3.7037037037037037, "formatted_display": "3.7%"}	2025-12-05 17:15:53.932118+00	2025-12-05 17:15:53.932118+00	33.12487380558695
719	80	chapa exp 5/16 3x1,20 malha 50x100	5	0	715	0.18	0	532.06725	532.06725	5	931	0.18	692.80365	0	30.20979020979021	2660.33625	3464.0182499999996	138.56073	3464.0182499999996	0.015	0.015	69.83	\N	0.0325	151.29	4806.3	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-05 17:46:22.529176+00	2025-12-05 17:46:22.529176+00	30.2097902097902
944	104	50X20X1,55	3	2	71	0.12	0	56.7006	56.7006	3	99.4	0.12	79.38084	0	40	170.1018	238.14252000000002	26.46028	238.14252000000002	0.025	0.025	7.46	\N	0.05	14.91	313.11	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-10 20:41:31.435524+00	2025-12-10 20:41:31.435524+00	40.000000000000014
945	104	20X20X1,50	12	2	33.25	0.12	0	26.55345	26.55345	12	46.55	0.12	37.17483	0	40	318.6414	446.09796	3.097903	446.09796	0.05	0.05	27.93	\N	0.05	27.93	586.5600000000001	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-10 20:41:31.435524+00	2025-12-10 20:41:31.435524+00	40.000000000000014
608	47	30x30x1,95 GALVANIZADO	190	3	89.25	0.18	0	66.415388	66.415388	190	113.3	0.12	90.48138	0	36.23556637205824	12618.92372	17191.4622	0.476218	17191.4622	0.015	0.015	322.91	\N	0.05	1076.35	22604.3	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-03 17:59:08.608136+00	2025-12-03 17:59:08.608136+00	36.235566372058244
724	76	100 X 100 X 2,00 X 6000 - 6 BR	226	1	6.28	0.18	0	4.673262	4.673262	226	8.2	0.18	6.10203	0	30.573248407643312	1056.157212	1379.05878	0.027	1379.05878	0.015	0.015	27.8	\N	0.05	92.66	1945.86	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-09 00:58:53.599169+00	2025-12-09 00:58:53.599169+00	30.573248407643305
725	76	50 X 30 X 1,20 X 6000 - 4 BR	36	1	6.17	0.12	0	4.927362	4.927362	36	8.8	0.18	6.54852	0	32.90113452188007	177.385032	235.74671999999998	0.181903	235.74671999999998	0.015	0.015	4.75	\N	0.05	15.84	332.64	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-09 00:58:53.599169+00	2025-12-09 00:58:53.599169+00	32.90113452188006
726	76	PERFIL U 3'' X 2,65 X 6000 - 16 BR	290	1	5.49	0.12	0	4.384314	4.384314	290	7.8	0.18	5.80437	0	32.38946845504223	1271.45106	1683.2673	0.020015	1683.2673	0.015	0.015	33.93	\N	0	0	2262	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-09 00:58:53.599169+00	2025-12-09 00:58:53.599169+00	32.389468455042206
617	53	080 X 040 X 4,75 X 6000 - 4 BR	207	1	5.9	0.12	0	4.71174	4.71174	207	8.5	0.18	6.325275	0	34.24499229583976	975.33018	1309.3319250000002	0.030557	1309.3319250000002	0.015	0.015	26.39	\N	0.05	87.98	1848.51	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-03 18:55:28.433542+00	2025-12-03 18:55:28.433542+00	34.24499229583977
618	53	080 X 080 X 2,00 X 6000 - 2 BR	121	1	5.88	0.12	0	4.695768	4.695768	121	8.55	0.18	6.362483	0	35.493980963284386	568.187928	769.860443	0.052583	769.860443	0.015	0.015	15.52	\N	0.05	51.73	1086.5800000000002	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-03 18:55:28.433542+00	2025-12-03 18:55:28.433542+00	35.49398096328438
625	64	TUBO QUADRADO 60X60X2,00X6000 - 1 BR	22	5	5.47	0.12	0	4.368342	4.368342	22	7.87	0.18	5.856461	0	34.06599117010527	96.103524	128.842142	0.266203	128.842142	0.015	0.015	2.6	\N	0.05	8.66	181.72	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-03 19:21:28.520923+00	2025-12-03 19:21:28.520923+00	34.06599117010527
626	64	TUBO REDONDO 25,40X2,00X6000 - 1 BR	7	0	5.56	0.12	0	4.440216	4.440216	7	7.99	0.18	5.945759	0	33.90697659753489	31.081512	41.620312999999996	0.849394	41.620312999999996	0.015	0.015	0.84	\N	0.0325	1.82	57.75	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-03 19:21:28.520923+00	2025-12-03 19:21:28.520923+00	33.90697659753488
627	64	PERFIL US 100X40X3,00	752	0	5.3	0.12	0	4.23258	4.23258	752	7.87	0.18	5.856461	0	38.36622107556148	3182.90016	4404.058672	0.007788	4404.058672	0.015	0.015	88.77	\N	0	0	5918.24	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-03 19:21:28.520923+00	2025-12-03 19:21:28.520923+00	38.36622107556147
645	39	PERFIL I 6'' X 2ª ALMA - 30 BR 	4110	4	7.5	0.12	0	5.9895	5.8086	4238	9.47	0.12	7.562742	128	30.1990496849499	24616.845	32050.900596	0.001785	32050.900596	0.015	0.015	602.01	\N	0	0	40133.86	{"has_difference": true, "absolute_difference": 128.0, "percentage_difference": 3.1143552311435525, "formatted_display": "3.1%"}	2025-12-04 13:17:22.214654+00	2025-12-04 13:17:22.214654+00	30.199059205190594
646	39	VIGA W 200 X 19,30 - 30 BR 	3558	4	8	0.12	0	6.3888	6.203971	3664	10.17	0.12	8.121762	106	30.912314064653106	22731.3504	29758.135968000002	0.002217	29758.135968000002	0.015	0.015	558.94	\N	0	0	37262.88	{"has_difference": true, "absolute_difference": 106.0, "percentage_difference": 2.9792017987633503, "formatted_display": "3.0%"}	2025-12-04 13:17:22.214654+00	2025-12-04 13:17:22.214654+00	30.912310286677915
647	39	PERFIL I 4'' X 2ª ALMA - 30 BR 	2311	4	7.5	0.12	0	5.9895	5.815855	2380	9.47	0.12	7.562742	69	30.03663261893565	13841.7345	17999.325960000002	0.003178	17999.325960000002	0.015	0.015	338.08	\N	0	0	22538.600000000002	{"has_difference": true, "absolute_difference": 69.0, "percentage_difference": 2.98572046733016, "formatted_display": "3.0%"}	2025-12-04 13:17:22.214654+00	2025-12-04 13:17:22.214654+00	30.036636376748895
941	103	VIGA U 6'' X 1ª ALMA X 6000 - 4 BR	301	3	7.5	0.12	0	5.9895	5.9895	301	9.8	0.12	7.82628	0	30.666666666666664	1802.8395	2355.71028	0.026001	2355.71028	0.015	0.015	44.25	\N	0	0	2949.8	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-10 19:30:07.674201+00	2025-12-10 19:30:07.674201+00	30.666666666666643
1479	129	30- tb 80x80cx3x6000mm	1352	4	5.37	0.18	0	3.996086	3.996086	1352	7.2	0.18	5.35788	0	34.07819551431076	5402.708272	7243.85376	0.003963	7243.85376	0.015	0.015	146.02	\N	0.05	486.72	10221.119999999999	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-18 11:47:01.853355+00	2025-12-18 11:47:01.853355+00	34.07819551431075
942	103	VIGA U 8'' X 1ª ALMA X 6000 - 2 BR	338	3	8.95	0.12	0	7.14747	7.14747	338	11.7	0.12	9.34362	0	30.726256983240223	2415.84486	3158.14356	0.027644	3158.14356	0.015	0.015	59.32	\N	0	0	3954.6	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-10 19:30:07.674201+00	2025-12-10 19:30:07.674201+00	30.72625698324021
720	81	Tubo Qd 50x50x2,00 ( 5brs) 	91	3	5.58	0.12	0	4.456188	4.268559	95	8.5	0.18	6.325275	4	48.18291137594678	405.513108	600.9011250000001	0.066582	600.9011250000001	0.025	0.025	20.19	\N	0.05	40.38	848.35	{"has_difference": true, "absolute_difference": 4.0, "percentage_difference": 4.395604395604396, "formatted_display": "4.4%"}	2025-12-05 19:23:37.729107+00	2025-12-05 19:23:37.729107+00	48.182910279684506
778	67	TB 48,30X5,60X6000MM	365	0	6.17	0.12	0	4.927362	4.927362	365	8	0.12	6.3888	0	29.65964343598055	1798.48713	2331.912	0.017504	2331.912	0.01	0.01	29.2	\N	0.0325	94.9	3014.9	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-09 16:30:03.602101+00	2025-12-09 16:30:03.602101+00	29.65964343598053
782	74	TB RED SCH40 4"X6000MM	1986	3	6.4	0.18	0	4.76256	4.76256	1986	8.4	0.18	6.25086	0	31.25	9458.44416	12414.20796	0.003147	12414.20796	0.015	0.015	250.24	\N	0.0325	542.18	17218.62	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-09 16:31:50.079737+00	2025-12-09 16:31:50.079737+00	31.25
1002	87	25 x 25 x 2,00 x 6000 - 4 br	37	1	5.47	0.12	0	4.368342	4.368342	37	8.85	0.18	6.585728	0	50.76035713320981	161.628654	243.671936	0.177993	243.671936	0.03	0.03	9.82	\N	0.05	16.37	343.72999999999996	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-11 16:30:08.412636+00	2025-12-11 16:30:08.412636+00	50.76035713320979
1003	87	31,75 x 1,50 x 6000 - 2 br 	13	1	6.27	0.12	0	5.007222	5.007222	13	9.8	0.18	7.29267	0	45.64303320284181	65.093886	94.80471	0.560975	94.80471	0.025	0.025	3.19	\N	0.0325	4.14	131.56	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-11 16:30:08.412636+00	2025-12-11 16:30:08.412636+00	45.64303320284182
1008	27	120 x 60 x 2,00 x 60000 - 100 br	3391	5	6.29	0.18	0	4.680704	4.680704	3391	8.27	0.18	6.154121	0	31.47853399830453	15872.267264	20868.624311	0.001815	20868.624311	0.015	0.015	420.65	\N	0.05	1402.18	29433.879999999997	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-11 16:38:31.693955+00	2025-12-11 16:38:31.693955+00	31.478533998304513
1013	71	TB 1.1/2'' SCH 10 - 10 BARRAS	184	1	5.9	0.12	0	4.71174	4.71174	184	8.45	0.18	6.288068	0	33.45532648236108	866.96016	1157.004512	0.034174	1157.004512	0.015	0.015	23.32	\N	0.0325	50.53	1604.48	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-11 16:39:41.37601+00	2025-12-11 16:39:41.37601+00	33.455326482361095
1207	122	TUBO RETANGULAR 50X30X3,00X6000 - 9 BRS	227	0	5.37	0.12	0	4.288482	4.288482	227	8.14	0.18	6.057381	0	41.24767225325884	973.485414	1375.025487	0.026684	1375.025487	0.025	0.025	46.19	\N	0.05	92.39	1940.8500000000001	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-12 18:04:12.024952+00	2025-12-12 18:04:12.024952+00	41.24767225325885
947	105	TUBO S/C 5'' X 12,70 X 1000MM	45	4	13.2	0.18	0	9.82278	9.82278	45	25.4	0.12	20.28444	0	106.5040650406504	442.0251	912.7998	0.450765	912.7998	0.05	0.05	57.15	\N	0.0325	37.15	1180.35	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-11 13:21:15.45795+00	2025-12-11 13:21:15.45795+00	106.5040650406504
623	63	PERFIL US 127X50X4,25X6000 - 6 BRS	258	0	6.94	0.18	0	5.164401	5.164401	258	8.99	0.18	6.689909	0	29.53891458080037	1332.415458	1725.996522	0.02593	1725.996522	0.01	0.01	23.19	\N	0	0	2319.42	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-03 19:17:36.148706+00	2025-12-03 19:17:36.148706+00	29.53891458080036
624	63	PERFIL US 75X40X3,00X6000 - 15 BRS	285	0	5.3	0.12	0	4.23258	4.23258	285	7.46	0.18	5.551359	0	31.157804459691253	1206.2853	1582.137315	0.019478	1582.137315	0.015	0.015	31.89	\N	0	0	2126.1	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-03 19:17:36.148706+00	2025-12-03 19:17:36.148706+00	31.157804459691253
632	65	CHAPA LISA 1200X3000X6,30 - 1 PÇ	187	2	6	0.18	0	4.4649	4.4649	187	7.2	0.12	5.74992	0	28.780487804878046	834.9363	1075.23504	0.030748	1075.23504	0.01	0.01	13.46	\N	0.0325	43.76	1389.4099999999999	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-03 20:07:17.375971+00	2025-12-03 20:07:17.375971+00	28.780487804878053
633	65	TUBO QUADRADO 50X50X2,25X6000 - 110 BRS	2090	5	5.58	0.12	0	4.456188	4.456188	2090	7.25	0.12	5.78985	0	29.92831541218638	9313.43292	12100.7865	0.00277	12100.7865	0.01	0.01	151.53	\N	0.05	757.63	15904.900000000001	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-03 20:07:17.375971+00	2025-12-03 20:07:17.375971+00	29.92831541218639
634	65	TUBO QUADRADO 20X20X1,25X6000 ZINCADO - 198 BRS	1188	0	7.55	0.12	0	6.02943	6.02943	1188	9.82	0.12	7.842252	0	30.066225165562916	7162.96284	9316.595376000001	0.006601	9316.595376000001	0.015	0.015	174.99	\N	0.05	583.31	12248.28	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-03 20:07:17.375971+00	2025-12-03 20:07:17.375971+00	30.06622516556292
657	13	Tubo de aço carbono SCH40 sem costura de 8'' - 7 br	1840	3	11.9	0.18	0	8.855385	8.855385	1840	14.9	0.12	11.89914	0	34.3717974994876	16293.9084	21894.417599999997	0.006467	21894.417599999997	0.015	0.015	411.24	\N	0	0	27416	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-04 16:50:05.835922+00	2025-12-04 16:50:05.835922+00	34.37179749948758
658	13	Tubo de aço carbono SCH40 sem costura de 12'' - 1 br 	604	3	11.9	0.18	0	8.855385	8.855385	604	14.9	0.12	11.89914	0	34.3717974994876	5348.65254	7187.080559999999	0.019701	7187.080559999999	0.015	0.015	134.99	\N	0	0	8999.6	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-04 16:50:05.835922+00	2025-12-04 16:50:05.835922+00	34.37179749948758
659	26	250 x 150 x 6,35 x 6000 - 12 br	2767	1	6.57	0.12	0	5.246802	5.246802	2767	8.97	0.18	6.675026	0	27.220848051822806	14517.901134	18469.796942	0.002412	18469.796942	0.01	0.01	248.2	\N	0.05	1241	26065.14	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-04 16:50:48.011516+00	2025-12-04 16:50:48.011516+00	27.22084805182281
660	30	CANTONEIRA 2'' X 1/8 - 13 BR	194	2	6.6	0.12	0	5.27076	5.27076	194	8.7	0.12	6.94782	0	31.818181818181817	1022.52744	1347.87708	0.035814	1347.87708	0.015	0.015	25.32	\N	0	0	1687.8	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-04 16:51:20.83298+00	2025-12-04 16:51:20.83298+00	31.818181818181813
661	30	CHATO 2'' X 1/8 - 26 BR 	203	2	6.55	0.12	0	5.23083	5.23083	203	8.5	0.12	6.7881	0	29.770992366412212	1061.85849	1377.9843	0.033439	1377.9843	0.01	0.01	17.26	\N	0	0	1725.5	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-04 16:51:20.83298+00	2025-12-04 16:51:20.83298+00	29.77099236641221
662	40	TB S/C 4'' SCH 40 - 25 BR 	2490	5	11	0.18	0	8.18565	8.18565	2490	14.87	0.205	10.728147	0	31.06041670484323	20382.2685	26713.08603	0.004308	26713.08603	0.015	0.015	555.39	\N	0	0	37026.299999999996	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-04 16:51:46.148991+00	2025-12-04 16:51:46.148991+00	31.06041670484323
663	40	TB S/C 6'' SCH 40 - 25 BR 	4380	5	11	0.18	0	8.18565	8.18565	4380	14.87	0.205	10.728147	0	31.06041670484323	35853.147	46989.283859999996	0.002449	46989.283859999996	0.015	0.015	976.96	\N	0	0	65130.6	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-04 16:51:46.148991+00	2025-12-04 16:51:46.148991+00	31.06041670484323
664	40	PERFIL I 4'' X 2ª ALMA - 50 BR 	3910	5	7.5	0.12	0	5.9895	5.9895	3910	10.8	0.205	7.791795	0	30.09090909090909	23418.945	30465.918449999997	0.001993	30465.918449999997	0.015	0.015	633.42	\N	0	0	42228	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-04 16:51:46.148991+00	2025-12-04 16:51:46.148991+00	30.09090909090908
665	40	PERFIL I 6'' X 2ª ALMA - 50 BR 	6800	5	7.5	0.12	0	5.9895	5.9895	6800	10.8	0.205	7.791795	0	30.09090909090909	40728.6	52984.206	0.001146	52984.206	0.015	0.015	1101.6	\N	0	0	73440	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-04 16:51:46.148991+00	2025-12-04 16:51:46.148991+00	30.0909090909091
666	40	BARRA CHATA 2'' X 3/16 - 50 BR 	590	5	6.5	0.12	0	5.1909	5.1909	590	9.47	0.205	6.83225	0	31.619757652815505	3062.631	4031.0275	0.01158	4031.0275	0.015	0.015	83.81	\N	0	0	5587.3	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-04 16:51:46.148991+00	2025-12-04 16:51:46.148991+00	31.619757652815505
954	86	TUBO REDONDO 38,10X1,50X6000 - 124 BRS	1149	5	6.27	0.12	0	5.007222	5.007222	1149	8.15	0.12	6.50859	0	29.98405103668261	5753.298078	7478.369909999999	0.005665	7478.369909999999	0.01	0.01	93.64	\N	0.0325	304.34	9663.09	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-11 13:47:10.764146+00	2025-12-11 13:47:10.764146+00	29.9840510366826
955	86	FERRO CHATO 2" X 1/4 X 6000 - 32 BRS	512	2	6.5	0.12	0	5.1909	5.1909	512	8.45	0.12	6.74817	0	30	2657.7408	3455.06304	0.01318	3455.06304	0.015	0.015	64.9	\N	0	0	4326.4	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-11 13:47:10.764146+00	2025-12-11 13:47:10.764146+00	30.000000000000004
1495	22	PT 300X100X3X6000MM	3330	7	9.3	0.18	0	6.920595	6.920595	3330	12.2	0.18	9.07863	0	31.182795698924732	23045.58135	30231.837900000002	0.002726	30231.837900000002	0.015	0.015	609.39	\N	0	0	40626	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-18 12:40:07.410269+00	2025-12-18 12:40:07.410269+00	31.18279569892475
1387	139	sch 80 S/C API 5L 1/2	30	0	14.19	0.04	0	12.362328	12.362328	30	19.87	0.04	17.310744	0	40.02818886539817	370.86984	519.32232	0.577025	519.32232	0.025	0.025	14.9	\N	0	0	596.1	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-16 18:11:46.639752+00	2025-12-16 18:11:46.639752+00	40.028188865398164
1388	139	FERRO RED 2" 11 BRS	1056	0	6.5	0.12	0	5.1909	5.1909	1056	8.45	0.12	6.74817	0	30	5481.5904	7126.06752	0.00639	7126.06752	0.015	0.015	133.85	\N	0	0	8923.199999999999	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-16 18:11:46.639752+00	2025-12-16 18:11:46.639752+00	29.999999999999982
1389	139	FERRO RED  1" 89 brs	2136	0	6.5	0.12	0	5.1909	5.1909	2136	8.45	0.12	6.74817	0	30	11087.7624	14414.09112	0.003159	14414.09112	0.015	0.015	270.74	\N	0	0	18049.199999999997	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-16 18:11:46.639752+00	2025-12-16 18:11:46.639752+00	30.000000000000004
1390	139	100X100X6,35 150 BRS 	17100	0	6.35	0.12	0	5.07111	5.07111	17100	8.6	0.12	6.86796	0	35.43307086614173	86715.981	117442.116	0.000402	117442.116	0.015	0.015	2205.9	\N	0.05	7353	154413	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-16 18:11:46.639752+00	2025-12-16 18:11:46.639752+00	35.43307086614173
863	91	100 X 50 X 2,65 X 6000 - 4 BR	150	1	5.9	0.12	0	4.71174	4.71174	150	8.55	0.18	6.362483	0	35.03467933290037	706.761	954.3724500000001	0.042417	954.3724500000001	0.015	0.015	19.24	\N	0.05	64.13	1347	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-09 18:37:31.439547+00	2025-12-09 18:37:31.439547+00	35.03467933290039
864	91	120 X 120 X 4,75 X 6000 - 4 BR	430	1	6.02	0.12	0	4.807572	4.807572	430	8.72	0.18	6.488988	0	34.974327997583806	2067.25596	2790.26484	0.015091	2790.26484	0.015	0.015	56.24	\N	0.05	187.48	3938.8	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-09 18:37:31.439547+00	2025-12-09 18:37:31.439547+00	34.9743279975838
865	91	150 X 100 X 4,75 X 6000 - 3 BR	335	1	6.52	0.12	0	5.206872	5.206872	335	9.45	0.18	7.032218	0	35.0564792067099	1744.30212	2355.7930300000003	0.020992	2355.7930300000003	0.015	0.015	47.49	\N	0.05	158.29	3323.2	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-09 18:37:31.439547+00	2025-12-09 18:37:31.439547+00	35.05647920670991
745	49	Perfil H 200x35,90 (11brs)	2370	7	8.4	0.18	0	6.25086	6.224596	2380	9.3	0.07	7.848968	10	26.096022938677464	14814.5382	18680.543840000002	0.003298	18680.543840000002	0.01	0.01	221.34	\N	0	0	22134	{"has_difference": true, "absolute_difference": 10.0, "percentage_difference": 0.4219409282700422, "formatted_display": "0.4%"}	2025-12-09 14:06:22.592238+00	2025-12-09 14:06:22.592238+00	26.0960253219368
746	49	Perfil W 250x17,90 (43brs)	4620	7	7.8	0.18	0	5.80437	5.766922	4650	8.7	0.07	7.342583	30	27.32239139006909	26816.1894	34143.01095	0.001579	34143.01095	0.01	0.01	404.55	\N	0	0	40455	{"has_difference": true, "absolute_difference": 30.0, "percentage_difference": 0.6493506493506493, "formatted_display": "0.6%"}	2025-12-09 14:06:22.592238+00	2025-12-09 14:06:22.592238+00	27.322381419337695
747	49	Perfil U 200x50x4,75 ( 8brs)	510	7	6.2	0.18	0	4.61373	4.525004	520	6.8	0.07	5.73903	10	26.82928015091257	2353.0023	2984.2956	0.011037	2984.2956	0.01	0.01	35.36	\N	0	0	3536	{"has_difference": true, "absolute_difference": 10.0, "percentage_difference": 1.9607843137254901, "formatted_display": "2.0%"}	2025-12-09 14:06:22.592238+00	2025-12-09 14:06:22.592238+00	26.82926829268293
748	49	Perfil U 150x50x3,04(15Brs)	510	7	6.2	0.18	0	4.61373	4.525004	520	6.8	0.07	5.73903	10	26.82928015091257	2353.0023	2984.2956	0.011037	2984.2956	0.01	0.01	35.36	\N	0	0	3536	{"has_difference": true, "absolute_difference": 10.0, "percentage_difference": 1.9607843137254901, "formatted_display": "2.0%"}	2025-12-09 14:06:22.592238+00	2025-12-09 14:06:22.592238+00	26.82926829268293
749	49	Chapa Lisa 1200x2000x3,00(10pçs)	590	7	6	0.18	0	4.4649	4.31851	610	6.8	0.07	5.73903	20	32.89375270637326	2634.291	3500.8082999999997	0.009408	3500.8082999999997	0.015	0.015	62.22	\N	0.0325	134.81	4282.2	{"has_difference": true, "absolute_difference": 20.0, "percentage_difference": 3.389830508474576, "formatted_display": "3.4%"}	2025-12-09 14:06:22.592238+00	2025-12-09 14:06:22.592238+00	32.89375775113681
754	84	02 CANTONEIRAS 3X1/4X6000MM	90	1	7.1	0.12	0	5.67006	5.67006	90	15	0.12	11.979	0	111.26760563380283	510.3054	1078.11	0.1331	1078.11	0.05	0.05	67.5	\N	0	0	1350	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-09 16:26:08.830976+00	2025-12-09 16:26:08.830976+00	111.2676056338028
667	40	CANTONEIRA 2.1/2'' X 1/4 - 50 BR 	1890	5	7.1	0.12	0	5.67006	5.67006	1890	10.27	0.205	7.40942	0	30.67621859380677	10716.4134	14003.8038	0.00392	14003.8038	0.015	0.015	291.15	\N	0	0	19410.3	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-04 16:51:46.148991+00	2025-12-04 16:51:46.148991+00	30.67621859380678
956	93	TUBO RETANGULAR 50X30X2,65X6000 - 50 BRS	1100	0	5.37	0.12	0	4.288482	4.288482	1100	7.38	0.18	5.491827	0	28.059928897917725	4717.3302	6041.0097	0.004993	6041.0097	0.01	0.01	81.18	\N	0.05	405.9	8525	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-11 13:47:58.933731+00	2025-12-11 13:47:58.933731+00	28.059928897917708
757	83	TB 40X40X4,75X6000MM	333	0	6.23	0.18	0	4.636055	4.636055	333	8.2	0.12	6.54852	0	41.25199118647212	1543.806315	2180.6571599999997	0.019665	2180.6571599999997	0.025	0.025	68.27	\N	0.05	136.53	2867.1299999999997	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-09 16:27:08.324736+00	2025-12-09 16:27:08.324736+00	41.25199118647209
758	83	TB 30X30X2X6000MM	22	0	6.45	0.12	0	5.15097	5.15097	22	8.5	0.12	6.7881	0	31.782945736434108	113.32134	149.3382	0.30855	149.3382	0.015	0.015	2.8	\N	0.05	9.35	196.45999999999998	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-09 16:27:08.324736+00	2025-12-09 16:27:08.324736+00	31.782945736434097
759	66	tb 60x060x2x6000mm	1809	0	5.58	0.12	0	4.456188	4.456188	1809	7.5	0.12	5.9895	0	34.40860215053764	8061.244092	10835.0055	0.003311	10835.0055	0.015	0.015	203.51	\N	0.05	678.38	14254.92	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-09 16:28:58.763521+00	2025-12-09 16:28:58.763521+00	34.408602150537625
760	66	tb 30x30x3x6000mm	771	0	6.14	0.18	0	4.569081	4.569081	771	8.2	0.12	6.54852	0	43.32247557003257	3522.761451	5048.90892	0.008494	5048.90892	0.025	0.025	158.06	\N	0.05	316.11	6638.3099999999995	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-09 16:28:58.763521+00	2025-12-09 16:28:58.763521+00	43.32247557003257
761	66	tb 40x40x2x6000mm	90	0	6.34	0.18	0	4.717911	4.717911	90	8	0.12	6.3888	0	35.41586519966146	424.61199	574.992	0.070987	574.992	0.015	0.015	10.8	\N	0.05	36	756	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-09 16:28:58.763521+00	2025-12-09 16:28:58.763521+00	35.41586519966145
762	66	tb 70x70x2x6000mm	160	2	5.47	0.12	0	4.368342	4.368342	160	7.15	0.12	5.70999	0	30.712979890310788	698.93472	913.5984000000001	0.035687	913.5984000000001	0.015	0.015	17.16	\N	0.05	57.2	1201.6	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-09 16:28:58.763521+00	2025-12-09 16:28:58.763521+00	30.71297989031081
770	82	CHP1200X300X2	58	0	6.2	0.18	0	4.61373	4.61373	58	8	0.18	5.9532	0	29.03225806451613	267.59634	345.2856	0.102641	345.2856	0.01	0.01	4.64	\N	0.0325	15.08	479.08	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-09 16:29:31.687572+00	2025-12-09 16:29:31.687572+00	29.032258064516125
771	82	CHP1200X3000X3	87	0	6	0.18	0	4.4649	4.4649	87	7.8	0.18	5.80437	0	30	388.4463	504.98018999999994	0.066717	504.98018999999994	0.05	0.05	33.93	\N	0.0325	22.05	700.35	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-09 16:29:31.687572+00	2025-12-09 16:29:31.687572+00	29.999999999999982
772	82	CHP1200X2000XX4,25	91	0	5.8	0.18	0	4.31607	4.31607	91	7.6	0.18	5.65554	0	31.03448275862069	392.76237	514.65414	0.062149	514.65414	0.015	0.015	10.37	\N	0.0325	22.48	714.35	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-09 16:29:31.687572+00	2025-12-09 16:29:31.687572+00	31.034482758620683
773	82	CHP1200X300X6,35	183	0	5.8	0.18	0	4.31607	4.31607	183	7.6	0.18	5.65554	0	31.03448275862069	789.84081	1034.96382	0.030905	1034.96382	0.015	0.015	20.86	\N	0.0325	45.2	1436.55	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-09 16:29:31.687572+00	2025-12-09 16:29:31.687572+00	31.034482758620683
774	82	CHP1200X3000X4,75	137	0	5.8	0.18	0	4.31607	4.31607	137	7.6	0.18	5.65554	0	31.03448275862069	591.30159	774.80898	0.041281	774.80898	0.015	0.015	15.62	\N	0.0325	33.84	1075.45	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-09 16:29:31.687572+00	2025-12-09 16:29:31.687572+00	31.034482758620683
775	82	CHP1200X2000X5/16	154	0	5.8	0.18	0	4.31607	4.31607	154	7.6	0.18	5.65554	0	31.03448275862069	664.67478	870.95316	0.036724	870.95316	0.015	0.015	17.56	\N	0.0325	38.04	1208.8999999999999	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-09 16:29:31.687572+00	2025-12-09 16:29:31.687572+00	31.034482758620683
776	82	CHP1200X2000X9,53	184	0	5.8	0.18	0	4.31607	4.31607	184	7.6	0.18	5.65554	0	31.03448275862069	794.15688	1040.6193600000001	0.030737	1040.6193600000001	0.015	0.015	20.98	\N	0.0325	45.45	1444.3999999999999	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-09 16:29:31.687572+00	2025-12-09 16:29:31.687572+00	31.034482758620708
780	79	TB RED 25,40X2,65X6000MM C C	46	0	6.34	0.18	0	4.717911	4.717911	46	8.6	0.18	6.39969	0	35.646687697160885	217.023906	294.38574	0.139124	294.38574	0.015	0.015	5.93	\N	0.0325	12.86	408.48	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-09 16:30:50.301378+00	2025-12-09 16:30:50.301378+00	35.646687697160885
834	88	100 X 100 X 3,00 X 6000 - 6 BR	300	1	6.21	0.18	0	4.621172	4.621172	300	8.2	0.18	6.10203	0	32.045074279858014	1386.3516	1830.609	0.02034	1830.609	0.015	0.015	36.9	\N	0.05	123	2583	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-09 18:11:44.720624+00	2025-12-09 18:11:44.720624+00	32.045074279858014
835	88	25,40 X 2,00 X 6000 - 27 BR	186	1	5.57	0.12	0	4.448202	4.448202	186	8.17	0.18	6.079706	0	36.677830728011	827.365572	1130.825316	0.032687	1130.825316	0.015	0.015	22.79	\N	0.0325	49.39	1569.84	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-09 18:11:44.720624+00	2025-12-09 18:11:44.720624+00	36.67783072801099
836	88	50,80 X 3,00 X 6000 - 8 BR	160	1	5.47	0.12	0	4.368342	4.368342	160	8.07	0.18	6.005291	0	37.47300463196334	698.93472	960.84656	0.037533	960.84656	0.015	0.015	19.37	\N	0.0325	41.96	1332.8	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-09 18:11:44.720624+00	2025-12-09 18:11:44.720624+00	37.47300463196335
838	89	30X20X1,50X6000 - 30 BR	211	1	6.17	0.12	0	4.927362	4.927362	211	8.9	0.18	6.622935	0	34.41137468690143	1039.673382	1397.439285	0.031388	1397.439285	0.015	0.015	28.17	\N	0.05	93.9	1972.85	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-09 18:24:27.656857+00	2025-12-09 18:24:27.656857+00	34.41137468690143
957	93	TUBO QUADRADO 20X20X1,50X6000 - 10 BRS	60	0	6.19	0.12	0	4.943334	4.943334	60	8.72	0.18	6.488988	0	31.267440152739024	296.60004	389.33928	0.10815	389.33928	0.015	0.015	7.85	\N	0.05	26.16	549.6	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-11 13:47:58.933731+00	2025-12-11 13:47:58.933731+00	31.267440152739013
1254	125	30- TB RED 114,30X3,75X600MM	1895	3	5.97	0.12	0	4.767642	4.767642	1895	7.85	0.12	6.26901	0	31.490787269681743	9034.68159	11879.773949999999	0.003308	11879.773949999999	0.015	0.015	223.14	\N	0.0325	483.46	15368.449999999999	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-15 00:22:56.671321+00	2025-12-15 00:22:56.671321+00	31.490787269681732
1255	125	56-TB RED 88,90X3,35X6000MM	2445	3	6.1	0.12	0	4.87146	4.87146	2445	7.85	0.12	6.26901	0	28.688524590163933	11910.7197	15327.729449999999	0.002564	15327.729449999999	0.01	0.01	191.93	\N	0.0325	623.78	19828.949999999997	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-15 00:22:56.671321+00	2025-12-15 00:22:56.671321+00	28.688524590163933
1256	125	460- TB RED 4240X3,75X6000MM	10150	3	5.97	0.12	0	4.767642	4.767642	10150	7.85	0.12	6.26901	0	31.490787269681743	48391.5663	63630.451499999996	0.000618	63630.451499999996	0.015	0.015	1195.16	\N	0.0325	2589.52	82316.5	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-15 00:22:56.671321+00	2025-12-15 00:22:56.671321+00	31.490787269681732
1280	130	Perfil W200x15,00 (45Brs)	4070	3	7.75	0.12	0	6.18915	6.011895	4190	9.3	0.07	7.848968	120	30.557303479185848	25189.8405	32887.17592	0.001873	32887.17592	0.015	0.015	584.51	\N	0	0	38967	{"has_difference": true, "absolute_difference": 120.0, "percentage_difference": 2.9484029484029484, "formatted_display": "2.9%"}	2025-12-15 15:55:35.675967+00	2025-12-15 15:55:35.675967+00	30.557301146865147
1281	130	Perfil U 150x50x4,75( 75Brs)	4050	3	5.38	0.12	0	4.296468	4.192939	4150	6.8	0.07	5.73903	100	36.87368215945903	17400.6954	23816.9745	0.001383	23816.9745	0.015	0.015	423.3	\N	0	0	28220	{"has_difference": true, "absolute_difference": 100.0, "percentage_difference": 2.4691358024691357, "formatted_display": "2.5%"}	2025-12-15 15:55:35.675967+00	2025-12-15 15:55:35.675967+00	36.873693565143384
1309	135	CH #1,20X1500X3000 0 8 PÇ	340	4	7.7	0.18	0	5.729955	5.729955	340	9.57	0.12	7.642602	0	33.379790940766554	1948.1847	2598.48468	0.022478	2598.48468	0.015	0.015	48.81	\N	0.0325	105.75	3359.2000000000003	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-15 19:50:32.336304+00	2025-12-15 19:50:32.336304+00	33.379790940766554
1009	29	100 X 100 X 2,25 X 6000 - 16 BR	670	1	6.42	0.18	0	4.777443	4.777443	670	8.4	0.18	6.25086	0	30.8411214953271	3200.88681	4188.0762	0.00933	4188.0762	0.015	0.015	84.42	\N	0.05	281.4	5909.400000000001	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-11 16:39:10.227286+00	2025-12-11 16:39:10.227286+00	30.841121495327116
1010	29	150 X 150 X 3,00 X 6000 - 15 BR	1270	1	6.1	0.12	0	4.87146	4.87146	1270	8.7	0.18	6.474105	0	32.89865871833085	6186.7542	8222.11335	0.005098	8222.11335	0.015	0.015	165.73	\N	0.05	552.45	11607.800000000001	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-11 16:39:10.227286+00	2025-12-11 16:39:10.227286+00	32.89865871833084
1011	29	50 X 50 X 2,00 X 6000 - 12 BR	250	1	5.88	0.12	0	4.695768	4.695768	250	8.35	0.18	6.213653	0	32.32453136526336	1173.942	1553.41325	0.024855	1553.41325	0.015	0.015	31.31	\N	0.05	104.38	2192.5	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-11 16:39:10.227286+00	2025-12-11 16:39:10.227286+00	32.32453136526337
1027	110	PERFIL U 100X50X2,65 - 50 BRS 	1300	3	6.59	0.18	0	4.903949	4.829647	1320	7.6	0.07	6.41421	20	32.80908521885761	6375.1337	8466.7572	0.004859	8466.7572	0.015	0.015	150.48	\N	0	0	10032	{"has_difference": true, "absolute_difference": 20.0, "percentage_difference": 1.5384615384615385, "formatted_display": "1.5%"}	2025-12-11 16:54:14.282588+00	2025-12-11 16:54:14.282588+00	32.80909230186027
1028	107	TUBO RETANGULAR 40X30X1,50X6000 - 12 BRS	123	0	6.17	0.12	0	4.927362	4.927362	123	7.99	0.12	6.380814	0	29.497568881685577	606.065526	784.840122	0.051877	784.840122	0.01	0.01	9.83	\N	0.05	49.14	1031.97	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-11 17:27:48.739588+00	2025-12-11 17:27:48.739588+00	29.497568881685577
1029	107	TUBO REDONDO 31,75X1,50X6000 - 50  BRS	360	0	6.27	0.12	0	5.007222	5.007222	360	8.13	0.12	6.492618	0	29.665071770334926	1802.59992	2337.3424800000003	0.018035	2337.3424800000003	0.01	0.01	29.27	\N	0.0325	95.12	3020.4	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-11 17:27:48.739588+00	2025-12-11 17:27:48.739588+00	29.665071770334926
871	92	150 x 100 x 3,00 x 6000 - 3br	212	1	5.99	0.12	0	4.783614	4.783614	212	8.67	0.18	6.451781	0	34.87252524973796	1014.126168	1367.7775720000002	0.030433	1367.7775720000002	0.015	0.015	27.57	\N	0.05	91.9	1929.1999999999998	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-09 19:40:08.155558+00	2025-12-09 19:40:08.155558+00	34.87252524973798
872	92	50 x 50 x 2,00 x 6000 - 9 br	170	1	5.88	0.12	0	4.695768	4.695768	170	8.47	0.18	6.302951	0	34.22620112407598	798.28056	1071.50167	0.037076	1071.50167	0.015	0.015	21.6	\N	0.05	72	1511.3000000000002	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-09 19:40:08.155558+00	2025-12-09 19:40:08.155558+00	34.22620112407597
1349	45	01 chapa 1200x3000x4,25 mm	123	0	6.4	0.18	0	4.966088	4.966088	123	8.5	0.18	6.325275	0	27.36937001519103	610.828824	778.008825	0.051425	778.008825	0.01	0.01	10.46	\N	0.0325	33.98	1079.9399999999998	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-16 16:31:10.577727+00	2025-12-16 16:31:10.577727+00	27.36937001519102
1350	136	TUBO QUADRADO 20X20X0,90X6000	200	5	7	0.18	0	5.20905	5.20905	200	9.8	0.18	7.29267	0	40	1041.81	1458.534	0.036463	1458.534	0.05	0.05	98	\N	0.05	98	2058	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-16 16:37:50.964417+00	2025-12-16 16:37:50.964417+00	40.000000000000014
1351	136	TUBO REDONDO 22,22X1,20X6000	200	0	6.27	0.12	0	5.007222	5.007222	200	9.49	0.18	7.061984	0	41.03596764832875	1001.4444	1412.3968	0.03531	1412.3968	0.025	0.025	47.45	\N	0.0325	61.69	1960.0000000000002	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-16 16:37:50.964417+00	2025-12-16 16:37:50.964417+00	41.03596764832875
882	90	VIGA I3.3/8X5,90X6000MM	2790	0	6.88	0.12	0	5.494368	5.494368	2790	9.3	0.12	7.42698	0	35.174418604651166	15329.28672	20721.2742	0.002662	20721.2742	0.015	0.015	389.21	\N	0	0	25947.000000000004	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-09 20:00:34.359449+00	2025-12-09 20:00:34.359449+00	35.17441860465116
883	90	VIGA I2.5/8X4,90X6000MM	1376	3	8.85	0.12	0	7.06761	7.06761	1376	10	0.12	7.986	0	12.994350282485875	9725.03136	10988.735999999999	0.005804	10988.735999999999	0	0	0	\N	0	0	13760	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-09 20:00:34.359449+00	2025-12-09 20:00:34.359449+00	12.994350282485856
884	90	VIGA I 4.5/8X8X600MM	6840	3	8.9	0.12	0	7.10754	7.10754	6840	12	0.12	9.5832	0	34.831460674157306	48615.5736	65549.088	0.001401	65549.088	0.015	0.015	1231.2	\N	0	0	82080	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-09 20:00:34.359449+00	2025-12-09 20:00:34.359449+00	34.8314606741573
963	106	76,20 X 3,00 X 6000 - 85 BR	2844	3	5.9	0.12	0	4.71174	4.71174	2844	7.7	0.12	6.14922	0	30.508474576271187	13400.18856	17488.38168	0.002162	17488.38168	0.015	0.015	328.48	\N	0.0325	711.71	22609.8	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-11 13:53:44.696658+00	2025-12-11 13:53:44.696658+00	30.508474576271173
964	108	TUBO A-106 - 1/2'' X SCH 80 X 5800MM - 37 BR	280	2	14.36	0.04	0	12.510432	12.510432	280	25.75	0.18	19.161863	0	53.16707688431542	3502.92096	5365.32164	0.068435	5365.32164	0.03	0.03	216.3	\N	0	0	7210	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-11 14:09:25.815612+00	2025-12-11 14:09:25.815612+00	53.167076884315435
1498	145	20 X 20 X 1,20 X 6000 - 122BR	537	1	5.98	0.12	0	4.775628	4.775628	537	8.47	0.18	6.302951	0	31.98161582099778	2564.512236	3384.684687	0.011737	3384.684687	0.015	0.015	68.23	\N	0.05	227.42	4773.93	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-18 13:11:30.642466+00	2025-12-18 13:11:30.642466+00	31.98161582099779
970	109	Tubo Galv. 2" 50,80x1,25 (100brs)	930	5	7	0.12	0	5.5902	5.472512	950	8.7	0.7	2.368575	20	-56.718687871310294	5198.886	2250.14625	0.002493	2250.14625	0.05	0.05	413.25	\N	0.0325	268.61	8531	{"has_difference": true, "absolute_difference": 20.0, "percentage_difference": 2.150537634408602, "formatted_display": "2.2%"}	2025-12-11 14:38:52.111376+00	2025-12-11 14:38:52.111376+00	-56.7186845412652
971	109	Tubo Galv. 2" 50,80x1,95 (100brs)	1420	5	0.07	0.12	0	0.055902	0.054745	1450	8.7	0.7	2.368575	30	4226.559503150973	79.38084	3434.4337499999997	0.001634	3434.4337499999997	0.05	0.05	630.75	\N	0.0325	409.99	13021	{"has_difference": true, "absolute_difference": 30.0, "percentage_difference": 2.112676056338028, "formatted_display": "2.1%"}	2025-12-11 14:38:52.111376+00	2025-12-11 14:38:52.111376+00	4226.527345893543
903	95	TUBO QUADRADO 50X50X2,00X6000 - 12 BRS	235	0	5.58	0.12	0	4.456188	4.456188	235	8.29	0.18	6.169004	0	38.43679844746227	1047.20418	1449.71594	0.026251	1449.71594	0.015	0.015	29.22	\N	0.05	97.41	2044.4999999999998	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-10 14:04:25.392453+00	2025-12-10 14:04:25.392453+00	38.43679844746228
904	95	CANTONEIRA 1"X18/X6000 - 12 BRS	99	0	6.5	0.12	0	5.1909	5.1909	99	8.9	0.12	7.10754	0	36.92307692307693	513.8991	703.64646	0.071793	703.64646	0.015	0.015	13.22	\N	0	0	881.1	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-10 14:04:25.392453+00	2025-12-10 14:04:25.392453+00	36.92307692307695
1294	131	TB NBR 6591 GALV - 114,30 x 2,00 x 6000 - 300PÇ 	10966	15	6.03	0.12	2.09	7.515296	7.515296	10966	11.7	0.07	9.874508	0	31.392136783434744	82412.735936	108283.854728	0.0009	108283.854728	0.015	0.015	1924.53	\N	0.0325	4169.82	132469.28	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-15 17:15:18.934944+00	2025-12-15 17:15:18.934944+00	31.392136783434754
1007	94	TUBO MEC 177 X 20 X 6000 - 1 BR	478	5	23.7	0.18	0	17.636355	17.636355	478	29.47	0.12	23.534742	0	33.444478748584956	8430.17769	11249.606676000001	0.049236	11249.606676000001	0.015	0.015	211.3	\N	0.0325	457.82	14545.539999999999	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-11 16:36:11.782341+00	2025-12-11 16:36:11.782341+00	33.44447874858496
1012	69	TB INDUSTRIAL C/C - 88,90 X 6,35 X 6000	80	1	6.55	0.12	0	5.23083	5.23083	80	9.7	0.12	7.74642	0	48.091603053435115	418.4664	619.7135999999999	0.09683	619.7135999999999	0.025	0.025	19.4	\N	0.0325	25.22	801.5999999999999	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-11 16:39:30.44006+00	2025-12-11 16:39:30.44006+00	48.091603053435094
905	95	TUBO RETANGULAR 50X30X1,50X6000 - 4 BRS	45	0	6.59	0.12	0	5.262774	5.262774	45	9.77	0.18	7.270346	0	38.146650416681396	236.82483	327.16557	0.161563	327.16557	0.015	0.015	6.59	\N	0.05	21.98	461.7	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-10 14:04:25.392453+00	2025-12-10 14:04:25.392453+00	38.146650416681396
906	95	TUBO RETANGULAR 30X20X2,00X6000 - 10 BRS	93	0	5.58	0.12	0	4.456188	4.456188	93	8.27	0.18	6.154121	0	38.1028134360579	414.425484	572.333253	0.066173	572.333253	0.015	0.015	11.54	\N	0.05	38.46	807.24	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-10 14:04:25.392453+00	2025-12-10 14:04:25.392453+00	38.1028134360579
907	95	TUBO QUADRADO 30X30X1,50X6000 - 16 BRS	148	0	6.19	0.12	0	4.943334	4.943334	148	9.19	0.18	6.838739	0	38.34264486275862	731.613432	1012.133372	0.046208	1012.133372	0.015	0.015	20.4	\N	0.05	68.01	1428.2	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-10 14:04:25.392453+00	2025-12-10 14:04:25.392453+00	38.342644862758625
908	96	CHATO 1 X 1/8	2	2	29	0.12	0	23.1594	23.1594	2	37.5	0.12	29.9475	0	29.310344827586203	46.3188	59.895	14.97375	59.895	0.01	0.01	0.75	\N	0	0	75	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-10 14:09:12.468209+00	2025-12-10 14:09:12.468209+00	29.31034482758621
909	96	Cantoneira 5/8x1/8	10	2	29.5	0.12	0	23.5587	23.5587	10	38.3	0.12	30.58638	0	29.830508474576273	235.587	305.86379999999997	3.058638	305.86379999999997	0.01	0.01	3.83	\N	0	0	383	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-10 14:09:12.468209+00	2025-12-10 14:09:12.468209+00	29.830508474576266
910	96	3/4x2,00	2	2	37.4	0.18	0	27.83121	27.83121	2	49	0.18	36.46335	0	31.016042780748666	55.66242	72.9267	18.231675	72.9267	0.015	0.015	1.47	\N	0.0325	3.19	101.18	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-10 14:09:12.468209+00	2025-12-10 14:09:12.468209+00	31.016042780748656
911	96	20X20X1,50	3	2	44.32	0.12	0	35.393952	35.393952	3	62.4	0.18	46.43496	0	31.19461765671152	106.181856	139.30488	15.47832	139.30488	0.015	0.015	2.81	\N	0.05	9.36	196.56	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-10 14:09:12.468209+00	2025-12-10 14:09:12.468209+00	31.19461765671152
912	97	SCH 40 S/C 3"	270	3	11.9	0.18	0	8.855385	8.855385	270	15.47	0.18	11.512001	0	30.000005646281895	2390.95395	3108.24027	0.042637	3108.24027	0.015	0.015	62.65	\N	0	0	4176.900000000001	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-10 14:19:18.481843+00	2025-12-10 14:19:18.481843+00	30.000005646281892
913	98	ferro red 1045 130 x 680 - 06 pçs	426	5	8.6	0.12	0	6.86796	6.679797	438	10.75	0.07	9.072731	12	35.823453916339076	2925.75096	3973.8561779999995	0.020714	3973.8561779999995	0.015	0.015	70.63	\N	0	0	4708.5	{"has_difference": true, "absolute_difference": 12.0, "percentage_difference": 2.816901408450704, "formatted_display": "2.8%"}	2025-12-10 14:36:27.948303+00	2025-12-10 14:36:27.948303+00	35.82345976569379
914	98	ferro red 1045 190,50 x 145 - 12 pçs	390	5	9.75	0.12	0	7.78635	7.553922	402	11.9	0.07	10.043303	12	32.954814730678976	3036.6765	4037.407806	0.024983	4037.407806	0.015	0.015	71.76	\N	0	0	4783.8	{"has_difference": true, "absolute_difference": 12.0, "percentage_difference": 3.076923076923077, "formatted_display": "3.1%"}	2025-12-10 14:36:27.948303+00	2025-12-10 14:36:27.948303+00	32.95482103543135
915	98	ferro red 1045 forjado 355,60 x 160 06 pçs	750	5	12.99	0.18	0	9.666509	9.37889	773	14.9	0.07	12.575228	23	34.08013101763642	7249.88175	9720.651243999999	0.016268	9720.651243999999	0.015	0.015	172.77	\N	0	0	11517.7	{"has_difference": true, "absolute_difference": 23.0, "percentage_difference": 3.066666666666667, "formatted_display": "3.1%"}	2025-12-10 14:36:27.948303+00	2025-12-10 14:36:27.948303+00	34.08013508634122
1522	147	cantoneira 2 x 1/4 - 10 brs	285	3	6.5	0.12	0	5.1909	5.031995	294	8.25	0.12	6.58845	9	30.931171433993875	1479.4065	1937.0043	0.02241	1937.0043	0.015	0.015	36.38	\N	0	0	2425.5	{"has_difference": true, "absolute_difference": 9.0, "percentage_difference": 3.1578947368421053, "formatted_display": "3.2%"}	2025-12-18 13:34:14.703783+00	2025-12-18 13:34:14.703783+00	30.931174089068826
1357	138	70 X 30 X 2,00 X 6000 - 11 BR	210	1	5.47	0.12	0	4.368342	4.368342	210	7.77	0.18	5.782046	0	32.362484439176235	917.35182	1214.22966	0.027534	1214.22966	0.015	0.015	24.48	\N	0.05	81.59	1713.6000000000001	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-16 17:03:24.90099+00	2025-12-16 17:03:24.90099+00	32.36248443917624
1252	126	06-TB RED SCH160 5"X6000MM	2376	0	13	0.18	0	9.67395	9.67395	2376	21	0.07	17.723475	0	83.20825515947467	22985.3052	42110.9766	0.007459	42110.9766	0.05	0.05	2494.8	\N	0	0	49896	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-15 00:17:56.263863+00	2025-12-15 00:17:56.263863+00	83.2082551594747
1253	126	06-TB RED SCH160 6"X6000MM	2714	0	13	0.18	0	9.67395	9.67395	2714	16.8	0.07	14.17878	0	46.56660412757974	26255.1003	38481.20892	0.005224	38481.20892	0.025	0.025	1139.88	\N	0	0	45595.200000000004	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-15 00:17:56.263863+00	2025-12-15 00:17:56.263863+00	46.56660412757974
1129	114	Tubo  A/C 50x50x4,75  NBR 6591	760	3	6.35	0.12	0	5.07111	5.07111	760	9.5	0.18	7.069425	0	39.40586972083035	3854.0436	5372.763	0.009302	5372.763	0.015	0.015	108.3	\N	0.05	361	7584.8	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-12 13:25:57.451371+00	2025-12-12 13:25:57.451371+00	39.40586972083035
1130	114	Tubo A/C 100x100x6,35(4brs )NBR6591 	450	3	5.9	0.12	0	4.71174	4.609311	460	9.5	0.18	7.069425	10	53.37270581221358	2120.283	3251.9355	0.015368	3251.9355	0.03	0.03	131.1	\N	0.05	218.5	4590.8	{"has_difference": true, "absolute_difference": 10.0, "percentage_difference": 2.2222222222222223, "formatted_display": "2.2%"}	2025-12-12 13:25:57.451371+00	2025-12-12 13:25:57.451371+00	53.37271015237117
1131	115	60X60X5,00 20 BRS	1020	3	6.29	0.12	0	5.023194	4.875031	1051	8.17	0.12	6.524562	31	33.83631816905369	5123.65788	6857.314662000001	0.006208	6857.314662000001	0.015	0.015	128.8	\N	0.05	429.33	9017.58	{"has_difference": true, "absolute_difference": 31.0, "percentage_difference": 3.0392156862745097, "formatted_display": "3.0%"}	2025-12-12 14:20:22.255628+00	2025-12-12 14:20:22.255628+00	33.836310358801725
1132	115	40X40X5,00 05 BRS	170	3	6.29	0.12	0	5.023194	4.879674	175	8.17	0.12	6.524562	5	33.70897318140515	853.94298	1141.79835	0.037283	1141.79835	0.015	0.015	21.45	\N	0.05	71.49	1501.5	{"has_difference": true, "absolute_difference": 5.0, "percentage_difference": 2.9411764705882355, "formatted_display": "2.9%"}	2025-12-12 14:20:22.255628+00	2025-12-12 14:20:22.255628+00	33.70896848405498
1133	115	CANRONEIRA 2X3/16 05 BRS	110	3	6.5	0.12	0	5.1909	5.053088	113	8.17	0.12	6.524562	3	29.120292383588016	570.999	737.2755060000001	0.057739	737.2755060000001	0.01	0.01	9.23	\N	0	0	923.21	{"has_difference": true, "absolute_difference": 3.0, "percentage_difference": 2.727272727272727, "formatted_display": "2.7%"}	2025-12-12 14:20:22.255628+00	2025-12-12 14:20:22.255628+00	29.12027972027973
1267	124	5580 1/2X2,65 BSP GALV	3	0	78	0.18	0	58.0437	58.0437	3	80.5	0.18	59.904075	0	3.205128205128205	174.1311	179.712225	19.968025	179.712225	0	0	0	\N	0.0325	7.85	249.36	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-15 13:14:06.568023+00	2025-12-15 13:14:06.568023+00	3.2051282051281937
1268	124	5580 1/2X2,65 NPT GALV	3	0	96.76	0.18	0	72.003954	16.616297	13	125.78	0.18	93.599187	10	463.2975084641301	216.011862	1216.789431	7.199937	1216.789431	0.05	0.05	81.76	\N	0.0325	53.14	1688.31	{"has_difference": true, "absolute_difference": 10.0, "percentage_difference": 333.3333333333333, "formatted_display": "333.3%"}	2025-12-15 13:14:06.568023+00	2025-12-15 13:14:06.568023+00	463.2975058564145
1269	124	5580 1X3,35 NPT GALV	3	0	208	0.18	0	154.7832	92.86992	5	270.4	0.18	201.21816	2	116.66666666666667	464.3496	1006.0908000000001	40.243632	1006.0908000000001	0.05	0.05	67.6	\N	0.0325	43.94	1395.95	{"has_difference": true, "absolute_difference": 2.0, "percentage_difference": 66.66666666666667, "formatted_display": "66.7%"}	2025-12-15 13:14:06.568023+00	2025-12-15 13:14:06.568023+00	116.6666666666667
1270	124	5580 2X3,75 NPT GALV	3	0	416	0.18	0	309.5664	185.73984	5	541	0.18	402.58515	2	116.74679487179486	928.6992	2012.9257499999999	80.51703	2012.9257499999999	0.05	0.05	135.25	\N	0.0325	87.91	2792.9	{"has_difference": true, "absolute_difference": 2.0, "percentage_difference": 66.66666666666667, "formatted_display": "66.7%"}	2025-12-15 13:14:06.568023+00	2025-12-15 13:14:06.568023+00	116.74679487179485
1157	113	PERFIL US 150X60X3,75X6000	1293.6	5	6.93	0.12	0	5.534298	5.534298	1293.6	9.96	0.12	7.954056	0	43.722943722943725	7159.167893	10289.366841599998	0.006149	10289.366841599998	0.025	0.025	322.11	\N	0	0	12884.256	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-12 17:14:05.882108+00	2025-12-12 17:14:05.882108+00	43.72294371892862
1158	113	PERFIL US 150X60X2,00X6000	1166.7	5	7.25	0.12	0	5.78985	5.78985	1166.7	9.93	0.12	7.930098	0	36.96551724137931	6755.017995	9252.0453366	0.006797	9252.0453366	0.015	0.015	173.78	\N	0	0	11585.331	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-12 17:14:05.882108+00	2025-12-12 17:14:05.882108+00	36.96551724137931
1159	113	PERFIL UE 150X60X20X2,25X6000	4187.57	5	6.01	0.12	0	4.799586	4.799586	4187.57	8.42	0.12	6.724212	0	40.099833610648915	20098.602346	28158.108444839996	0.001606	28158.108444839996	0.025	0.025	881.48	\N	0	0	35259.3394	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-12 17:14:05.882108+00	2025-12-12 17:14:05.882108+00	40.0998336107883
1259	127	150X50X2,00X6000 - 13 BR	480	1	5.88	0.12	0	4.695768	4.695768	480	7.87	0.12	6.284982	0	33.843537414965986	2253.96864	3016.79136	0.013094	3016.79136	0.015	0.015	56.66	\N	0.05	188.88	3964.7999999999997	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-15 12:11:46.006057+00	2025-12-15 12:11:46.006057+00	33.84353741496599
1266	128	ferro redondo 3/4	26	1	7.31	0.12	0	5.837766	5.837766	26	9.57	0.12	7.642602	0	30.91655266757866	151.781916	198.707652	0.293946	198.707652	0.015	0.015	3.73	\N	0	0	248.82	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-15 13:09:48.788203+00	2025-12-15 13:09:48.788203+00	30.916552667578667
1295	131	TB NBR 6591 GALV - 101,60 x 2,00 x 6000 - 300PÇ 	9726	15	6.02	0.12	2.09	7.50731	7.50731	9726	11.7	0.07	9.874508	0	31.531906901406764	73016.09706	96039.464808	0.001015	96039.464808	0.015	0.015	1706.91	\N	0.0325	3698.31	117490.08	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-15 17:15:18.934944+00	2025-12-15 17:15:18.934944+00	31.53190690140677
1296	131	TB NBR 6591 GALV - 88,90 x 2,00 x 6000 - 300PÇ 	8486	15	6.78	0.18	2.09	7.745075	7.745075	8486	11.95	0.07	10.085501	0	30.218248370738827	65724.70645	85585.561486	0.001188	85585.561486	0.015	0.015	1521.12	\N	0.0325	3295.75	104717.24	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-15 17:15:18.934944+00	2025-12-15 17:15:18.934944+00	30.21824837073883
1297	131	TB NBR 6591 GALV - 76,20 x 2,00 x 6000 - 150PÇ 	3623	15	6.03	0.12	2.09	7.515296	7.515296	3623	11.7	0.07	9.874508	0	31.392136783434744	27227.917408	35775.342484	0.002726	35775.342484	0.015	0.015	635.84	\N	0.0325	1377.65	43765.840000000004	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-15 17:15:18.934944+00	2025-12-15 17:15:18.934944+00	31.392136783434733
1302	134	273 X 6,35 24 BRS	6024	0	7.25	0.12	0	5.78985	5.704622	6114	8.95	0.07	7.553576	90	32.411507721282845	34878.0564	46182.563664	0.001235	46182.563664	0.015	0.015	820.8	\N	0.0325	1778.41	56493.36	{"has_difference": true, "absolute_difference": 90.0, "percentage_difference": 1.4940239043824701, "formatted_display": "1.5%"}	2025-12-15 18:59:46.408071+00	2025-12-15 18:59:46.408071+00	32.41151724268671
1303	134	114,30 X 4,50 90 BRS	6930	0	6.1	0.12	0	4.87146	4.823434	6999	7.6	0.07	6.41421	69	32.98015480257426	33759.2178	44893.05579	0.000916	44893.05579	0.015	0.015	797.89	\N	0.0325	1728.75	54942.149999999994	{"has_difference": true, "absolute_difference": 69.0, "percentage_difference": 0.9956709956709957, "formatted_display": "1.0%"}	2025-12-15 18:59:46.408071+00	2025-12-15 18:59:46.408071+00	32.98014206359958
1310	132	30X30X2,65X6000 - 6 BR	85	1	6.13	0.18	0	4.56164	4.56164	85	8.4	0.18	6.25086	0	37.03098008610938	387.7394	531.3231000000001	0.07354	531.3231000000001	0.015	0.015	10.71	\N	0.05	35.7	749.7	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-15 20:02:11.760729+00	2025-12-15 20:02:11.760729+00	37.03098008610941
1160	113	CANTONEIRA 2.1/2"X3/16X6000	1018.91	3	7.1	0.12	0	5.67006	5.67006	1018.91	9.23	0.12	7.371078	0	30	5777.280835	7510.465084979999	0.007234	7510.465084979999	0.05	0.05	470.23	\N	0	0	9404.5393	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-12 17:14:05.882108+00	2025-12-12 17:14:05.882108+00	29.99999999099923
1161	113	CANTONEIRA 2"X3/16X6000	288.8	2	6.5	0.12	0	5.1909	5.1909	288.8	8.77	0.12	7.003722	0	34.92307692307692	1499.13192	2022.6749136	0.024251	2022.6749136	0.015	0.015	37.99	\N	0	0	2532.776	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-12 17:14:05.882108+00	2025-12-12 17:14:05.882108+00	34.92307692307692
1162	113	CANTONEIRA 2.1/2X1/4X6000	125.31	2	7.15	0.12	0	5.70999	5.70999	125.31	9.65	0.12	7.70649	0	34.96503496503497	715.518847	965.7002619	0.061499	965.7002619	0.015	0.015	18.14	\N	0	0	1209.2415	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-12 17:14:05.882108+00	2025-12-12 17:14:05.882108+00	34.9650349461724
1163	113	CANTONEIRA 3"X5/16X6000	81.74	2	6.9	0.12	0	5.51034	5.51034	81.74	9.32	0.12	7.442952	0	35.07246376811594	450.415192	608.38689648	0.091056	608.38689648	0.015	0.015	11.43	\N	0	0	761.8168	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-12 17:14:05.882108+00	2025-12-12 17:14:05.882108+00	35.07246364816221
1164	113	FERRO CHATO 1"X3/16X6000	11.28	2	6.5	0.12	0	5.1909	5.1909	11.28	8.77	0.12	7.003722	0	34.92307692307692	58.553352	79.00198415999999	0.620897	79.00198415999999	0.015	0.015	1.48	\N	0	0	98.92559999999999	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-12 17:14:05.882108+00	2025-12-12 17:14:05.882108+00	34.92307692307692
1165	113	FERRO CHATO 1"X1/8X6000	173.88	2	7.27	0.12	0	5.805822	5.805822	173.88	9.82	0.12	7.842252	0	35.075653370013754	1009.516329	1363.61077776	0.045102	1363.61077776	0.015	0.015	25.61	\N	0	0	1707.5016	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-12 17:14:05.882108+00	2025-12-12 17:14:05.882108+00	35.0756534181826
1166	113	FERRO CHATO 3"X3/8X6000	266.34	2	6.5	0.12	0	5.1909	5.1909	266.34	8.77	0.12	7.003722	0	34.92307692307692	1382.544306	1865.3713174799998	0.026296	1865.3713174799998	0.015	0.015	35.04	\N	0	0	2335.8017999999997	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-12 17:14:05.882108+00	2025-12-12 17:14:05.882108+00	34.9230769230769
1167	113	FERRO CHATO 2"X3/16X6000	22.68	2	6.5	0.12	0	5.1909	5.1909	22.68	8.77	0.12	7.003722	0	34.92307692307692	117.729612	158.84441496	0.308806	158.84441496	0.015	0.015	2.98	\N	0	0	198.90359999999998	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-12 17:14:05.882108+00	2025-12-12 17:14:05.882108+00	34.92307692307692
1168	113	FERRO CHATO 2"X1/4X6000	179.04	2	6.5	0.12	0	5.1909	5.1909	179.04	8.77	0.12	7.003722	0	34.92307692307692	929.378736	1253.9463868799999	0.039118	1253.9463868799999	0.015	0.015	23.55	\N	0	0	1570.1807999999999	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-12 17:14:05.882108+00	2025-12-12 17:14:05.882108+00	34.9230769230769
1169	113	VIGA W 200X15X6000	178.14	2	7.75	0.12	0	6.18915	6.18915	178.14	10.46	0.12	8.353356	0	34.96774193548387	1102.535181	1488.0668378399998	0.046892	1488.0668378399998	0.015	0.015	27.95	\N	0	0	1863.3444	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-12 17:14:05.882108+00	2025-12-12 17:14:05.882108+00	34.967741935483865
1170	113	VIGA U 6" 2° ALMA	53.63	2	7.5	0.12	0	5.9895	5.9895	53.63	10.12	0.12	8.081832	0	34.93333333333333	321.216885	433.42865016	0.150696	433.42865016	0.015	0.015	8.14	\N	0	0	542.7356	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-12 17:14:05.882108+00	2025-12-12 17:14:05.882108+00	34.93333333333335
1171	113	PERFIL US 300X75X4,75X6000	9022.18	5	6.49	0.12	0	5.182914	5.182914	9022.18	8.89	0.12	7.099554	0	36.97996918335901	46761.183033	64053.454107720005	0.000787	64053.454107720005	0.015	0.015	1203.11	\N	0	0	80207.1802	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-12 17:14:05.882108+00	2025-12-12 17:14:05.882108+00	36.979969181952924
1582	154	120 X 120 X 9,52 A36 1237 BRS	264400	0	6.9	0.12	0	5.51034	5.51034	264400	8.97	0.12	7.163442	0	30	1456933.896	1894014.0648	2.7e-05	1894014.0648	0.05	0.05	118583.4	\N	0.05	118583.4	2490648	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-18 18:04:34.496821+00	2025-12-18 18:04:34.496821+00	30.000000000000004
1583	154	150 X 150 X 6,35 A36 200 BRS	35700	0	6.9	0.12	0	5.51034	5.51034	35700	8.97	0.12	7.163442	0	30	196719.138	255734.8794	0.000201	255734.8794	0.05	0.05	16011.45	\N	0.05	16011.45	336294	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-18 18:04:34.496821+00	2025-12-18 18:04:34.496821+00	30.000000000000004
1584	154	100 x 50 x 3,35 A36 250 BRS	11710	0	6.9	0.12	0	5.51034	5.51034	11710	8.97	0.12	7.163442	0	30	64526.0814	83883.90582	0.000612	83883.90582	0.05	0.05	5251.94	\N	0.05	5251.94	110308.2	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-18 18:04:34.496821+00	2025-12-18 18:04:34.496821+00	30.000000000000004
1593	150	VIGA U 8" 2° ALMA X 6000 - 2 BRS	246	5	8.95	0.12	0	7.14747	7.14747	246	11.63	0.12	9.287718	0	29.944134078212294	1758.27762	2284.778628	0.037755	2284.778628	0.01	0.01	28.61	\N	0	0	2860.98	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-18 18:44:54.854285+00	2025-12-18 18:44:54.854285+00	29.94413407821228
1594	150	VIGA I 3" 1° ALMA X 6000 - 2 BRS	105	5	7.5	0.12	0	5.9895	5.9895	105	9.75	0.12	7.78635	0	30	628.8975	817.56675	0.074156	817.56675	0.015	0.015	15.36	\N	0	0	1023.75	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-18 18:44:54.854285+00	2025-12-18 18:44:54.854285+00	29.999999999999982
1603	120	PERFIL US 100X50X2,62X6000 - 9 BRS	225	0	5.19	0.12	0	4.144734	4.144734	225	7.69	0.18	5.722514	0	38.0670991190267	932.56515	1287.56565	0.025433	1287.56565	0.015	0.015	25.95	\N	0	0	1730.25	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-18 18:49:06.228919+00	2025-12-18 18:49:06.228919+00	38.06709911902671
1391	139	FERRO RED 1/2 22 BRS	131	0	6.5	0.12	0	5.1909	5.1909	131	8.45	0.18	6.288068	0	21.136373268604675	680.0079	823.736908	0.048001	823.736908	0.01	0.01	11.07	\N	0	0	1106.9499999999998	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-16 18:11:46.639752+00	2025-12-16 18:11:46.639752+00	21.136373268604668
1392	139	FERRO RED 1.1/2 13 BRS	702	0	6.5	0.12	0	5.1909	5.1909	702	8.45	0.12	6.74817	0	30	3644.0118	4737.21534	0.009613	4737.21534	0.015	0.015	88.98	\N	0	0	5931.9	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-16 18:11:46.639752+00	2025-12-16 18:11:46.639752+00	29.999999999999982
1393	139	TUBO RED 88,90X7,95	1344	0	7.6	0.18	0	5.65554	5.630404	1350	9.2	0.12	7.34712	6	30.490103374464784	7601.04576	9918.612000000001	0.005442	9918.612000000001	0.015	0.015	186.3	\N	0.0325	403.65	12825	{"has_difference": true, "absolute_difference": 6.0, "percentage_difference": 0.44642857142857145, "formatted_display": "0.4%"}	2025-12-16 18:11:46.639752+00	2025-12-16 18:11:46.639752+00	30.490097194205035
1394	139	SCH 40 S/C API 5L 6"X5800 12 BRS	2160	0	14.75	0.18	0	10.976213	10.976213	2160	17.9	0.12	14.29494	0	30.23562862710481	23708.62008	30877.0704	0.006618	30877.0704	0.015	0.015	579.96	\N	0	0	38664	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-16 18:11:46.639752+00	2025-12-16 18:11:46.639752+00	30.235628627104806
1395	139	120X120X9,50 555 BRS	114000	0	6.59	0.12	0	5.262774	5.262774	114000	8.6	0.12	6.86796	0	30.500758725341427	599956.236	782947.4400000001	6e-05	782947.4400000001	0.015	0.015	14706	\N	0.05	49020	1029419.9999999999	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-16 18:11:46.639752+00	2025-12-16 18:11:46.639752+00	30.500758725341438
1396	139	127X127X9,50 555 BRS	121000	0	6.59	0.12	0	5.262774	5.262774	121000	8.6	0.12	6.86796	0	30.500758725341427	636795.654	831023.16	5.7e-05	831023.16	0.015	0.015	15609	\N	0.05	52030	1092630	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-16 18:11:46.639752+00	2025-12-16 18:11:46.639752+00	30.500758725341438
1397	139	150x150x6,35 100 brs 	17100	0	6.59	0.12	0	5.262774	5.262774	17100	8.6	0.12	6.86796	0	30.500758725341427	89993.4354	117442.116	0.000402	117442.116	0.015	0.015	2205.9	\N	0.05	7353	154413	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-16 18:11:46.639752+00	2025-12-16 18:11:46.639752+00	30.500758725341413
1398	139	cantoneira 3"x3/8 03 brs	108	0	6.9	0.12	0	5.51034	5.361412	111	8.97	0.12	7.163442	3	33.6111084169618	595.11672	795.142062	0.064536	795.142062	0.015	0.015	14.94	\N	0	0	995.6700000000001	{"has_difference": true, "absolute_difference": 3.0, "percentage_difference": 2.7777777777777777, "formatted_display": "2.8%"}	2025-12-16 18:11:46.639752+00	2025-12-16 18:11:46.639752+00	33.61111111111113
1399	139	chapa 1/2 6000x1800 11 pçs	12078	0	5.7	0.18	0	4.241655	4.241655	12078	6.9	0.12	5.51034	0	29.910141206675224	51230.70909	66553.88652	0.000456	66553.88652	0.01	0.01	833.38	\N	0.0325	2708.49	85995.36	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-16 18:11:46.639752+00	2025-12-16 18:11:46.639752+00	29.910141206675235
1400	139	chapa 3/8  2440x1200 50 pçs	11150	0	5.7	0.18	0	4.241655	4.241655	11150	6.9	0.12	5.51034	0	29.910141206675224	47294.45325	61440.291000000005	0.000494	61440.291000000005	0.01	0.01	769.35	\N	0.0325	2500.39	79388	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-16 18:11:46.639752+00	2025-12-16 18:11:46.639752+00	29.910141206675235
1401	139	chapa 1/4 6000x1200x01 pç	370	0	5.7	0.18	0	4.241655	4.241655	370	6.9	0.12	5.51034	0	29.910141206675224	1569.41235	2038.8258	0.014893	2038.8258	0.01	0.01	25.53	\N	0.0325	82.97	2634.4	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-16 18:11:46.639752+00	2025-12-16 18:11:46.639752+00	29.910141206675235
1402	139	chapa 2" 6000x1200 01 pç	2300	0	8	0.18	0	5.9532	5.9532	2300	7.2	0.12	5.74992	0	-3.414634146341464	13692.36	13224.816	0.0025	13224.816	0.05	0.05	828	\N	0.0325	538.2	17089	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-16 18:11:46.639752+00	2025-12-16 18:11:46.639752+00	-3.4146341463414664
1403	139	chapa 3/4 6000x1200 01 pç	1100	0	6.2	0.18	0	4.61373	4.61373	1100	7.55	0.12	6.02943	0	30.68450039339103	5075.103	6632.373	0.005481	6632.373	0.015	0.015	124.57	\N	0.0325	269.91	8580	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-16 18:11:46.639752+00	2025-12-16 18:11:46.639752+00	30.684500393391012
1404	85	TB 100X100X3X600MM	286	2	6.14	0.12	0	4.903404	4.903404	286	7.9	0.12	6.30894	0	28.664495114006517	1402.373544	1804.35684	0.022059	1804.35684	0.01	0.01	22.59	\N	0.05	112.97	2373.8	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-16 18:51:54.252955+00	2025-12-16 18:51:54.252955+00	28.664495114006506
1405	85	TB 120X120X3X6000MM	1106	4	6.42	0.12	0	5.127012	5.127012	1106	8.2	0.12	6.54852	0	27.725856697819314	5670.475272	7242.66312	0.005921	7242.66312	0.01	0.01	90.69	\N	0.05	453.46	9522.66	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-16 18:51:54.252955+00	2025-12-16 18:51:54.252955+00	27.725856697819328
1406	85	TB 140X140X4,75X6000MM	3550	3	6.18	0.12	0	4.935348	4.935348	3550	8.1	0.12	6.46866	0	31.06796116504854	17520.4854	22963.743	0.001822	22963.743	0.015	0.015	431.33	\N	0.05	1437.75	30210.5	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-16 18:51:54.252955+00	2025-12-16 18:51:54.252955+00	31.06796116504853
1407	85	TB 200X100X3X6000MM	656	0	6.1	0.12	0	4.87146	4.87146	656	8	0.12	6.3888	0	31.147540983606557	3195.67776	4191.0527999999995	0.009739	4191.0527999999995	0.015	0.015	78.72	\N	0.05	262.4	5510.400000000001	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-16 18:51:54.252955+00	2025-12-16 18:51:54.252955+00	31.147540983606547
1408	85	TB 200X100X4,75X6000MM	267	0	7.4	0.18	0	5.50671	5.50671	267	9.5	0.12	7.5867	0	37.77191825972314	1470.29157	2025.6489000000001	0.028415	2025.6489000000001	0.015	0.015	38.05	\N	0.05	126.83	2664.6600000000003	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-16 18:51:54.252955+00	2025-12-16 18:51:54.252955+00	37.77191825972315
1409	85	TB 250X1506,35X6000MM	454	0	6.57	0.12	0	5.246802	5.246802	454	8.9	0.12	7.10754	0	35.46423135464231	2382.048108	3226.82316	0.015655	3226.82316	0.015	0.015	60.61	\N	0.05	202.03	4244.9	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-16 18:51:54.252955+00	2025-12-16 18:51:54.252955+00	35.464231354642315
1412	137	80 x 80 x 3,00 X 6000 	8	1	244.4	0.18	0	181.87026	181.87026	8	317.72	0.18	236.431338	0	30	1454.96208	1891.450704	29.553917	1891.450704	0.015	0.015	38.13	\N	0.05	127.09	2668.88	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-17 11:52:44.968645+00	2025-12-17 11:52:44.968645+00	30.000000000000004
1595	146	TUBO REDONDO 38,10X4,25X6000	2	0	132.07	0.12	0	105.471102	105.471102	2	192	0.18	142.8768	0	35.465352395768086	210.942204	285.7536	71.4384	285.7536	0.015	0.015	5.76	\N	0.0325	12.48	396.48	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-18 18:45:16.477797+00	2025-12-18 18:45:16.477797+00	35.46535239576809
1596	146	TUBO QUADRADO 40X40X2,65X6000	7	0	102.03	0.12	0	81.481158	81.481158	7	145	0.18	107.90175	0	32.42540072884089	570.368106	755.3122500000001	15.414536	755.3122500000001	0.015	0.015	15.23	\N	0.05	50.75	1065.75	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-18 18:45:16.477797+00	2025-12-18 18:45:16.477797+00	32.425400728840906
1597	146	TUBO QUADRADO 60X60X3,00X6000	3	0	129.36	0.12	0	103.306896	103.306896	3	205	0.18	152.55075	0	47.667538089616016	309.920688	457.65225	50.85025	457.65225	0.025	0.025	15.38	\N	0.05	30.75	645.75	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-18 18:45:16.477797+00	2025-12-18 18:45:16.477797+00	47.667538089616016
1598	144	TUBO RETANGULAR 60X40X2,00X6000 - 2 BRS	38	0	6.28	0.18	0	4.673262	4.439599	40	9.28	0.12	7.411008	2	66.92967090045745	177.583956	296.44032	0.185275	296.44032	0.04	0.04	14.85	\N	0.05	18.56	389.6	{"has_difference": true, "absolute_difference": 2.0, "percentage_difference": 5.2631578947368425, "formatted_display": "5.3%"}	2025-12-18 18:45:53.998925+00	2025-12-18 18:45:53.998925+00	66.92967466047439
1599	123	TUBO REDONDO 25,40X0,90X6000 - 95 BRS	380	5	7.17	0.18	0	5.335556	5.335556	380	9.09	0.18	6.764324	0	26.778240168409816	2027.51128	2570.44312	0.017801	2570.44312	0.01	0.01	34.54	\N	0.0325	112.26	3568.2000000000003	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-18 18:48:07.355212+00	2025-12-18 18:48:07.355212+00	26.778240168409816
1600	123	TUBO REDONDO 22,22X0,90X6000 - 105 BRS	315	5	7.17	0.18	0	5.335556	5.335556	315	9.09	0.18	6.764324	0	26.778240168409816	1680.70014	2130.76206	0.021474	2130.76206	0.01	0.01	28.63	\N	0.0325	93.06	2957.8500000000004	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-18 18:48:07.355212+00	2025-12-18 18:48:07.355212+00	26.778240168409816
1601	123	TUBO REDONDO 31,75X0,90X6000 - 45 BRS	225	5	7.17	0.18	0	5.335556	5.335556	225	9.09	0.18	6.764324	0	26.778240168409816	1200.5001	1521.9729	0.030064	1521.9729	0.01	0.01	20.45	\N	0.0325	66.47	2112.75	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-18 18:48:07.355212+00	2025-12-18 18:48:07.355212+00	26.778240168409816
1602	123	TUBO REDONDO 58,80X1,20X6000  - 45 BRS	405	0	6.27	0.12	0	5.007222	5.007222	405	8.83	0.18	6.570845	0	31.227355208137364	2027.92491	2661.1922250000002	0.016224	2661.1922250000002	0.015	0.015	53.64	\N	0.0325	116.22	3693.6	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-18 18:48:07.355212+00	2025-12-18 18:48:07.355212+00	31.227355208137375
1413	137	CANTONEIRA 2'' X 1/8 	4	1	99	0.12	0	79.0614	79.0614	4	128.7	0.12	102.77982	0	30	316.2456	411.11928	25.694955	411.11928	0.05	0.05	25.74	\N	0	0	514.8	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-17 11:52:44.968645+00	2025-12-17 11:52:44.968645+00	29.999999999999982
1424	140	24 brs- tb101x4,75x6000mm	2000	5	5.98	0.12	0	4.775628	4.775628	2000	8	0.12	6.3888	0	33.77926421404682	9551.256	12777.6	0.003194	12777.6	0.015	0.015	240	\N	0.0325	520	16520	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-17 13:09:36.099841+00	2025-12-17 13:09:36.099841+00	33.77926421404685
1425	133	144-TB S/C SCH40 1.1/2  API 5 L	3500	2	17.25	0.18	0	12.836588	12.836588	3500	23	0.18	17.11545	0	33.33332813984526	44928.058	59904.075	0.00489	59904.075	0.015	0.015	1207.5	\N	0	0	80500	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-17 13:13:19.346414+00	2025-12-17 13:13:19.346414+00	33.333328139845264
1427	141	04 PÇS TB610X9,53X400MM	240	2	13.25	0.18	0	9.859988	9.859988	240	20	0.18	14.883	0	50.94338857207534	2366.39712	3571.9199999999996	0.062013	3571.9199999999996	0.03	0.03	144	\N	0.0325	156	4956	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-17 14:21:09.998998+00	2025-12-17 14:21:09.998998+00	50.94338857207532
1585	152	TUBO REDONDO 25,40X2,00X6000 - 1 BR	7	0	5.56	0.12	0	4.440216	4.440216	7	7.83	0.18	5.826695	0	31.225485426835093	31.081512	40.786865	0.832385	40.786865	0.015	0.015	0.82	\N	0.0325	1.78	56.56	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-18 18:44:26.606595+00	2025-12-18 18:44:26.606595+00	31.2254854268351
1586	152	TUBO REDONDO 88,90X6,30X6000 - 1 BR	77	0	6.18	0.12	0	4.935348	4.935348	77	8.69	0.18	6.466664	0	31.027518221612745	380.021796	497.93312799999995	0.083983	497.93312799999995	0.015	0.015	10.04	\N	0.0325	21.75	690.69	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-18 18:44:26.606595+00	2025-12-18 18:44:26.606595+00	31.027518221612738
1548	149	CANTONEIRA 150 X 100 X 3,00 X 6000 - 10 BR	353	5	8.6	0.18	0	6.39969	6.39969	353	11.31	0.18	8.416337	0	31.511635719855178	2259.09057	2970.966961	0.023842	2970.966961	0.015	0.015	59.89	\N	0	0	3992.4300000000003	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-18 13:43:09.934933+00	2025-12-18 13:43:09.934933+00	31.511635719855203
1452	143	100 X 50 X 2,00 X 6000 - 30 BR 	855	1	5.98	0.12	0	4.775628	4.775628	855	7.57	0.07	6.388891	0	33.781169722599834	4083.16194	5462.501805	0.007472	5462.501805	0.015	0.015	97.09	\N	0.05	323.62	6797.25	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-17 18:42:34.535235+00	2025-12-17 18:42:34.535235+00	33.781169722599834
1453	143	200 X 100 X 4,25 X 6000 - 4 BR 	500	4	6.55	0.12	0	5.23083	5.23083	500	8.27	0.07	6.979673	0	33.433374818145495	2615.415	3489.8365	0.013959	3489.8365	0.015	0.015	62.03	\N	0.05	206.75	4340	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-17 18:42:34.535235+00	2025-12-17 18:42:34.535235+00	33.4333748181455
1454	143	200 X 100 X 4,75 X 6000 - 4 BR 	524	4	6.55	0.12	0	5.23083	5.23083	524	8.27	0.07	6.979673	0	33.433374818145495	2740.95492	3657.348652	0.01332	3657.348652	0.015	0.015	65	\N	0.05	216.67	4548.32	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-17 18:42:34.535235+00	2025-12-17 18:42:34.535235+00	33.4333748181455
1549	149	CANTONEIRA 3/4 X 1/8 - 5 BR	27	5	6.9	0.12	0	5.51034	5.51034	27	9	0.12	7.1874	0	30.434782608695656	148.77918	194.0598	0.2662	194.0598	0.015	0.015	3.65	\N	0	0	243	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-18 13:43:09.934933+00	2025-12-18 13:43:09.934933+00	30.434782608695656
1550	149	CANTONEIRA 100 X 100 X 3,00 X 6000 - 5 BR 	141	5	8.6	0.18	0	6.39969	6.39969	141	11.31	0.18	8.416337	0	31.511635719855178	902.35629	1186.7035170000001	0.05969	1186.7035170000001	0.015	0.015	23.92	\N	0	0	1594.71	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-18 13:43:09.934933+00	2025-12-18 13:43:09.934933+00	31.511635719855203
1556	151	30 X 30 X 1,95	190	0	88	0.18	0	65.4852	65.4852	190	113	0.12	90.2418	0	37.80487804878049	12442.188	17145.942	0.474957	17145.942	0.015	0.015	322.05	\N	0	0	21470	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-18 13:53:46.765917+00	2025-12-18 13:53:46.765917+00	37.80487804878048
1573	153	50- TB RED GAL 50.80X3X6000MM	1092	4	6.44	0.12	2.17	7.312984	7.312984	1092	13.3	0.18	9.897195	0	35.337298700503105	7985.778528	10807.73694	0.009063	10807.73694	0.015	0.015	217.85	\N	0.0325	472.02	14993.16	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-18 14:34:47.72826+00	2025-12-18 14:34:47.72826+00	35.337298700503105
1587	152	TUBO REDONDO 101,60X5,74X6000 - 1 BR	81	0	6.35	0.12	0	5.07111	5.07111	81	8.93	0.18	6.64526	0	31.04152739735482	410.75991	538.26606	0.08204	538.26606	0.015	0.015	10.85	\N	0.0325	23.51	746.82	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-18 18:44:26.606595+00	2025-12-18 18:44:26.606595+00	31.04152739735484
1588	150	CHAPA XADREZ 1200X440X4,75 - 17 PÇS - UNIDADE POR PÇ	17	5	210.8	0.18	0	156.86682	156.86682	17	276	0.18	205.3854	0	30.929791271347252	2666.73594	3491.5518	12.081494	3491.5518	0.015	0.015	70.38	\N	0.0325	152.49	4844.490000000001	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-18 18:44:54.854285+00	2025-12-18 18:44:54.854285+00	30.929791271347252
1461	142	30 X 30 X 1,55 X 6000 - 7 BR	60	4	6.98	0.12	0	5.574228	5.574228	60	9.77	0.18	7.270346	0	30.427854763027273	334.45368	436.22076	0.121172	436.22076	0.015	0.015	8.79	\N	0.05	29.31	615.6	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-17 18:44:52.779681+00	2025-12-17 18:44:52.779681+00	30.427854763027273
1462	142	80 X 40 X 1,55 X 6000 - 5 BR 	90	4	7.1	0.18	1.53	6.813465	6.813465	90	11.95	0.18	8.892593	0	30.51498760175623	613.21185	800.33337	0.098807	800.33337	0.015	0.015	16.13	\N	0.05	53.78	1129.5	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-17 18:44:52.779681+00	2025-12-17 18:44:52.779681+00	30.514987601756218
1463	142	60 X 40 X 1,55 X 6000 - 4 BR	60	4	6.17	0.12	1.53	6.457362	6.457362	60	11.3	0.18	8.408895	0	30.221830524601224	387.44172	504.53369999999995	0.140148	504.53369999999995	0.015	0.015	10.17	\N	0.05	33.9	712.1999999999999	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-17 18:44:52.779681+00	2025-12-17 18:44:52.779681+00	30.221830524601213
1464	142	40 X 40 X 1,55 X 6000 - 4 BR	45	4	6.98	0.12	0	5.574228	5.574228	45	9.77	0.18	7.270346	0	30.427854763027273	250.84026	327.16557	0.161563	327.16557	0.015	0.015	6.59	\N	0.05	21.98	461.7	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-17 18:44:52.779681+00	2025-12-17 18:44:52.779681+00	30.427854763027273
1465	142	30 X 20 X 1,55 X 6000 - 70 BR	490	4	6.98	0.12	0	5.574228	5.574228	490	9.77	0.18	7.270346	0	30.427854763027273	2731.37172	3562.46954	0.014837	3562.46954	0.015	0.015	71.81	\N	0.05	239.37	5027.4	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-17 18:44:52.779681+00	2025-12-17 18:44:52.779681+00	30.427854763027273
1466	142	50,80 X 1,55 X 6000 - 6 BR	70	4	6.23	0.12	1.53	6.505278	6.505278	70	11.37	0.18	8.460986	0	30.063403900648055	455.36946	592.26902	0.120871	592.26902	0.015	0.015	11.94	\N	0.0325	25.87	821.8000000000001	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-17 18:44:52.779681+00	2025-12-17 18:44:52.779681+00	30.063403900648055
1589	150	TUBO REDONDO 25,40X2,00X6000 - 8 BRS	58	5	5.56	0.12	0	4.440216	4.440216	58	7.85	0.18	5.841578	0	31.560671823172566	257.532528	338.811524	0.100717	338.811524	0.015	0.015	6.83	\N	0.0325	14.8	470.38	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-18 18:44:54.854285+00	2025-12-18 18:44:54.854285+00	31.56067182317257
1590	150	TUBO REDONDO 50,80X2,00X6000 - 4 BRS	62	5	5.58	0.12	0	4.456188	4.456188	62	7.85	0.18	5.841578	0	31.08912819656621	276.283656	362.177836	0.094219	362.177836	0.015	0.015	7.3	\N	0.0325	15.82	502.81999999999994	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-18 18:44:54.854285+00	2025-12-18 18:44:54.854285+00	31.089128196566218
1591	150	CHAPA XADREZ 1000X1200X4,75 - 1 PÇ - UNIDADE POR PÇ	1	5	480	0.18	0	357.192	357.192	1	624	0.18	464.3496	0	30	357.192	464.3496	464.3496	464.3496	0.015	0.015	9.36	\N	0.0325	20.28	644.28	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-18 18:44:54.854285+00	2025-12-18 18:44:54.854285+00	30.000000000000004
1592	150	BARRA CHATA 2"X1/4X6000 - 1 BR	16	5	6.5	0.12	0	5.1909	5.1909	16	8.45	0.12	6.74817	0	30	83.0544	107.97072	0.421761	107.97072	0.015	0.015	2.03	\N	0	0	135.2	{"has_difference": false, "absolute_difference": 0.0, "percentage_difference": 0.0, "formatted_display": ""}	2025-12-18 18:44:54.854285+00	2025-12-18 18:44:54.854285+00	30.000000000000004
\.


--
-- Data for Name: budgets; Type: TABLE DATA; Schema: public; Owner: crm_user
--

COPY public.budgets (id, order_number, client_name, client_id, total_purchase_value, total_sale_value, total_sale_with_icms, total_commission, markup_percentage, profitability_percentage, total_ipi_value, total_final_value, status, notes, created_by, origem, outras_despesas_totais, freight_type, freight_value_total, payment_condition, valor_frete_compra, created_at, updated_at, expires_at, commission_percentage_actual, total_weight_difference_percentage) FROM stdin;
17	PROP-00006	Pilar Industria	\N	4970.946491	6482.9804952	8117.931999999999	121.75999999999999	\N	0.30417426679960613	123.67999999999999	8241.811999999998	approved	\N	aline	Cliente Ativo	0	CIF	\N	28/35/42/49	0	2025-11-27 13:47:11.942929+00	2025-11-28 11:37:23.958373+00	2025-11-30 03:00:00+00	0.015000000000000001	1.29
23	PROP-00012	TCI PROJETOS	\N	88678.162504	115338.71398499998	154993.9	2324.91	\N	0.3006439322623245	7749.700000000001	162818.3	approved	Foi liberado, está aguardando assinatura do ultimo gestor.	aline	Cliente Ativo	0	FOB	\N	À vista	0	2025-11-28 13:03:54.083072+00	2025-12-11 18:36:23.902031+00	2025-12-12 03:00:00+00	0.014999999999999998	0.95
40	PROP-00029	SALOC	\N	134162.00489999997	175187.32564	242822.49999999997	3642.33	\N	0.3057894131097622	0	242822.49999999997	lost	Cliente não responde mais.	aline	Orpen Whatsapp	0	CIF	\N	30/45/60	0	2025-12-01 17:45:34.570961+00	2025-12-04 16:51:46.148991+00	2025-12-05 03:00:00+00	0.015	0
12	PROP-00001	Serralheria Carvalho	\N	310.33596	413.04792799999996	555.06	8.33	\N	0.33097024270084574	27.75	582.9000000000001	approved	\N	aline	Cliente Ativo	0	CIF	\N	21	0	2025-11-24 14:16:40.890658+00	2025-11-24 18:06:48.9645+00	2025-11-28 03:00:00+00	0.015	0
15	PROP-00004	SERRALHERIA CARVALHO	\N	1189.131372	1590.695168	2137.6	32.06	\N	0.33769506503273045	106.88	2245.12	lost	\N	aline	Cliente Ativo	0	CIF	\N	28/35	0	2025-11-26 12:38:31.642187+00	2025-12-02 14:43:11.823545+00	2025-11-28 03:00:00+00	0.015000000000000001	2.81
22	PROP-00011	SUPRAFER	\N	23045.58135	30231.837900000002	40626	609.39	\N	0.3118279569892474	0	40626	sent	\N	adriana	Orpen Whatsapp	0	FOB	\N	7	0	2025-11-28 11:39:41.207549+00	2025-11-28 12:12:18.375808+00	2025-12-05 03:00:00+00	0.015	0
21	PROP-00010	TIBRE	\N	29382.0912	38338.608	51520	772.8	\N	0.30482911304829113	1674.4	53200	sent	\N	adriana	Indicacao	0	FOB	\N	28	0	2025-11-27 20:12:49.60462+00	2025-11-28 12:13:41.59574+00	2025-12-05 03:00:00+00	0.015	0
36	PROP-00025	MUNDO AZUL	\N	722.68998	1017.327465	1367.1	34.18	\N	0.4076955446372731	44.43	1411.74	approved	MATERIAL PRECISA FORMAR LOTE PARA GALVANIZAR	luciana	Cliente Ativo	141.36	CIF	\N	À vista	0	2025-12-01 16:27:50.446565+00	2025-12-02 14:46:57.067656+00	2025-12-10 03:00:00+00	0.025	0
45	PROP-00040	ADRIAÇO	\N	31968.855932000002	41897.523525	52535	690.28	\N	0.3105731282382757	2608.46	55156.59	approved	frete meio a meio ditual cliente	adriana	Orpen Whatsapp	0	FOB	1500	30/45/60	0.203528	2025-12-02 14:05:21.955097+00	2025-12-16 16:31:10.577727+00	2025-12-12 03:00:00+00	0.013139240506329116	0
26	PROP-00015	Jodi - CYRELA	\N	14517.901134	18469.796942	24819.99	248.2	\N	0.27220848051822805	1241	26065.14	lost	Cliente quer pegar tudo em um lugar só - 36 barras	aline	Cliente Ativo	0	CIF	\N	28	0	2025-11-28 16:15:08.272072+00	2025-12-04 16:50:48.011516+00	2025-12-13 03:00:00+00	0.01	0
18	PROP-00007	PROJINOX	\N	10286.013375	13711.1634	17169	257.53	\N	0.3329910141206675	557.99	17721.899999999998	lost	tem preço a R$ 8,20kg + ipi	aline	Cliente Ativo	0	CIF	\N	28/35/42/49	0	2025-11-27 16:54:32.847937+00	2025-11-27 17:23:46.360739+00	2025-11-28 03:00:00+00	0.014999999999999998	0
20	PROP-00009	PATRICIO	\N	1850.25416	2450.1048	3068	46.02	\N	0.3241990494970702	0	3068	sent	CONDIÇÃO DE PAGAMENTO LIBERADO APÓS ANÁLISE DE CRÉDITO	adriana	Orpen Whatsapp	512.12	FOB	\N	21	0	2025-11-27 17:49:08.512778+00	2025-11-27 17:51:45.148826+00	2025-12-05 03:00:00+00	0.015	0
24	PROP-00013	PISOMETAL	\N	6519.3311699999995	8547.381825	11486.1	172.29	\N	0.311082625213531	574.31	12064.7	lost	1 ITEM, FECHOU NA FABRICA O OUTRO TEVE PREÇO MELHOR EM DISTRIBUIÇÃO	luciana	Cliente Ativo	0	CIF	\N	28/35/42	0	2025-11-28 13:04:36.430271+00	2025-12-02 14:50:40.075862+00	2025-11-30 03:00:00+00	0.015000000000000001	0
35	PROP-00024	ROLETESKAR	\N	230.891232	303.76205600000003	408.2	6.12	\N	0.3156067182317258	20.41	428.48	approved	\N	luciana	Cliente Ativo	0	CIF	\N	28	0	2025-12-01 13:59:51.155827+00	2025-12-02 14:47:48.816969+00	2025-12-17 03:00:00+00	0.015	0
33	PROP-00022	 NARJE ORPEN	\N	11273.13224	14430.334190000001	19391.7	222.23	\N	0.2800643053576032	969.59	20367.7	sent	os itens que não constam no orçamento é devido a não termos em estoque, por hora sem previsão	adriana	Orpen Whatsapp	0	FOB	\N	7	0	2025-11-28 19:08:10.070347+00	2025-12-01 18:04:52.01562+00	2025-12-05 03:00:00+00	0.011460031869304908	0
30	PROP-00019	SERRALHERIA CARVALHO	\N	2084.38593	2725.8613800000003	3413.3	42.58	\N	0.3077527250435817	0	3413.3	lost	somente para saber preço	aline	Cliente Ativo	0	CIF	\N	28/35/42	0	2025-11-28 18:41:46.9365+00	2025-12-04 16:51:20.83298+00	2025-12-05 03:00:00+00	0.012472387425658451	0
29	PROP-00018	JODI - SICON	\N	10561.583009999998	13963.602799999999	18764.5	281.46	\N	0.3221126782584462	938.23	19709.7	lost	PREÇO	aline	Cliente Ativo	0	CIF	\N	30	0	2025-11-28 16:53:55.087908+00	2025-12-11 16:39:10.227286+00	2025-12-05 03:00:00+00	0.014999999999999998	0
28	PROP-00017	RODRIGO	\N	3342.364608	4474.641127	6013.09	90.19999999999999	\N	0.33876511146925115	300.65	6312.32	sent	\N	aline	Cliente Ativo	0	CIF	\N	À vista	0	2025-11-28 16:43:22.14925+00	2025-11-28 16:43:31.99682+00	2025-12-05 03:00:00+00	0.015	0
38	PROP-00027	REFRIN	\N	1002.898317	1510.140884	2029.35	56.900000000000006	\N	0.5057766658910446	65.96	2094.55	sent	\N	aldo	Cliente Ativo	252.81	CIF	\N	28	0	2025-12-01 17:29:24.056308+00	2025-12-01 18:05:50.231882+00	2025-12-05 03:00:00+00	0.028036809815950924	2.52
34	PROP-00023	CARESE	\N	983.301179	1304.8325399999999	1633.9	19.369999999999997	\N	0.32699173749287236	63.69	1697.52	approved	\N	luciana	Reativacao Cliente	0	FOB	\N	28	0	2025-12-01 12:20:50.653353+00	2025-12-03 14:16:44.152783+00	2025-12-15 03:00:00+00	0.011852010526960034	0
19	PROP-00008	FALTEC	\N	347.03163	468.02497500000004	614.0999999999999	9.209999999999999	\N	0.34865221075093367	20.57	634.8	approved	\N	luciana	Cliente Ativo	0	CIF	\N	21	0	2025-11-27 17:46:50.720176+00	2025-12-02 14:48:37.5703+00	2025-11-30 03:00:00+00	0.015000000000000003	0
41	PROP-00030	MADEMETAL	\N	496.665312	663.246064	891.28	13.37	\N	0.33539840205309124	44.56	936	sent	\N	aline	Cliente Ativo	0	CIF	\N	À vista	0	2025-12-01 17:50:38.979871+00	2025-12-01 17:50:50.961007+00	2025-12-05 03:00:00+00	0.015	0
32	PROP-00021	JODI - ZION	\N	2850.690546	3753.306866	5043.75	75.66	\N	0.31663076206799196	252.19	5294.08	approved	\N	aline	Cliente Ativo	0	CIF	\N	30	0	2025-11-28 18:49:47.860223+00	2025-12-01 14:48:17.594987+00	2025-12-05 03:00:00+00	0.015	0.33
16	PROP-00005	TRUCKVAN	\N	1004.6388	1285.8912	1728	17.28	\N	0.27995375054198585	86.4	1814	lost	\N	luciana	Cliente Ativo	0	CIF	\N	30	0	2025-11-26 20:24:02.489124+00	2025-12-02 14:47:24.826949+00	2025-11-30 03:00:00+00	0.01	0
31	PROP-00020	ESTRUTUURAS METALICAS ORPEN	\N	1364.12859	1774.94658	2385.2	30.12	\N	0.30115781826697147	119.27000000000001	2505.8	sent	\N	adriana	Orpen Whatsapp	0	FOB	\N	21	0	2025-11-28 18:48:02.094345+00	2025-12-01 18:04:18.270341+00	2025-12-05 03:00:00+00	0.012630597014925374	0
27	PROP-00016	Jodi - Mitre	\N	15872.267264	20868.624311	28043.57	420.65	\N	0.3147853399830453	1402.18	29433.879999999997	lost	NÃO TINHAMOS TODOS OS ITENS SOLICITADOS.	aline	Cliente Ativo	0	CIF	\N	28	0	2025-11-28 16:26:02.733731+00	2025-12-11 16:38:31.693955+00	2025-12-12 03:00:00+00	0.015	0
37	PROP-00026	MULTH TECNOLOGIAS	\N	4392.489257	5717.60211	7683.4	89.38	\N	0.3016769707263965	384.16999999999996	8067.57	sent	\N	adriana	Orpen Whatsapp	0	FOB	\N	7	0	2025-12-01 17:18:50.636758+00	2025-12-01 18:02:49.818273+00	2025-12-12 03:00:00+00	0.011632870864461046	0
25	PROP-00014	CONFORMI	\N	3611.94075	4544.561076	5690.66	58.53	\N	0.2582047687244039	0	5690.660000000001	lost	TEVE PREÇO PROXIMO DO MEU CUSTO	luciana	Cliente Ativo	0	FOB	\N	28/35/42	0	2025-11-28 14:13:04.729304+00	2025-12-02 14:51:57.155988+00	2025-11-30 03:00:00+00	0.010283271184713196	0
43	PROP-00032	BRACI MOVEIS	\N	832.06134	1091.04732	1366.2	20.49	\N	0.31125827814569534	68.31	1435.2	approved	\N	adriana	Orpen Whatsapp	0	CIF	\N	À vista	0	2025-12-02 12:30:16.440785+00	2025-12-02 13:40:11.487938+00	2025-12-05 03:00:00+00	0.014999999999999998	0
42	PROP-00031	KMV	\N	14004.16038	18212.47593	24474.2	367.11	\N	0.30050466688528454	1223.71	25713.4	draft	\N	aldo	Prospeccao	0	CIF	\N	30/45/60	0	2025-12-01 20:45:21.831276+00	2025-12-02 20:32:50.383862+00	2025-12-01 03:00:00+00	0.015	1.24
13	PROP-00002	THE BEST WAY SERVICE	\N	21642.56094	29081.498159999996	36415.6	546.23	\N	0.34371797499487583	0	36415.6	lost	cliente não respondeu mais.	aline	Orpen Whatsapp	0	FOB	\N	30/45/60	0	2025-11-24 14:45:59.772166+00	2025-12-04 16:50:05.835922+00	2025-11-28 03:00:00+00	0.015000000000000001	0
39	PROP-00028	SANASA	\N	61189.929899999996	79808.362524	99935.34	1499.03	\N	0.3042728215970714	0	99935.34	sent	Enviado por e-mail.	aline	Primeiro Google	0	CIF	\N	30/45/60	0	2025-12-01 17:31:29.8341+00	2025-12-02 13:46:36.578379+00	2025-12-05 03:00:00+00	0.014999999999999998	3.04
57	PROP-00047	RTK	\N	1525.991355	1938.548115	2605.05	26.05	\N	0.2703532747077719	84.66	2690.1	sent	\N	luciana	Cliente Ativo	0	CIF	\N	28/35/42	0	2025-12-03 14:19:18.270013+00	2025-12-03 14:19:27.740776+00	2025-12-15 03:00:00+00	0.01	0
14	PROP-00003	MULTIENERGIA	\N	74716.03600000001	95199.85380000001	127931	1279.31	\N	0.2741555748487513	2755.25	130686	lost	PREÇO	aline	Orpen Whatsapp	0	CIF	0	30/45/60	0	2025-11-26 12:13:38.183308+00	2025-12-02 14:42:40.664681+00	2025-11-28 03:00:00+00	0.01	0
46	PROP-00035	FALTEC	\N	821.416002	1076.0037889999999	1445.9499999999998	21.689999999999998	\N	0.3099377007267018	30.58	1476.73	approved		luciana	Cliente Ativo	0	CIF	\N	28	0	2025-12-02 14:17:18.181577+00	2025-12-02 14:46:28.780604+00	2025-12-15 03:00:00+00	0.015000000000000003	0
48	PROP-00037	CARESE	\N	2999.6214600000003	3899.1645	4882.5	64.68	\N	0.2998855195548573	85.58	4968.3	sent	\N	luciana	Reativacao Cliente	0	FOB	\N	30	0	2025-12-02 16:35:30.666737+00	2025-12-02 16:35:40.41065+00	2025-12-15 03:00:00+00	0.013247209421402967	0
50	PROP-00039	GET TANKS LOCACAO DE EQUIPAMENTOS LTDA	\N	55501.62189	72138.09702	90330.7	2665.19	\N	0.29974754905311113	1504.22	91839.56999999999	sent	\N	luciana	Orpen Whatsapp	0	FOB	\N	28/35/42	0	2025-12-02 17:14:49.678325+00	2025-12-02 17:15:56.669164+00	2025-12-15 03:00:00+00	0.02950477080328172	0
44	PROP-00033	ARAMADOS BRAGANÇA	\N	7633.009362	9959.292684	12470.939999999999	187.07	\N	0.30476620840806457	527.75	12994.26	lost	PREÇO, PERDEMOS PARA NOROAÇO r$ 7,60KG	aline	Cliente Ativo	0	FOB	\N	28/35/42/49	0	2025-12-02 13:40:54.232292+00	2025-12-02 19:39:49.954513+00	2025-12-05 03:00:00+00	0.015000000000000001	0
54	PROP-00044	MARCO	\N	1717.756656	2251.827666	3026.04	45.39	\N	0.31091191417278374	151.3	3176.34	sent	FRETE CIF ATÉ 60KM	luciana	Orpen Whatsapp	0	CIF	\N	28	0	2025-12-03 12:18:30.764082+00	2025-12-03 12:18:41.651975+00	2025-12-15 03:00:00+00	0.015	0
71	PROP-00061	SER-COP	\N	866.96016	1157.004512	1554.8	23.32	\N	0.3345532648236108	50.53	1604.48	lost	\N	aline	Cliente Ativo	0	CIF	\N	28	0	2025-12-04 18:24:27.53864+00	2025-12-11 16:39:41.37601+00	2025-12-05 03:00:00+00	0.015	0
53	PROP-00043	DIRSAN ELEVADORES	\N	1686.7869480000002	2273.4155180000002	3055.05	45.83	\N	0.3477786988425286	148.19	3204.49	approved	\N	aline	Cliente Ativo	0	CIF	\N	28/35/42	0	2025-12-03 12:05:52.670827+00	2025-12-03 18:55:28.433542+00	2025-12-05 03:00:00+00	0.015	0
55	PROP-00045	TRUCKVAN	\N	1298.04444	1648.214568	2063.88	20.64	\N	0.26976744186046514	0	2063.8799999999997	sent	\N	luciana	Cliente Ativo	0	CIF	\N	30	0	2025-12-03 13:59:26.356981+00	2025-12-03 14:03:29.66989+00	2025-12-15 03:00:00+00	0.01	0
58	PROP-00048	PROJECT LASER	\N	5961.409971000001	7768.574492	10298.93	152.48000000000002	\N	0.30314380822509596	352.04	10652.77	draft	\N	aldo	\N	0	FOB	\N	30/45/60	0	2025-12-03 14:34:29.309074+00	2025-12-03 16:31:23.399295+00	2025-12-09 03:00:00+00	0.01480556232540662	0
56	PROP-00046	ALPINO	\N	1256.5971	1651.6410500000002	2219.5	33.71	\N	0.31437598415594004	72.13	2292	sent	\N	luciana	Cliente Ativo	0	FOB	\N	28/35/42	0	2025-12-03 14:04:50.630191+00	2025-12-03 14:15:45.090005+00	2025-12-15 03:00:00+00	0.015189231808965982	0
51	PROP-00041	VIVAX	\N	1312.6806	1706.48478	2293.2	114.66	\N	0.3	74.53	2367	approved	\N	luciana	Cliente Ativo	0	CIF	\N	28/35/42	0	2025-12-02 17:38:21.597244+00	2025-12-03 14:16:03.045455+00	2025-12-15 03:00:00+00	0.05	0
61	PROP-00051	USIFLEX	\N	301.367682	422.61912	529.2	13.23	\N	0.4023372287145242	0	529.2	sent	ESTAREMOS EM FÉRIAS CLETIVAS DE 19/12/2025 Á 04/01/2026.	luciana	Orpen Whatsapp	0	FOB	\N	À vista	0	2025-12-03 16:36:28.098127+00	2025-12-03 16:36:38.061209+00	2025-12-15 03:00:00+00	0.025	0
67	PROP-00057	DKN	\N	1798.48713	2331.912	2920	29.2	\N	0.2965964343598055	94.9	3014.9	sent	TRANSPORTADORA SJP	adriana	Cliente Ativo	0	FOB	\N	28/35/42	0	2025-12-04 13:21:47.680329+00	2025-12-09 16:30:03.479343+00	2025-12-12 03:00:00+00	0.01	0
52	PROP-00042	FTDE	\N	137.36102000000002	174.89339999999999	224.39999999999992	2.98	\N	0.27323894362461754	0	224.39999999999992	sent	\N	adriana	Orpen Whatsapp	40.97	FOB	\N	À vista	0	2025-12-02 18:59:48.272653+00	2025-12-03 17:08:25.087873+00	\N	0.013235294117647064	0
59	PROP-00049	CALLEVE	\N	2234.754324	2937.9042	3948	59.22	\N	0.31464303187539105	183.95999999999998	4131.96	approved	CONSIDERAR A UNIDADE PÇ	luciana	Cliente Ativo	0	CIF	\N	À vista	0	2025-12-03 14:47:41.221074+00	2025-12-03 17:33:31.816248+00	2025-12-15 03:00:00+00	0.015	0
47	PROP-00036	SEUMA	\N	12618.92372	17191.4622	21527	322.91	\N	0.36235566372058237	1076.35	22604.3	draft	faturamento correto 30/50	aldo	\N	0	FOB	\N	30/45	0	2025-12-02 14:51:47.968517+00	2025-12-03 17:54:24.569159+00	2025-12-09 03:00:00+00	0.015	0
68	PROP-00058	NOSSA EMGENHARIA	\N	3449.9519999999998	4570.351500000001	6115	89.9	\N	0.324757996632997	287.5	6402.5	draft	\N	aldo	\N	0	CIF	\N	À vista	0	2025-12-04 17:48:17.614013+00	2025-12-04 18:37:29.286653+00	2025-12-09 03:00:00+00	0.014701553556827474	0
63	PROP-00053	GTRUCK	\N	2538.700758	3308.133837	4445.52	55.08	\N	0.30308143902953055	0	4445.52	approved	\N	luciana	Cliente Ativo	0	FOB	\N	À vista	0	2025-12-03 18:26:44.757778+00	2025-12-03 19:17:36.148706+00	2025-12-15 03:00:00+00	0.012391283809318145	0
64	PROP-00054	GTRUCK	\N	3310.085196	4574.521127	6147.3099999999995	92.21	\N	0.3819949808325115	10.48	6157.71	sent	60X60 ESTOU COM PEDIDO NA FABRICA PARA ENTREGA EM ATE 5 DIAS	luciana	Cliente Ativo	0	CIF	\N	À vista	0	2025-12-03 19:15:15.745384+00	2025-12-03 19:21:28.520923+00	2025-12-15 03:00:00+00	0.014999999999999998	0
70	PROP-00060	SOSED COMERCIAL	\N	15350.671049999999	20180.622	25270	415.15	\N	0.3146410299763411	180.5	25450.5	draft	saiu em kgs mais é por br ok	aldo	\N	0	FOB	\N	28/35/42	0	2025-12-04 18:00:37.092062+00	2025-12-04 18:06:21.54332+00	2025-12-09 03:00:00+00	0.016428571428571428	0
65	PROP-00055	CMC MODULOS	\N	17311.33206	22492.616916	28165.06	339.98	\N	0.29930018314257906	1384.6999999999998	29542.590000000004	sent	50X50 TENHO METADE PARA IMEDIATO	luciana	Cliente Ativo	0	FOB	\N	30/45/60	0	2025-12-03 20:05:56.583206+00	2025-12-03 20:07:17.375971+00	2025-12-15 03:00:00+00	0.01207103411105817	0
60	PROP-00050	KMW	\N	5020.686396	12153.814992	16332.48	816.62	\N	1.4207476893364601	816.62	17152.920000000002	lost	TEM POR R$8,10 DA ROMEVA\nDARIA 13% DE MARGEM	luciana	Reativacao Cliente	0	CIF	\N	28/35/42	0	2025-12-03 16:20:31.882648+00	2025-12-04 17:17:10.173868+00	2025-12-15 03:00:00+00	0.05	100
66	PROP-00056	LAUDELINO	\N	12707.552252999998	17372.50482	21753.7	389.53000000000003	\N	0.36710079755121217	1087.69	22850.829999999998	sent	\N	adriana	Indicacao	0	CIF	\N	À vista	0	2025-12-04 12:13:07.807042+00	2025-12-09 16:28:58.763521+00	2025-12-12 03:00:00+00	0.017906264221718603	0
72	PROP-00062	FACCHINI	\N	14394.060000000001	17762.861	23870	238.7	\N	0.23404105582441637	775.78	24650	sent	FRETE CIF ATÉ 60KM	luciana	Reativacao Cliente	2190	CIF	\N	28/35/42	0	2025-12-04 18:37:31.233938+00	2025-12-04 18:38:07.201957+00	2025-12-15 03:00:00+00	0.01	0
73	PROP-00063	TRAMAFE	\N	5369.779006	7509.2180180000005	10091	188.43	\N	0.3984221714915023	504.55000000000007	10594.42	sent	ESTAREMOS EM FERIAS COLETIVAS DE 19/12/25 Á 04/01/26	luciana	Email Vendas	0	FOB	\N	28/35/42	0	2025-12-04 19:11:03.605647+00	2025-12-04 19:11:22.272654+00	2025-12-10 03:00:00+00	0.01867313447626598	0
69	PROP-00059	INVICTOS	\N	418.4664	619.7135999999999	776	19.4	\N	0.4809160305343509	25.22	801.5999999999999	lost	\N	aline	Orpen Whatsapp	0	FOB	\N	À vista	0	2025-12-04 17:57:50.624411+00	2025-12-11 16:39:30.44006+00	2025-12-05 03:00:00+00	0.025	0
62	PROP-00052	FTA HORTIFRUTI	\N	10513.9683	13696.43145	18632.7	279.49	\N	0.30268905699477905	605.56	19235.7	sent	\N	aline	Orpen Whatsapp	0	FOB	\N	28/35/42	0	2025-12-03 17:20:55.652838+00	2025-12-05 16:59:08.419245+00	2025-12-05 03:00:00+00	0.015	0
49	PROP-00038	LRS	\N	48971.023199999996	62292.95429	73809	758.83	\N	0.2720370173927672	134.81	73943.2	draft	Cond. Pgto : 1 avista 30/60DD	laura	Cliente Ativo	0	FOB	\N	30	0	2025-12-02 16:50:41.567039+00	2025-12-09 14:06:22.592238+00	2025-12-05 03:00:00+00	0.010280995542549012	0.93
76	PROP-00066	AJV ESPORTES	\N	2504.993304	3298.0728	4432	66.47999999999999	\N	0.31659944748499014	108.5	4540.5	approved	\N	aline	Cliente Ativo	0	CIF	\N	28/35/42	0	2025-12-05 16:23:15.038094+00	2025-12-09 00:50:35.480097+00	2025-12-12 03:00:00+00	0.014999999999999998	0
74	PROP-00064	LM SERVIÇOS ORPEN	\N	9458.44416	12414.20796	16682.4	250.24	\N	0.3125	542.18	17218.62	sent	\N	adriana	Orpen Whatsapp	0	FOB	\N	7	0	2025-12-04 19:54:42.229942+00	2025-12-09 16:31:49.958173+00	2025-12-12 03:00:00+00	0.015	0
75	PROP-00065	AJV ESPORTES	\N	4003.3818	5257.4202000000005	7065	105.98	\N	0.31324476721156114	229.61	7298.999999999999	lost	preço - compra na sigma esse.	aline	Cliente Ativo	0	CIF	\N	28/35/42	0	2025-12-05 16:17:59.414878+00	2025-12-09 17:51:38.383867+00	2025-12-12 03:00:00+00	0.015	0
81	PROP-00071	Suprimentos 01 Capua 	\N	405.513108	600.9011250000001	807.5	20.19	\N	0.481829102796845	40.38	848.35	draft	1298312 2322	laura	Orpen Whatsapp	0	CIF	\N	À vista	0	2025-12-05 19:23:37.729107+00	2025-12-05 19:23:37.729107+00	2025-12-01 03:00:00+00	0.025	4.4
79	PROP-00069	AÇOS BTG	\N	217.023906	294.38574	395.6	5.93	\N	0.35646687697160884	12.86	408.48	sent	\N	adriana	Email Vendas	0	FOB	\N	7	0	2025-12-05 17:14:16.550814+00	2025-12-09 16:30:50.176762+00	2025-12-12 03:00:00+00	0.015	0
77	PROP-00067	ATT-SISTEMAS	\N	55454.058	73733.36319999999	99084	1486.26	\N	0.3296297125811783	3220.23	102304	lost	cliente declinou, vai usar outro material para o piso.	aline	Orpen Whatsapp	0	CIF	\N	30/45/60	0	2025-12-05 17:03:28.167824+00	2025-12-11 18:14:57.602767+00	2025-12-12 03:00:00+00	0.015	0
78	PROP-00068	Rafael Marques	\N	1085.3373299999998	1527.29346	2052.4	48.93	\N	0.407206236977033	102.62	2156.28	draft	12992083421	laura	Orpen Whatsapp	0	FOB	\N	À vista	0	2025-12-05 17:11:03.339355+00	2025-12-05 17:15:53.932118+00	2025-12-12 03:00:00+00	0.023840381991814465	2.86
80	PROP-00070	vista alegre	\N	2660.33625	3464.0182499999996	4655	69.83	\N	0.30209790209790194	151.29	4806.3	draft	\N	aldo	\N	0	CIF	\N	28/35/42	0	2025-12-05 17:46:22.529176+00	2025-12-05 17:46:22.529176+00	\N	0.015000000000000001	0
92	PROP-00082	SERRALHERIA CARVALHO	\N	1812.406728	2439.2792420000005	3277.94	49.17	\N	0.345878496429859	163.9	3440.5	sent	\N	aline	Cliente Ativo	0	CIF	\N	28/35/42	0	2025-12-09 19:39:55.286956+00	2025-12-09 19:40:08.155558+00	2025-12-12 03:00:00+00	0.015	0
84	PROP-00074	LS SUPRIMENTOS	\N	510.3054	1078.11	1350	67.5	\N	1.1126760563380282	0	1350	sent	material galvanizado a fogo prazo de 7 dias	adriana	Orpen Whatsapp	0	FOB	\N	7	0	2025-12-09 15:02:54.769669+00	2025-12-09 16:26:08.830976+00	2025-12-17 03:00:00+00	0.05	0
83	PROP-00073	VMAQ	\N	1657.127655	2329.99536	2917.6	71.07	\N	0.40604458139949395	145.88	3063.5899999999997	sent	\N	adriana	\N	0	CIF	\N	28/35	0	2025-12-09 13:57:25.469491+00	2025-12-09 16:26:40.806088+00	2025-12-12 03:00:00+00	0.024359062242939402	0
82	PROP-00072	ADRIAÇO	\N	3888.77907	5086.26525	6835	123.96000000000001	\N	0.30793371349841175	222.14	7059.079999999999	sent	\N	adriana	Prospeccao	0	FOB	\N	28/35/42	0	2025-12-09 12:50:49.236092+00	2025-12-09 16:29:31.53229+00	2025-12-12 03:00:00+00	0.01813547915142648	0
90	PROP-00080	SANASA	\N	73669.89168	97259.09820000001	121787	1620.41	\N	0.32020145519508125	0	121787	sent	frete cif  material com certificado e prazo de 4 dias entrega. lembrando que nosso estoque é rotativo, e reajuste conforme usina.	adriana	Email Vendas	0	FOB	\N	28/35	0	2025-12-09 18:24:54.634659+00	2025-12-09 20:00:34.359449+00	\N	0.013305237833266276	0
106	PROP-00096	JR ENGENHARIA	\N	13400.18856	17488.38168	21898.8	328.48	\N	0.3050847457627119	711.71	22609.8	lost	cliente caroço, só cota, não compra! Quer preço de fabrica ou material de segunda linha.	aline	Reativacao Cliente	0	CIF	\N	À vista	0	2025-12-11 13:26:33.71697+00	2025-12-11 13:53:44.696658+00	2025-12-12 03:00:00+00	0.015	0
110	PROP-00100	INTERSTEEL	\N	6375.1337	8466.7572	10032	150.48	\N	0.3280909230186027	0	10032	draft	\N	aldo	\N	0	FOB	\N	28/35/42	0	2025-12-11 16:53:34.768774+00	2025-12-11 16:54:14.282588+00	2025-12-16 03:00:00+00	0.015	1.54
101	PROP-00091	JMA	\N	34931.871150000006	46371.906899999994	58066.5	870.9999999999999	\N	0.32749564719495383	2747.6899999999996	60832.25	draft	916090480	laura	Orpen Whatsapp	0	CIF	\N	À vista	0	2025-12-10 17:21:29.746791+00	2025-12-10 17:32:44.694601+00	2025-12-16 03:00:00+00	0.015000000000000001	2.48
88	PROP-00078	JODI - MAC PINHEIROS	\N	2912.651892	3922.280876	5270.82	79.06	\N	0.34663565075287067	214.35	5485.64	sent	\N	aline	Cliente Ativo	0	CIF	\N	30	0	2025-12-09 18:11:35.77956+00	2025-12-09 18:11:44.720624+00	2025-12-12 03:00:00+00	0.015	0
89	PROP-00079	SERRALHERIA CARVALHO	\N	1039.673382	1397.439285	1877.9	28.17	\N	0.3441137468690143	93.9	1972.85	sent	\N	aline	Cliente Ativo	0	CIF	\N	28/35	0	2025-12-09 18:24:20.818356+00	2025-12-09 18:24:27.656857+00	2025-12-12 03:00:00+00	0.015	0
95	PROP-00085	TESSIN	\N	2943.967026	4064.994595	5398.13	80.97	\N	0.3807880859736233	225.86	5622.74	sent	ESTAREMOS EM FERIAS COLETIVAS DE 19/12 Á 04/01.\nVOLTAMOS AS ATIVIDADES EM 05/01/2026.	luciana	Cliente Ativo	0	CIF	\N	28/35/42	0	2025-12-10 13:56:10.869278+00	2025-12-10 14:04:25.392453+00	2025-12-15 03:00:00+00	0.014999999999999998	0
91	PROP-00081	JODI - VINCI GAFISA	\N	4518.31908	6100.4303199999995	8197.85	122.97	\N	0.3501548279321609	409.9	8609	sent	\N	aline	Cliente Ativo	0	CIF	\N	30	0	2025-12-09 18:37:24.021406+00	2025-12-09 18:37:31.439547+00	2025-12-12 03:00:00+00	0.015	0
102	PROP-00092	ILUMITEL	\N	2518.10559	3286.724805	4416.75	66.25	\N	0.3052370869801373	143.54	4563	draft	\N	adriana	Cliente Ativo	0	FOB	\N	28	0	2025-12-10 17:35:21.473194+00	2025-12-10 17:35:21.473194+00	2025-12-15 03:00:00+00	0.015	0
96	PROP-00086	RTE	\N	443.750076	577.99038	743.2	8.86	\N	0.30251330931603043	12.549999999999999	755.74	draft	\N	aldo	\N	0	CIF	\N	28	0	2025-12-10 14:09:12.468209+00	2025-12-10 14:09:12.468209+00	2025-12-12 03:00:00+00	0.011918729817007536	0
97	PROP-00087	IBAR	\N	2390.95395	3108.24027	4176.9	62.65	\N	0.30000005646281896	0	4176.900000000001	draft	\N	aldo	\N	0	CIF	\N	28/35/42	0	2025-12-10 14:19:18.481843+00	2025-12-10 14:19:18.481843+00	2025-12-12 03:00:00+00	0.015	0
98	PROP-00088	FERMAR	\N	13212.30921	17731.915227999998	21010	315.15999999999997	\N	0.3420754045461821	0	21010	draft	\N	aldo	\N	0	FOB	\N	28/35/42	0	2025-12-10 14:36:27.948303+00	2025-12-10 14:36:27.948303+00	2025-12-12 03:00:00+00	0.015	3
99	PROP-00089	ADRIAÇO	\N	20207.327184	26341.0224	32984	494.76	\N	0.30353817504655495	1649.2	34633.2	sent	\N	adriana	Prospeccao	0	FOB	\N	30/45/60	0	2025-12-10 16:14:42.091647+00	2025-12-10 17:56:07.214713+00	\N	0.015	0
100	PROP-00090	transferaço	\N	1280.283576	1680.9668689999999	2213.25	30.08	\N	0.31296448733011	79.46	2293.12	draft	\N	aldo	\N	0	CIF	\N	28/35/42	0	2025-12-10 16:35:08.773602+00	2025-12-10 16:35:08.773602+00	2025-12-12 03:00:00+00	0.013590308370044053	2.99
103	PROP-00093	RJ EX COMERCIO E SERVICOS	\N	4218.68436	5513.85384	6904.4	103.57	\N	0.30700791277022677	0	6904.4	sent	\N	aline	Orpen Whatsapp	0	FOB	\N	28/35/42	0	2025-12-10 19:30:03.920586+00	2025-12-10 19:30:07.674201+00	2025-12-12 03:00:00+00	0.015000000000000001	0
104	PROP-00094	KADOSH	\N	697.1777999999999	976.04892	1222.1999999999998	53.66	\N	0.4000000000000002	61.11	1283.3400000000001	draft	\N	aldo	\N	0	FOB	\N	À vista	0	2025-12-10 20:41:31.435524+00	2025-12-10 20:41:31.435524+00	2025-12-12 03:00:00+00	0.043900343642611694	0
105	PROP-00095	PERSPECTIVA SERVICOS TECNICOS INDUSTRIAIS	\N	442.0251	912.7998	1143	57.15	\N	1.065040650406504	37.15	1180.35	sent	\N	aline	Orpen Whatsapp	0	FOB	\N	21	0	2025-12-11 13:20:51.1397+00	2025-12-11 13:21:15.45795+00	2025-12-12 03:00:00+00	0.05	0
87	PROP-00077	PROJINOX	\N	226.72254	338.47664599999996	454.85	13.01	\N	0.49291131794836085	20.51	475.28999999999996	approved	\N	aline	Cliente Ativo	0	FOB	\N	21	0	2025-12-09 18:03:09.695597+00	2025-12-11 16:30:08.412636+00	2025-12-12 03:00:00+00	0.028599538309332744	0
86	PROP-00076	SCM INDUSTRIA E COMERCIO 	\N	8411.038878	10933.432949999999	13690.75	158.54000000000002	\N	0.29989090629429843	304.34	13989.49	sent	\N	luciana	Primeiro Google	0	CIF	\N	28/35/42	0	2025-12-09 17:45:17.840578+00	2025-12-11 13:47:10.764146+00	2025-12-15 03:00:00+00	0.011580044920840712	0
93	PROP-00083	PONTO CINCO	\N	5013.930240000001	6430.34898	8641.2	89.03	\N	0.28249669863775345	432.06	9074.6	approved	\N	luciana	Cliente Ativo	0	CIF	\N	7	0	2025-12-10 11:51:51.474713+00	2025-12-11 13:47:58.933731+00	2025-12-12 03:00:00+00	0.010302735731148451	0
109	PROP-00099	BWI Com.	\N	5278.26684	5684.58	20880	1044	\N	0.07697851819859869	678.6	21552	draft	\N	laura	Orpen Whatsapp	0	FOB	\N	À vista	0	2025-12-11 14:38:52.111376+00	2025-12-11 14:38:52.111376+00	2025-12-17 03:00:00+00	0.05	2.13
108	PROP-00098	METAL FIT	\N	3502.92096	5365.32164	7210	216.3	\N	0.5316707688431542	0	7210	sent	\N	aline	Primeiro Google	0	CIF	\N	28/35/42	0	2025-12-11 13:49:13.796105+00	2025-12-11 14:09:25.815612+00	2025-12-12 03:00:00+00	0.03	0
94	PROP-00084	PLASTMETAL	\N	8430.17769	11249.606676000001	14086.66	211.3	\N	0.33444478748584966	457.82	14545.539999999999	lost	PREÇO	aline	Cliente Ativo	0	FOB	\N	28/35/42/49	0	2025-12-10 13:35:39.229861+00	2025-12-11 16:36:11.782341+00	2025-12-12 03:00:00+00	0.015	0
107	PROP-00097	CMC MODULOS	\N	2408.665446	3122.1826020000003	3909.57	39.1	\N	0.29622924893322866	144.26	4052.37	approved	\N	luciana	Cliente Ativo	0	FOB	\N	30/45/60	0	2025-12-11 13:39:15.244743+00	2025-12-11 17:27:48.739588+00	2025-12-15 03:00:00+00	0.01	0
111	PROP-00101	CJC SERRALHERIA	\N	5473.968	7117.0512	9564	143.46	\N	0.30016309923623957	478.2	10043.999999999998	approved	\N	aline	Prospeccao	0	CIF	\N	28/35/42	0	2025-12-11 17:51:55.781202+00	2025-12-11 18:08:04.832861+00	2025-12-12 03:00:00+00	0.015000000000000001	0
112	PROP-00102	vista alegre 	\N	12459.068016000001	16882.782044	22551.7	338.28000000000003	\N	0.3550597863595449	0	22551.7	draft	\N	aldo	\N	0	FOB	\N	28/35/42	0	2025-12-11 20:16:26.664131+00	2025-12-11 20:16:26.664131+00	2025-12-15 03:00:00+00	0.014999999999999998	1.6
114	PROP-00104	PSG	\N	5974.3266	8624.6985	11590	239.39999999999998	\N	0.4436268850785627	579.5	12175.6	draft	\N	laura	Prospeccao	0	FOB	\N	À vista	0	2025-12-12 13:21:58.482862+00	2025-12-12 13:21:58.482862+00	2025-12-17 03:00:00+00	0.02065573770491803	0.83
115	PROP-00105	W-CONEX IND COM	\N	6548.599859999999	8736.388518000002	10939.630000000001	159.48	\N	0.33408495018353485	500.82	11442.29	draft	\N	aldo	\N	0	FOB	\N	28/35/42	0	2025-12-12 14:20:22.255628+00	2025-12-12 14:20:22.255628+00	2025-12-15 03:00:00+00	0.014578043315907391	3
113	PROP-00103	REAL ESTRTUTURA	\N	94137.79246200001	129502.47225696	162161.87360000002	3243.02	\N	0.375669312717689	0	162161.87360000002	draft	\N	luciana	Orpen Whatsapp	0	FOB	\N	28/35/42	0	2025-12-11 20:51:06.560976+00	2025-12-12 17:14:05.882108+00	2025-12-15 03:00:00+00	0.019998677010229116	0
118	PROP-00108	MACJEE	\N	1856.745	2414.9664	3024	45.36	\N	0.3006451612903226	0	3024	sent	ESTAREMOS EM FERIAS COLETIVAS DE 19/12 Á 04/01. RETORNAMOS DIA 05/01/2026\n\nFRETE CIF ATÉ 60KM	luciana	Cliente Ativo	0	FOB	\N	30/45	0	2025-12-12 17:20:00.7205+00	2025-12-12 17:20:28.322926+00	2025-12-15 03:00:00+00	0.015	0
116	PROP-00106	PROJINOX	\N	286.681428	388.691889	522.3299999999999	7.83	\N	0.35583212247707935	26.119999999999997	548.3100000000001	approved	\N	aline	Cliente Ativo	0	CIF	\N	21	0	2025-12-12 16:33:01.383974+00	2025-12-12 17:23:31.284003+00	2025-12-15 03:00:00+00	0.015000000000000001	0
119	PROP-00109	MUNDO NOVO MAQUINAS	\N	23357.788212	31371.579492	39283.22	589.24	\N	0.3430886181202267	1964.1699999999998	41240.59	sent	\N	aline	Cliente Ativo	0	FOB	\N	30/45/60	0	2025-12-12 17:20:40.328541+00	2025-12-12 17:35:32.133928+00	2025-12-15 03:00:00+00	0.015	0
117	PROP-00107	MCM USNINAGEM	\N	1064.118528	1457.566605	1958.7	29.38	\N	0.36974083868221114	70.15	2029.41	draft	\N	aldo	\N	0	CIF	\N	28/35/42	0	2025-12-12 17:10:44.504802+00	2025-12-12 17:39:38.794015+00	2025-12-15 03:00:00+00	0.015000000000000001	0
134	PROP-00124	ÉPURA ESTRUTURAS MISTAS	\N	68637.2742	91075.619454	107912.70000000001	1618.69	\N	0.32691195149471713	3507.16	111435.51	draft	\N	aldo	\N	0	FOB	\N	28/35/42/49	0	2025-12-15 18:59:46.408071+00	2025-12-15 18:59:46.408071+00	2025-12-17 03:00:00+00	0.014999999999999998	1.23
126	PROP-00116	AMZ	\N	49240.40549999999	80592.18552	95491.2	3634.6800000000003	\N	0.6367084044423642	0	95491.20000000001	approved	50% A VISTA E SALDO EM 3X	adriana	Orpen Whatsapp	0	FOB	\N	À vista	0	2025-12-15 00:03:12.15141+00	2025-12-15 00:17:56.263863+00	2025-12-16 03:00:00+00	0.03806298381421534	0
121	PROP-00111	BLOJAF LTDA - CNPJ. 00.860.887/0001-98	\N	6261.36084	9443.620968	12690.48	380.71	\N	0.5082377791853951	0	12690.48	sent	Estaremos em férias coletivas de 19/12 à 04/01.\nDia 18/12 é o último dia de faturamento e entrega, retornamos as atividades dia 05/01/2026\n	luciana	Primeiro Google	1208.8799999999999	CIF	\N	30	0	2025-12-12 17:58:02.711793+00	2025-12-12 17:58:16.523963+00	2025-12-15 03:00:00+00	0.03	0
122	PROP-00112	VALTER FRANÇA	\N	973.485414	1375.025487	1847.78	46.19	\N	0.41247672253258844	92.39	1940.8500000000001	sent	Estaremos em férias coletivas de 19/12 à 04/01.\nDia 18/12 é o último dia de faturamento e entrega, retornamos as atividades dia 05/01/2026\n	luciana	Orpen Whatsapp	0	CIF	\N	À vista	0	2025-12-12 18:04:04.054119+00	2025-12-12 18:04:12.024952+00	2025-12-15 03:00:00+00	0.025	0
125	PROP-00115	GUARUCOOP	\N	69336.96759	90837.9549	113746.5	1610.23	\N	0.3100941396390248	3696.76	117513.9	sent	lembrando que nosso estoque é rotativo e os reajustes são conforme usina, proposta válida por 02  dias	adriana	Prospeccao	0	CIF	\N	28/35/42	0	2025-12-13 15:56:30.57466+00	2025-12-15 00:22:56.671321+00	2025-12-18 03:00:00+00	0.01415631469979296	0
127	PROP-00117	SER-COP	\N	2253.96864	3016.79136	3777.6	56.66	\N	0.33843537414965985	188.88	3964.7999999999997	sent	\N	aline	Cliente Ativo	0	CIF	\N	À vista	0	2025-12-15 12:11:33.956382+00	2025-12-15 12:11:41.525894+00	2025-12-15 03:00:00+00	0.015	0
85	PROP-00075	TRIARCO	\N	31641.351654000002	41454.28782	51908.7	721.99	\N	0.310130119386334	2595.44	54526.920000000006	approved	\N	adriana	Cliente Ativo	0	CIF	\N	28	0	2025-12-09 17:41:42.100146+00	2025-12-16 18:51:54.252955+00	\N	0.013908795635413718	0
128	PROP-00118	PROJINOX	\N	151.781916	198.707652	248.82	3.73	\N	0.3091655266757866	0	248.82	sent	\N	aline	Cliente Ativo	0	CIF	\N	À vista	0	2025-12-15 13:09:33.706596+00	2025-12-15 13:09:48.788203+00	2025-12-16 03:00:00+00	0.015	0
124	PROP-00114	METALFIT	\N	1783.191762	4415.518206	5933.64	284.61	\N	1.47618809154189	192.84	6126.52	draft	\N	aldo	\N	0	CIF	\N	28/35/42	0	2025-12-12 19:27:19.706491+00	2025-12-15 13:14:06.568023+00	2025-12-17 03:00:00+00	0.04796499282059579	116.67
135	PROP-00125	SERRALHERIA CARVALHO	\N	1948.1847	2598.48468	3253.8	48.81	\N	0.3337979094076655	105.75	3359.2000000000003	sent	\N	aline	Cliente Ativo	0	CIF	\N	28/35/42	0	2025-12-15 19:48:44.494417+00	2025-12-15 19:48:50.354206+00	2025-12-16 03:00:00+00	0.015	0
130	PROP-00120	LRS	\N	42590.5359	56704.150420000005	67187	1007.81	\N	0.3313791250041539	0	67187	draft	\N	laura	Cliente Ativo	0	FOB	\N	À vista	0	2025-12-15 15:55:35.675967+00	2025-12-15 15:55:35.675967+00	2025-12-18 03:00:00+00	0.015000000000000001	2.71
132	PROP-00122	FW DO BRASIL	\N	387.7394	531.3231000000001	714	10.71	\N	0.37030980086109405	35.7	749.7	approved	\N	aline	Cliente Ativo	0	CIF	\N	21	0	2025-12-15 18:08:20.47153+00	2025-12-15 20:02:11.760729+00	2025-12-17 03:00:00+00	0.015	0
131	PROP-00121	LEDLUZ INDUSTRIA	\N	248381.45685400002	325684.22350600007	385893.19999999995	5788.4	\N	0.3112259974279764	12541.529999999999	398442.44	sent	\N	aline	Indicacao	68554.09	CIF	20000	30/45/60/75	0.609738	2025-12-15 17:14:17.360569+00	2025-12-15 17:15:18.934944+00	2026-01-06 03:00:00+00	0.015000000000000003	0
153	PROP-00143	COMANDO DA AERONAUTICA	\N	7985.778528	10807.73694	14523.6	217.85	\N	0.35337298700503106	472.02	14993.16	draft	\N	adriana	Orpen Whatsapp	2369.64	FOB	\N	7	0	2025-12-18 14:34:47.72826+00	2025-12-18 14:34:47.72826+00	2025-12-19 03:00:00+00	0.015	0
138	PROP-00128	Serralheria Carvalho	\N	917.35182	1214.22966	1631.7	24.48	\N	0.32362484439176237	81.59	1713.6000000000001	sent	\N	aline	Cliente Ativo	0	CIF	\N	28/35	0	2025-12-16 17:02:38.801285+00	2025-12-16 17:03:24.90099+00	2025-12-17 03:00:00+00	0.015	0
136	PROP-00126	CARLOS DE LARA	\N	2043.2543999999998	2870.9308	3858	145.45	\N	0.4050775077249315	159.69	4018	sent	Estaremos em férias coletivas de 19/12 á 04/01.\nRetornamos nossas atividades em 05/01/2026.	luciana	Orpen Whatsapp	0	CIF	\N	28/35/42	0	2025-12-16 12:19:44.353192+00	2025-12-16 16:37:50.964417+00	2025-12-16 03:00:00+00	0.037700881285640225	0
141	PROP-00131	CB LEANDRO	\N	2366.39712	3571.9199999999996	4800	144	\N	0.5094338857207532	156	4956	sent	\N	adriana	Orpen Whatsapp	0	FOB	\N	7	0	2025-12-17 12:59:52.342456+00	2025-12-17 14:20:49.016512+00	2025-12-19 03:00:00+00	0.03	0
139	PROP-00129	VITORIA INDL	\N	1585492.3689900003	2067956.28199	2589498.22	38608.369999999995	\N	0.3042991076061386	122259.61	2711654.7799999993	draft	\N	aldo	\N	0	FOB	\N	28/35/42	0	2025-12-16 17:05:35.973805+00	2025-12-16 18:11:46.639752+00	2026-01-05 03:00:00+00	0.014909594550715697	0
137	PROP-00127	RODRIGO	\N	1771.20768	2302.569984	3056.5600000000004	63.870000000000005	\N	0.3	127.09	3183.6800000000003	approved	\N	aline	Cliente Ativo	0	CIF	\N	À vista	0	2025-12-16 16:59:16.297505+00	2025-12-17 11:52:44.968645+00	2025-12-17 03:00:00+00	0.020894862198026536	0
140	PROP-00130	METALMOTIVA	\N	9551.256	12777.6	16000	240	\N	0.3377926421404682	520	16520	approved	\N	adriana	Prospeccao	0	FOB	\N	28/35	0	2025-12-16 20:20:53.082792+00	2025-12-17 13:09:36.099841+00	2025-12-19 03:00:00+00	0.015	0
133	PROP-00123	ENGEVALE	\N	44928.058	59904.075	80500	1207.5	\N	0.3333332813984526	0	80500	sent	\N	adriana	Cliente Ativo	0	CIF	\N	30/45	0	2025-12-15 18:26:52.89796+00	2025-12-17 13:13:19.346414+00	2025-12-18 03:00:00+00	0.015	0
142	PROP-00132	CONSTRUTORA BASSI	\N	4772.68869	6222.991959999999	8362.55	125.42999999999999	\N	0.3038755226249628	404.21000000000004	8768.199999999999	sent	\N	aline	Orpen Whatsapp	336.6	CIF	\N	28/35/42	0	2025-12-17 14:59:17.606903+00	2025-12-17 18:44:52.779681+00	2025-12-19 03:00:00+00	0.015000000000000003	0
143	PROP-00133	FRANCISCO FREIRE	\N	9439.53186	12609.686957	14940.83	224.12	\N	0.33583816909750863	747.04	15685.57	sent	\N	aline	Orpen Whatsapp	0	FOB	\N	28/35/42	0	2025-12-17 18:10:59.320469+00	2025-12-17 18:42:34.535235+00	2025-12-19 03:00:00+00	0.015	0
120	PROP-00110	PISOMETAL	\N	932.56515	1287.56565	1730.25	25.95	\N	0.380670991190267	0	1730.25	lost	tinha urgência, pegou na regiao\n	luciana	Cliente Ativo	0	CIF	\N	30	0	2025-12-12 17:50:52.000126+00	2025-12-18 18:49:06.228919+00	2025-12-15 03:00:00+00	0.015	0
129	PROP-00119	AGROPECUARIA BARRA BONITA	\N	23967.994066	31494.860099999998	40101.3	601.52	\N	0.3140382133470776	2005.07	42125.11	lost	GOLPEEEE	adriana	Orpen Whatsapp	0	FOB	\N	7	0	2025-12-15 13:19:31.103429+00	2025-12-18 11:47:01.853355+00	2025-12-19 03:00:00+00	0.015	0
144	PROP-00134	NATREB	\N	177.583956	296.44032	371.2	14.85	\N	0.6692967466047439	18.56	389.6	lost	não conseguiu coletar	luciana	Orpen Whatsapp	0	FOB	\N	À vista	0	2025-12-17 19:39:45.082388+00	2025-12-18 18:45:53.998925+00	2025-12-17 03:00:00+00	0.04	5.26
147	PROP-00137	vista alegre	\N	1479.4065	1937.0043	2425.5	36.38	\N	0.30931174089068825	0	2425.5	draft	\N	aldo	\N	0	FOB	\N	28/35/42	0	2025-12-18 12:24:09.305213+00	2025-12-18 12:25:55.793136+00	2026-01-07 03:00:00+00	0.015	3.16
145	PROP-00135	MADEMETAL	\N	2564.512236	3384.684687	4548.39	68.23	\N	0.31981615820997783	227.42	4773.93	approved	30% A VISTA + 70% 28/35	aline	Cliente Ativo	0	CIF	\N	À vista	0	2025-12-17 19:56:21.955208+00	2025-12-18 13:11:30.642466+00	2025-12-18 03:00:00+00	0.015000000000000001	0
149	PROP-00139	Pilar Industria	\N	3310.2260399999996	4351.730278	5830.14	87.46000000000001	\N	0.31463236208485645	0	5830.14	sent	\N	aline	Cliente Ativo	0	CIF	\N	28/35/42	0	2025-12-18 13:23:02.106603+00	2025-12-18 13:43:09.934933+00	2025-12-18 03:00:00+00	0.015	0
151	PROP-00141	SEUMA	\N	12442.188	17145.942	21470	322.05	\N	0.3780487804878049	0	21470	draft	\N	aldo	\N	0	FOB	\N	28/35/42	0	2025-12-18 13:41:11.223007+00	2025-12-18 13:53:46.765917+00	2026-01-05 03:00:00+00	0.015000000000000001	0
154	PROP-00144	HKM IND E COM	\N	1718179.1154	2233632.8500200002	2796935.7	139846.79	\N	0.3000000000000001	139846.79	2937250.2	draft	\N	aldo	\N	0	FOB	\N	28/35/42	0	2025-12-18 14:45:26.558868+00	2025-12-18 18:04:34.496821+00	\N	0.049999999999999996	0
152	PROP-00142	PIRAMIDE	\N	821.863218	1076.986053	1447.27	21.71	\N	0.3104200667610361	47.040000000000006	1494.0700000000002	sent	\N	luciana	Cliente Ativo	0	CIF	\N	28	0	2025-12-18 14:28:48.520454+00	2025-12-18 18:44:26.606595+00	2025-12-18 03:00:00+00	0.015	0
146	PROP-00136	CALLEVE	\N	1091.230998	1498.7181	2014	36.370000000000005	\N	0.37341965426828905	93.98	2107.98	approved	COTAÇÃO VALIDA PARA FECHAMENTO HOJE E ENTREGA EM JANEIRO,	luciana	Cliente Ativo	0	CIF	\N	À vista	0	2025-12-18 12:09:03.798445+00	2025-12-18 18:45:16.477797+00	2025-12-18 03:00:00+00	0.018053624627606752	0
123	PROP-00113	MAGIC TOYS	\N	6936.63643	8884.370305	11938.949999999999	137.26	\N	0.28078938469029724	388.01	12332.400000000001	lost	naõ tinha 2 itens e nos outros teve preço melhor com 22margem	luciana	Cliente Ativo	0	CIF	\N	28/35/42	0	2025-12-12 18:34:54.577124+00	2025-12-18 18:48:07.355212+00	2025-12-15 03:00:00+00	0.011497681956956015	0
148	PROP-00138	RJ EX COMERCIO E SERVICOS	\N	10935.43308	14602.001699999999	18284.5	274.27	\N	0.33529249305231895	594.25	18887.7	sent	\N	aline	Orpen Whatsapp	0	FOB	\N	28/35/42	0	2025-12-18 13:08:15.232341+00	2025-12-18 13:08:23.983071+00	2026-01-05 03:00:00+00	0.015	0.05
150	PROP-00140	FACTOOLS	\N	6027.973644000001	7867.2068580000005	10277.93	139.87	\N	0.3051163330534295	203.39000000000001	10481.9	sent	COTAÇÃO VALIDA PARA FECHAMENTO HOJE COM ENTREGA PARA JANEIRO APOS RECESSO EM 05/01/2026.	luciana	Email Vendas	0	FOB	\N	28/35/42	0	2025-12-18 13:31:15.049407+00	2025-12-18 18:44:54.854285+00	2025-12-18 03:00:00+00	0.013608192505689374	0
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: crm_user
--

COPY public.users (id, email, username, full_name, hashed_password, role, is_active, created_at, updated_at) FROM stdin;
1	admin@crmditual.com	admin	Administrador do Sistema	$2b$12$IqXDl3pfYjDrW13RyI.RRO6Y8KBwyJci2huGxJjlzOVVw.fOBrkBS	admin	t	2025-10-24 19:25:00.783923+00	2025-10-24 19:25:00.783923+00
2	aline@ditualsp.com.br	aline	Aline Andrade	$2a$12$XFqPNU9t85EKIGV9k3g.K./a23mA52lyyfEBLtua6OJdV1ymx31nS	vendas	t	2025-11-24 02:34:18.309137+00	2025-11-24 02:34:18.309137+00
3	adriana@ditualsp.com.br	adriana	Adriana Andrade	$2a$12$rOFiOWyg6cTsKolNfcV6ZOuPHDAmBJsfAmLd7IGpTrYk7QUKDciW.	vendas	t	2025-11-24 02:34:18.309137+00	2025-11-24 02:34:18.309137+00
4	aldo@ditualsp.com.br	aldo	Aldo Medeiros	$2a$12$EZb5jI.L8HORkNzjnqkSK.kXx2YtpHyMxmf1yWRoM6V9eSmMu/PuC	vendas	t	2025-11-24 02:34:18.309137+00	2025-11-24 02:34:18.309137+00
5	laura@ditualsp.com.br	laura	Laura Garcia	$2a$12$ESNEjyuKxSe86dKxL2Jl7uno.4b/YSpa8.wkHVe9JdGv6QqWXT/5W	vendas	t	2025-11-24 02:34:18.309137+00	2025-11-24 02:34:18.309137+00
6	luciana@ditualsp.com.br	luciana	Luciana Lucas	$2a$12$1CZQ1H7ivAuZi4Q0cOCi8.UE0jtzk.4ZFkvINgJsJeWdH3LcvpxZm	vendas	t	2025-11-24 02:34:18.309137+00	2025-11-24 02:34:18.309137+00
7	cecilia@ditualsp.com.br	cecilia	Cecilia Alves	$2b$12$PMnNvslC5ekv8AoRFI5vaOfc4wOYwGBgXu9/w8cvNbEcMGV87a9ZW	admin	t	2025-11-24 02:35:06.257743+00	2025-11-24 02:35:06.257743+00
\.


--
-- Name: budget_items_id_seq; Type: SEQUENCE SET; Schema: public; Owner: crm_user
--

SELECT pg_catalog.setval('public.budget_items_id_seq', 1603, true);


--
-- Name: budgets_id_seq; Type: SEQUENCE SET; Schema: public; Owner: crm_user
--

SELECT pg_catalog.setval('public.budgets_id_seq', 154, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: crm_user
--

SELECT pg_catalog.setval('public.users_id_seq', 7, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: crm_user
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: alembic_version_user alembic_version_user_pkey; Type: CONSTRAINT; Schema: public; Owner: crm_user
--

ALTER TABLE ONLY public.alembic_version_user
    ADD CONSTRAINT alembic_version_user_pkey PRIMARY KEY (version_num);


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
-- Name: budget_items fk_budget_items_budget_id; Type: FK CONSTRAINT; Schema: public; Owner: crm_user
--

ALTER TABLE ONLY public.budget_items
    ADD CONSTRAINT fk_budget_items_budget_id FOREIGN KEY (budget_id) REFERENCES public.budgets(id);


--
-- PostgreSQL database dump complete
--

\unrestrict uR4e1xqCCwGeLEFXQosCRL63n4ea2OIN7POrmNfI5Y6d50f6OoULUI8hocByHR8

