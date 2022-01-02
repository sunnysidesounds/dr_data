--
-- PostgreSQL database dump
--

-- Dumped from database version 13.5
-- Dumped by pg_dump version 13.5

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
-- Name: digital_asset_status; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.digital_asset_status AS ENUM (
    'pending_review',
    'published',
    'retracted',
    'qc_failed',
    'qc_passed'
);


ALTER TYPE public.digital_asset_status OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: __EFMigrationsHistory; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."__EFMigrationsHistory" (
                                                migration_id character varying(150) NOT NULL,
                                                product_version character varying(32) NOT NULL
);


ALTER TABLE public."__EFMigrationsHistory" OWNER TO postgres;

--
-- Name: controlled_vocabularies; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.controlled_vocabularies (
                                                id uuid NOT NULL,
                                                name text NOT NULL,
                                                discriminator text NOT NULL,
                                                created_by text NOT NULL,
                                                created_at timestamp with time zone NOT NULL,
                                                updated_by text,
                                                updated_at timestamp with time zone
);


ALTER TABLE public.controlled_vocabularies OWNER TO postgres;

--
-- Name: digital_asset_accounts; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.digital_asset_accounts (
                                               id uuid NOT NULL,
                                               name text NOT NULL,
                                               description text,
                                               created_by text NOT NULL,
                                               created_at timestamp with time zone NOT NULL,
                                               updated_by text,
                                               updated_at timestamp with time zone
);


ALTER TABLE public.digital_asset_accounts OWNER TO postgres;

--
-- Name: digital_asset_instances; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.digital_asset_instances (
                                                id uuid NOT NULL,
                                                external_id text,
                                                external_collection text,
                                                external_status text,
                                                download_url text NOT NULL,
                                                details_url text,
                                                digital_asset_id uuid,
                                                storage_id uuid NOT NULL,
                                                created_by text NOT NULL,
                                                created_at timestamp with time zone NOT NULL,
                                                updated_by text,
                                                updated_at timestamp with time zone
);


ALTER TABLE public.digital_asset_instances OWNER TO postgres;

--
-- Name: digital_assets; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.digital_assets (
                                       id uuid NOT NULL,
                                       name text NOT NULL,
                                       type_id uuid NOT NULL,
                                       doi text,
                                       hash text NOT NULL,
                                       status public.digital_asset_status NOT NULL,
                                       end_of_life timestamp with time zone NOT NULL,
                                       use_id uuid,
                                       submission_id uuid,
                                       created_by text NOT NULL,
                                       created_at timestamp with time zone NOT NULL,
                                       updated_by text,
                                       updated_at timestamp with time zone
);


ALTER TABLE public.digital_assets OWNER TO postgres;

--
-- Name: storage_storage_use; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.storage_storage_use (
                                            storages_id uuid NOT NULL,
                                            uses_id uuid NOT NULL
);


ALTER TABLE public.storage_storage_use OWNER TO postgres;

--
-- Name: storages; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.storages (
                                 id uuid NOT NULL,
                                 name text NOT NULL,
                                 storage_provider_id uuid NOT NULL,
                                 account_id uuid NOT NULL,
                                 discriminator text NOT NULL,
                                 path text,
                                 bucket text,
                                 region text,
                                 has_versioning boolean,
                                 created_by text NOT NULL,
                                 created_at timestamp with time zone NOT NULL,
                                 updated_by text,
                                 updated_at timestamp with time zone
);


ALTER TABLE public.storages OWNER TO postgres;

--
-- Name: submissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.submissions (
                                    id uuid NOT NULL,
                                    name text NOT NULL,
                                    description text,
                                    type_id uuid NOT NULL,
                                    account_id uuid NOT NULL,
                                    created_by text NOT NULL,
                                    created_at timestamp with time zone NOT NULL,
                                    updated_by text,
                                    updated_at timestamp with time zone
);


ALTER TABLE public.submissions OWNER TO postgres;

--
-- Name: tag; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tag (
                            id uuid NOT NULL,
                            value text NOT NULL,
                            digital_asset_id uuid NOT NULL,
                            created_by text NOT NULL,
                            created_at timestamp with time zone NOT NULL,
                            updated_by text,
                            updated_at timestamp with time zone
);


ALTER TABLE public.tag OWNER TO postgres;

--
-- Name: __EFMigrationsHistory pk___ef_migrations_history; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."__EFMigrationsHistory"
    ADD CONSTRAINT pk___ef_migrations_history PRIMARY KEY (migration_id);


--
-- Name: controlled_vocabularies pk_controlled_vocabularies; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.controlled_vocabularies
    ADD CONSTRAINT pk_controlled_vocabularies PRIMARY KEY (id);


--
-- Name: digital_asset_accounts pk_digital_asset_accounts; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.digital_asset_accounts
    ADD CONSTRAINT pk_digital_asset_accounts PRIMARY KEY (id);


--
-- Name: digital_asset_instances pk_digital_asset_instances; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.digital_asset_instances
    ADD CONSTRAINT pk_digital_asset_instances PRIMARY KEY (id);


--
-- Name: digital_assets pk_digital_assets; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.digital_assets
    ADD CONSTRAINT pk_digital_assets PRIMARY KEY (id);


--
-- Name: storage_storage_use pk_storage_storage_use; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.storage_storage_use
    ADD CONSTRAINT pk_storage_storage_use PRIMARY KEY (storages_id, uses_id);


--
-- Name: storages pk_storages; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.storages
    ADD CONSTRAINT pk_storages PRIMARY KEY (id);


--
-- Name: submissions pk_submissions; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.submissions
    ADD CONSTRAINT pk_submissions PRIMARY KEY (id);


--
-- Name: tag pk_tag; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tag
    ADD CONSTRAINT pk_tag PRIMARY KEY (id);


--
-- Name: ix_controlled_vocabularies_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_controlled_vocabularies_name ON public.controlled_vocabularies USING btree (name);


--
-- Name: ix_digital_asset_accounts_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_digital_asset_accounts_name ON public.digital_asset_accounts USING btree (name);


--
-- Name: ix_digital_asset_instances_digital_asset_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_digital_asset_instances_digital_asset_id ON public.digital_asset_instances USING btree (digital_asset_id);


--
-- Name: ix_digital_asset_instances_storage_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_digital_asset_instances_storage_id ON public.digital_asset_instances USING btree (storage_id);


--
-- Name: ix_digital_assets_hash; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_digital_assets_hash ON public.digital_assets USING btree (hash);


--
-- Name: ix_digital_assets_submission_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_digital_assets_submission_id ON public.digital_assets USING btree (submission_id);


--
-- Name: ix_digital_assets_type_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_digital_assets_type_id ON public.digital_assets USING btree (type_id);


--
-- Name: ix_digital_assets_use_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_digital_assets_use_id ON public.digital_assets USING btree (use_id);


--
-- Name: ix_storage_storage_use_uses_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_storage_storage_use_uses_id ON public.storage_storage_use USING btree (uses_id);


--
-- Name: ix_storages_account_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_storages_account_id ON public.storages USING btree (account_id);


--
-- Name: ix_storages_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_storages_name ON public.storages USING btree (name);


--
-- Name: ix_storages_storage_provider_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_storages_storage_provider_id ON public.storages USING btree (storage_provider_id);


--
-- Name: ix_submissions_account_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_submissions_account_id ON public.submissions USING btree (account_id);


--
-- Name: ix_submissions_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_submissions_name ON public.submissions USING btree (name);


--
-- Name: ix_submissions_type_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_submissions_type_id ON public.submissions USING btree (type_id);


--
-- Name: ix_tag_digital_asset_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_tag_digital_asset_id ON public.tag USING btree (digital_asset_id);


--
-- Name: digital_asset_instances fk_digital_asset_instances_digital_assets_digital_asset_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.digital_asset_instances
    ADD CONSTRAINT fk_digital_asset_instances_digital_assets_digital_asset_id FOREIGN KEY (digital_asset_id) REFERENCES public.digital_assets(id) ON DELETE CASCADE;


--
-- Name: digital_asset_instances fk_digital_asset_instances_storages_storage_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.digital_asset_instances
    ADD CONSTRAINT fk_digital_asset_instances_storages_storage_id FOREIGN KEY (storage_id) REFERENCES public.storages(id) ON DELETE CASCADE;


--
-- Name: digital_assets fk_digital_assets_controlled_vocabularies_type_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.digital_assets
    ADD CONSTRAINT fk_digital_assets_controlled_vocabularies_type_id FOREIGN KEY (type_id) REFERENCES public.controlled_vocabularies(id) ON DELETE CASCADE;


--
-- Name: digital_assets fk_digital_assets_controlled_vocabularies_use_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.digital_assets
    ADD CONSTRAINT fk_digital_assets_controlled_vocabularies_use_id FOREIGN KEY (use_id) REFERENCES public.controlled_vocabularies(id);


--
-- Name: digital_assets fk_digital_assets_submissions_submission_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.digital_assets
    ADD CONSTRAINT fk_digital_assets_submissions_submission_id FOREIGN KEY (submission_id) REFERENCES public.submissions(id);


--
-- Name: storage_storage_use fk_storage_storage_use_controlled_vocabularies_uses_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.storage_storage_use
    ADD CONSTRAINT fk_storage_storage_use_controlled_vocabularies_uses_id FOREIGN KEY (uses_id) REFERENCES public.controlled_vocabularies(id) ON DELETE CASCADE;


--
-- Name: storage_storage_use fk_storage_storage_use_storages_storages_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.storage_storage_use
    ADD CONSTRAINT fk_storage_storage_use_storages_storages_id FOREIGN KEY (storages_id) REFERENCES public.storages(id) ON DELETE CASCADE;


--
-- Name: storages fk_storages_controlled_vocabularies_storage_provider_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.storages
    ADD CONSTRAINT fk_storages_controlled_vocabularies_storage_provider_id FOREIGN KEY (storage_provider_id) REFERENCES public.controlled_vocabularies(id) ON DELETE CASCADE;


--
-- Name: storages fk_storages_digital_asset_accounts_account_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.storages
    ADD CONSTRAINT fk_storages_digital_asset_accounts_account_id FOREIGN KEY (account_id) REFERENCES public.digital_asset_accounts(id) ON DELETE RESTRICT;


--
-- Name: submissions fk_submissions_controlled_vocabularies_type_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.submissions
    ADD CONSTRAINT fk_submissions_controlled_vocabularies_type_id FOREIGN KEY (type_id) REFERENCES public.controlled_vocabularies(id) ON DELETE CASCADE;


--
-- Name: submissions fk_submissions_digital_asset_accounts_account_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.submissions
    ADD CONSTRAINT fk_submissions_digital_asset_accounts_account_id FOREIGN KEY (account_id) REFERENCES public.digital_asset_accounts(id) ON DELETE RESTRICT;


--
-- Name: tag fk_tag_digital_assets_digital_asset_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tag
    ADD CONSTRAINT fk_tag_digital_assets_digital_asset_id FOREIGN KEY (digital_asset_id) REFERENCES public.digital_assets(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

