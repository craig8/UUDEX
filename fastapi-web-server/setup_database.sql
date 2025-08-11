-- Database setup script generated from schema information
-- Generated on: 2025-06-03 14:10:31
-- This script creates all tables, constraints, and indexes

-- Create tables
CREATE TABLE IF NOT EXISTS auth_group (
    group_id integer NOT NULL DEFAULT nextval('auth_group_group_id_seq'::regclass),
    group_uuid character NOT NULL,
    group_name character varying(40) NOT NULL,
    description character varying(255),
    create_datetime timestamp without time zone NOT NULL,
    PRIMARY KEY (group_id)
);

CREATE TABLE IF NOT EXISTS auth_role (
    role_id integer NOT NULL DEFAULT nextval('auth_role_role_id_seq'::regclass),
    role_uuid character NOT NULL,
    role_name character varying(40) NOT NULL,
    description character varying(255),
    create_datetime timestamp without time zone NOT NULL,
    PRIMARY KEY (role_id)
);

CREATE TABLE IF NOT EXISTS contact (
    contact_id integer NOT NULL DEFAULT nextval('contact_contact_id_seq'::regclass),
    contact_name character varying(30) NOT NULL,
    contact_number character varying(15) NOT NULL,
    participant_id integer NOT NULL,
    PRIMARY KEY (contact_id)
);

CREATE TABLE IF NOT EXISTS dataset (
    dataset_id integer NOT NULL DEFAULT nextval('dataset_dataset_id_seq'::regclass),
    dataset_uuid character NOT NULL,
    dataset_name character varying(255) NOT NULL,
    description character varying(255) NOT NULL,
    properties character varying(1024),
    payload bytea NOT NULL,
    payload_size integer NOT NULL,
    payload_md5_hash character NOT NULL,
    payload_compression_algorithm character varying(15) NOT NULL,
    version_number integer NOT NULL,
    create_datetime timestamp without time zone NOT NULL,
    owner_participant_id integer NOT NULL,
    subject_id integer NOT NULL,
    PRIMARY KEY (dataset_id)
);

CREATE TABLE IF NOT EXISTS dataset_definition (
    dataset_definition_id integer NOT NULL DEFAULT nextval('dataset_definition_dataset_definition_id_seq'::regclass),
    dataset_definition_uuid character NOT NULL,
    dataset_definition_name character varying(100) NOT NULL,
    description character varying(255),
    schema character varying(32768),
    create_datetime timestamp without time zone NOT NULL,
    PRIMARY KEY (dataset_definition_id)
);

CREATE TABLE IF NOT EXISTS endpoint (
    endpoint_id integer NOT NULL DEFAULT nextval('endpoint_endpoint_id_seq'::regclass),
    endpoint_uuid character NOT NULL,
    endpoint_user_name character varying(30) NOT NULL,
    certificate_dn character varying(255) NOT NULL,
    description character varying(255),
    active_sw character NOT NULL,
    create_datetime timestamp without time zone NOT NULL,
    participant_id integer NOT NULL,
    PRIMARY KEY (endpoint_id)
);

CREATE TABLE IF NOT EXISTS grant_scope (
    grant_scope_id integer NOT NULL,
    grant_scope_name character varying(40),
    PRIMARY KEY (grant_scope_id)
);

CREATE TABLE IF NOT EXISTS participant (
    participant_id integer NOT NULL DEFAULT nextval('participant_participant_id_seq'::regclass),
    participant_uuid character NOT NULL,
    participant_short_name character varying(25) NOT NULL,
    participant_long_name character varying(50) NOT NULL,
    description character varying(255),
    root_org_sw character NOT NULL,
    active_sw character NOT NULL,
    create_datetime timestamp without time zone NOT NULL,
    PRIMARY KEY (participant_id)
);

CREATE TABLE IF NOT EXISTS privilege_allowed (
    privilege_allowed_id integer NOT NULL,
    privilege_allowed_name character varying(40),
    PRIMARY KEY (privilege_allowed_id)
);

CREATE TABLE IF NOT EXISTS subject (
    subject_id integer NOT NULL DEFAULT nextval('subject_subject_id_seq'::regclass),
    subject_uuid character NOT NULL,
    subject_name character varying(300) NOT NULL,
    dataset_instance_key character varying(100) NOT NULL,
    description character varying(300),
    subscription_type character NOT NULL,
    fulfillment_types_available character varying(15) NOT NULL,
    full_queue_behavior character varying(20),
    max_queue_size_kb integer,
    max_message_count integer,
    priority integer,
    backing_exchange_name character varying(300),
    create_datetime timestamp without time zone NOT NULL,
    owner_participant_id integer NOT NULL,
    dataset_definition_id integer NOT NULL,
    PRIMARY KEY (subject_id)
);

CREATE TABLE IF NOT EXISTS subject_policy (
    subject_policy_id integer NOT NULL DEFAULT nextval('subject_policy_subject_policy_id_seq'::regclass),
    subject_policy_uuid character NOT NULL,
    subject_policy_type character varying(25) NOT NULL,
    subject_policy_type_sort integer NOT NULL,
    action character varying(10) NOT NULL,
    full_queue_behavior character varying(20),
    max_queue_size_kb integer,
    max_message_count integer,
    max_priority integer,
    target_participant_id integer,
    dataset_definition_id integer,
    PRIMARY KEY (subject_policy_id)
);

CREATE TABLE IF NOT EXISTS subject_policy_acl_constraint (
    subject_policy_acl_constraint_id integer NOT NULL DEFAULT nextval('subject_policy_acl_constraint_subject_policy_acl_constraint_seq'::regclass),
    subject_policy_id integer NOT NULL,
    privilege_allowed_id integer NOT NULL,
    grant_scope_id integer NOT NULL,
    PRIMARY KEY (subject_policy_acl_constraint_id)
);

CREATE TABLE IF NOT EXISTS subject_policy_grant_allowed (
    sp_grant_allowed_id integer NOT NULL DEFAULT nextval('subject_policy_grant_allowed_sp_grant_allowed_id_seq'::regclass),
    object_uuid character NOT NULL,
    object_type character NOT NULL,
    create_datetime timestamp without time zone NOT NULL,
    subject_policy_acl_constraint_id integer NOT NULL,
    PRIMARY KEY (sp_grant_allowed_id)
);

CREATE TABLE IF NOT EXISTS subscription (
    subscription_id integer NOT NULL DEFAULT nextval('subscription_subscription_id_seq'::regclass),
    subscription_uuid character NOT NULL,
    subscription_name character varying(30) NOT NULL,
    subscription_state character varying(10) NOT NULL,
    create_datetime timestamp without time zone NOT NULL,
    owner_endpoint_id integer NOT NULL,
    PRIMARY KEY (subscription_id)
);

CREATE TABLE IF NOT EXISTS subscription_subject (
    subscription_subject_id integer NOT NULL DEFAULT nextval('subscription_subject_subscription_subject_id_seq'::regclass),
    preferred_fulfillment_type character varying(15) NOT NULL,
    backing_queue_name character varying(255),
    subject_id integer NOT NULL,
    subscription_id integer NOT NULL,
    PRIMARY KEY (subscription_subject_id)
);

-- Add foreign key constraints
ALTER TABLE contact ADD CONSTRAINT Refparticipant48 FOREIGN KEY (participant_id) REFERENCES participant (participant_id);
ALTER TABLE dataset ADD CONSTRAINT Refsubject45 FOREIGN KEY (subject_id) REFERENCES subject (subject_id);
ALTER TABLE dataset ADD CONSTRAINT Refparticipant52 FOREIGN KEY (owner_participant_id) REFERENCES participant (participant_id);
ALTER TABLE endpoint ADD CONSTRAINT Refparticipant29 FOREIGN KEY (participant_id) REFERENCES participant (participant_id);
ALTER TABLE subject ADD CONSTRAINT Refdataset_definition97 FOREIGN KEY (dataset_definition_id) REFERENCES dataset_definition (dataset_definition_id);
ALTER TABLE subject ADD CONSTRAINT Refparticipant60 FOREIGN KEY (owner_participant_id) REFERENCES participant (participant_id);
ALTER TABLE subject_policy ADD CONSTRAINT Refdataset_definition96 FOREIGN KEY (dataset_definition_id) REFERENCES dataset_definition (dataset_definition_id);
ALTER TABLE subject_policy ADD CONSTRAINT Refparticipant69 FOREIGN KEY (target_participant_id) REFERENCES participant (participant_id);
ALTER TABLE subject_policy_acl_constraint ADD CONSTRAINT Refsubject_policy71 FOREIGN KEY (subject_policy_id) REFERENCES subject_policy (subject_policy_id);
ALTER TABLE subject_policy_acl_constraint ADD CONSTRAINT Refprivilege_allowed82 FOREIGN KEY (privilege_allowed_id) REFERENCES privilege_allowed (privilege_allowed_id);
ALTER TABLE subject_policy_acl_constraint ADD CONSTRAINT Refgrant_scope83 FOREIGN KEY (grant_scope_id) REFERENCES grant_scope (grant_scope_id);
ALTER TABLE subject_policy_grant_allowed ADD CONSTRAINT Refsubject_policy_acl_constraint81 FOREIGN KEY (subject_policy_acl_constraint_id) REFERENCES subject_policy_acl_constraint (subject_policy_acl_constraint_id);
ALTER TABLE subscription ADD CONSTRAINT Refendpoint64 FOREIGN KEY (owner_endpoint_id) REFERENCES endpoint (endpoint_id);
ALTER TABLE subscription_subject ADD CONSTRAINT Refsubject58 FOREIGN KEY (subject_id) REFERENCES subject (subject_id);
ALTER TABLE subscription_subject ADD CONSTRAINT Refsubscription27 FOREIGN KEY (subscription_id) REFERENCES subscription (subscription_id);

-- Create indexes
CREATE UNIQUE INDEX pg_aggregate_fnoid_index ON pg_catalog.pg_aggregate USING btree (aggfnoid);
CREATE UNIQUE INDEX pg_am_name_index ON pg_catalog.pg_am USING btree (amname);
CREATE UNIQUE INDEX pg_am_oid_index ON pg_catalog.pg_am USING btree (oid);
CREATE UNIQUE INDEX pg_amop_fam_strat_index ON pg_catalog.pg_amop USING btree (amopfamily, amoplefttype, amoprighttype, amopstrategy);
CREATE UNIQUE INDEX pg_amop_oid_index ON pg_catalog.pg_amop USING btree (oid);
CREATE UNIQUE INDEX pg_amop_opr_fam_index ON pg_catalog.pg_amop USING btree (amopopr, amoppurpose, amopfamily);
CREATE UNIQUE INDEX pg_amproc_fam_proc_index ON pg_catalog.pg_amproc USING btree (amprocfamily, amproclefttype, amprocrighttype, amprocnum);
CREATE UNIQUE INDEX pg_amproc_oid_index ON pg_catalog.pg_amproc USING btree (oid);
CREATE UNIQUE INDEX pg_attrdef_adrelid_adnum_index ON pg_catalog.pg_attrdef USING btree (adrelid, adnum);
CREATE UNIQUE INDEX pg_attrdef_oid_index ON pg_catalog.pg_attrdef USING btree (oid);
CREATE UNIQUE INDEX pg_attribute_relid_attnam_index ON pg_catalog.pg_attribute USING btree (attrelid, attname);
CREATE UNIQUE INDEX pg_attribute_relid_attnum_index ON pg_catalog.pg_attribute USING btree (attrelid, attnum);
CREATE UNIQUE INDEX pg_auth_members_member_role_index ON pg_catalog.pg_auth_members USING btree (member, roleid);
CREATE UNIQUE INDEX pg_auth_members_role_member_index ON pg_catalog.pg_auth_members USING btree (roleid, member);
CREATE UNIQUE INDEX pg_authid_oid_index ON pg_catalog.pg_authid USING btree (oid);
CREATE UNIQUE INDEX pg_authid_rolname_index ON pg_catalog.pg_authid USING btree (rolname);
CREATE UNIQUE INDEX pg_cast_oid_index ON pg_catalog.pg_cast USING btree (oid);
CREATE UNIQUE INDEX pg_cast_source_target_index ON pg_catalog.pg_cast USING btree (castsource, casttarget);
CREATE UNIQUE INDEX pg_class_oid_index ON pg_catalog.pg_class USING btree (oid);
CREATE UNIQUE INDEX pg_class_relname_nsp_index ON pg_catalog.pg_class USING btree (relname, relnamespace);
CREATE INDEX pg_class_tblspc_relfilenode_index ON pg_catalog.pg_class USING btree (reltablespace, relfilenode);
CREATE UNIQUE INDEX pg_collation_name_enc_nsp_index ON pg_catalog.pg_collation USING btree (collname, collencoding, collnamespace);
CREATE UNIQUE INDEX pg_collation_oid_index ON pg_catalog.pg_collation USING btree (oid);
CREATE INDEX pg_constraint_conname_nsp_index ON pg_catalog.pg_constraint USING btree (conname, connamespace);
CREATE INDEX pg_constraint_conparentid_index ON pg_catalog.pg_constraint USING btree (conparentid);
CREATE UNIQUE INDEX pg_constraint_conrelid_contypid_conname_index ON pg_catalog.pg_constraint USING btree (conrelid, contypid, conname);
CREATE INDEX pg_constraint_contypid_index ON pg_catalog.pg_constraint USING btree (contypid);
CREATE UNIQUE INDEX pg_constraint_oid_index ON pg_catalog.pg_constraint USING btree (oid);
CREATE UNIQUE INDEX pg_conversion_default_index ON pg_catalog.pg_conversion USING btree (connamespace, conforencoding, contoencoding, oid);
CREATE UNIQUE INDEX pg_conversion_name_nsp_index ON pg_catalog.pg_conversion USING btree (conname, connamespace);
CREATE UNIQUE INDEX pg_conversion_oid_index ON pg_catalog.pg_conversion USING btree (oid);
CREATE UNIQUE INDEX pg_database_datname_index ON pg_catalog.pg_database USING btree (datname);
CREATE UNIQUE INDEX pg_database_oid_index ON pg_catalog.pg_database USING btree (oid);
CREATE UNIQUE INDEX pg_db_role_setting_databaseid_rol_index ON pg_catalog.pg_db_role_setting USING btree (setdatabase, setrole);
CREATE UNIQUE INDEX pg_default_acl_oid_index ON pg_catalog.pg_default_acl USING btree (oid);
CREATE UNIQUE INDEX pg_default_acl_role_nsp_obj_index ON pg_catalog.pg_default_acl USING btree (defaclrole, defaclnamespace, defaclobjtype);
CREATE INDEX pg_depend_depender_index ON pg_catalog.pg_depend USING btree (classid, objid, objsubid);
CREATE INDEX pg_depend_reference_index ON pg_catalog.pg_depend USING btree (refclassid, refobjid, refobjsubid);
CREATE UNIQUE INDEX pg_description_o_c_o_index ON pg_catalog.pg_description USING btree (objoid, classoid, objsubid);
CREATE UNIQUE INDEX pg_enum_oid_index ON pg_catalog.pg_enum USING btree (oid);
CREATE UNIQUE INDEX pg_enum_typid_label_index ON pg_catalog.pg_enum USING btree (enumtypid, enumlabel);
CREATE UNIQUE INDEX pg_enum_typid_sortorder_index ON pg_catalog.pg_enum USING btree (enumtypid, enumsortorder);
CREATE UNIQUE INDEX pg_event_trigger_evtname_index ON pg_catalog.pg_event_trigger USING btree (evtname);
CREATE UNIQUE INDEX pg_event_trigger_oid_index ON pg_catalog.pg_event_trigger USING btree (oid);
CREATE UNIQUE INDEX pg_extension_name_index ON pg_catalog.pg_extension USING btree (extname);
CREATE UNIQUE INDEX pg_extension_oid_index ON pg_catalog.pg_extension USING btree (oid);
CREATE UNIQUE INDEX pg_foreign_data_wrapper_name_index ON pg_catalog.pg_foreign_data_wrapper USING btree (fdwname);
CREATE UNIQUE INDEX pg_foreign_data_wrapper_oid_index ON pg_catalog.pg_foreign_data_wrapper USING btree (oid);
CREATE UNIQUE INDEX pg_foreign_server_name_index ON pg_catalog.pg_foreign_server USING btree (srvname);
CREATE UNIQUE INDEX pg_foreign_server_oid_index ON pg_catalog.pg_foreign_server USING btree (oid);
CREATE UNIQUE INDEX pg_foreign_table_relid_index ON pg_catalog.pg_foreign_table USING btree (ftrelid);
CREATE UNIQUE INDEX pg_index_indexrelid_index ON pg_catalog.pg_index USING btree (indexrelid);
CREATE INDEX pg_index_indrelid_index ON pg_catalog.pg_index USING btree (indrelid);
CREATE INDEX pg_inherits_parent_index ON pg_catalog.pg_inherits USING btree (inhparent);
CREATE UNIQUE INDEX pg_inherits_relid_seqno_index ON pg_catalog.pg_inherits USING btree (inhrelid, inhseqno);
CREATE UNIQUE INDEX pg_init_privs_o_c_o_index ON pg_catalog.pg_init_privs USING btree (objoid, classoid, objsubid);
CREATE UNIQUE INDEX pg_language_name_index ON pg_catalog.pg_language USING btree (lanname);
CREATE UNIQUE INDEX pg_language_oid_index ON pg_catalog.pg_language USING btree (oid);
CREATE UNIQUE INDEX pg_largeobject_loid_pn_index ON pg_catalog.pg_largeobject USING btree (loid, pageno);
CREATE UNIQUE INDEX pg_largeobject_metadata_oid_index ON pg_catalog.pg_largeobject_metadata USING btree (oid);
CREATE UNIQUE INDEX pg_namespace_nspname_index ON pg_catalog.pg_namespace USING btree (nspname);
CREATE UNIQUE INDEX pg_namespace_oid_index ON pg_catalog.pg_namespace USING btree (oid);
CREATE UNIQUE INDEX pg_opclass_am_name_nsp_index ON pg_catalog.pg_opclass USING btree (opcmethod, opcname, opcnamespace);
CREATE UNIQUE INDEX pg_opclass_oid_index ON pg_catalog.pg_opclass USING btree (oid);
CREATE UNIQUE INDEX pg_operator_oid_index ON pg_catalog.pg_operator USING btree (oid);
CREATE UNIQUE INDEX pg_operator_oprname_l_r_n_index ON pg_catalog.pg_operator USING btree (oprname, oprleft, oprright, oprnamespace);
CREATE UNIQUE INDEX pg_opfamily_am_name_nsp_index ON pg_catalog.pg_opfamily USING btree (opfmethod, opfname, opfnamespace);
CREATE UNIQUE INDEX pg_opfamily_oid_index ON pg_catalog.pg_opfamily USING btree (oid);
CREATE UNIQUE INDEX pg_partitioned_table_partrelid_index ON pg_catalog.pg_partitioned_table USING btree (partrelid);
CREATE UNIQUE INDEX pg_policy_oid_index ON pg_catalog.pg_policy USING btree (oid);
CREATE UNIQUE INDEX pg_policy_polrelid_polname_index ON pg_catalog.pg_policy USING btree (polrelid, polname);
CREATE UNIQUE INDEX pg_proc_oid_index ON pg_catalog.pg_proc USING btree (oid);
CREATE UNIQUE INDEX pg_proc_proname_args_nsp_index ON pg_catalog.pg_proc USING btree (proname, proargtypes, pronamespace);
CREATE UNIQUE INDEX pg_publication_oid_index ON pg_catalog.pg_publication USING btree (oid);
CREATE UNIQUE INDEX pg_publication_pubname_index ON pg_catalog.pg_publication USING btree (pubname);
CREATE UNIQUE INDEX pg_publication_rel_oid_index ON pg_catalog.pg_publication_rel USING btree (oid);
CREATE UNIQUE INDEX pg_publication_rel_prrelid_prpubid_index ON pg_catalog.pg_publication_rel USING btree (prrelid, prpubid);
CREATE UNIQUE INDEX pg_range_rngmultitypid_index ON pg_catalog.pg_range USING btree (rngmultitypid);
CREATE UNIQUE INDEX pg_range_rngtypid_index ON pg_catalog.pg_range USING btree (rngtypid);
CREATE UNIQUE INDEX pg_replication_origin_roiident_index ON pg_catalog.pg_replication_origin USING btree (roident);
CREATE UNIQUE INDEX pg_replication_origin_roname_index ON pg_catalog.pg_replication_origin USING btree (roname);
CREATE UNIQUE INDEX pg_rewrite_oid_index ON pg_catalog.pg_rewrite USING btree (oid);
CREATE UNIQUE INDEX pg_rewrite_rel_rulename_index ON pg_catalog.pg_rewrite USING btree (ev_class, rulename);
CREATE UNIQUE INDEX pg_seclabel_object_index ON pg_catalog.pg_seclabel USING btree (objoid, classoid, objsubid, provider);
CREATE UNIQUE INDEX pg_sequence_seqrelid_index ON pg_catalog.pg_sequence USING btree (seqrelid);
CREATE INDEX pg_shdepend_depender_index ON pg_catalog.pg_shdepend USING btree (dbid, classid, objid, objsubid);
CREATE INDEX pg_shdepend_reference_index ON pg_catalog.pg_shdepend USING btree (refclassid, refobjid);
CREATE UNIQUE INDEX pg_shdescription_o_c_index ON pg_catalog.pg_shdescription USING btree (objoid, classoid);
CREATE UNIQUE INDEX pg_shseclabel_object_index ON pg_catalog.pg_shseclabel USING btree (objoid, classoid, provider);
CREATE UNIQUE INDEX pg_statistic_relid_att_inh_index ON pg_catalog.pg_statistic USING btree (starelid, staattnum, stainherit);
CREATE UNIQUE INDEX pg_statistic_ext_name_index ON pg_catalog.pg_statistic_ext USING btree (stxname, stxnamespace);
CREATE UNIQUE INDEX pg_statistic_ext_oid_index ON pg_catalog.pg_statistic_ext USING btree (oid);
CREATE INDEX pg_statistic_ext_relid_index ON pg_catalog.pg_statistic_ext USING btree (stxrelid);
CREATE UNIQUE INDEX pg_statistic_ext_data_stxoid_index ON pg_catalog.pg_statistic_ext_data USING btree (stxoid);
CREATE UNIQUE INDEX pg_subscription_oid_index ON pg_catalog.pg_subscription USING btree (oid);
CREATE UNIQUE INDEX pg_subscription_subname_index ON pg_catalog.pg_subscription USING btree (subdbid, subname);
CREATE UNIQUE INDEX pg_subscription_rel_srrelid_srsubid_index ON pg_catalog.pg_subscription_rel USING btree (srrelid, srsubid);
CREATE UNIQUE INDEX pg_tablespace_oid_index ON pg_catalog.pg_tablespace USING btree (oid);
CREATE UNIQUE INDEX pg_tablespace_spcname_index ON pg_catalog.pg_tablespace USING btree (spcname);
CREATE UNIQUE INDEX pg_transform_oid_index ON pg_catalog.pg_transform USING btree (oid);
CREATE UNIQUE INDEX pg_transform_type_lang_index ON pg_catalog.pg_transform USING btree (trftype, trflang);
CREATE UNIQUE INDEX pg_trigger_oid_index ON pg_catalog.pg_trigger USING btree (oid);
CREATE INDEX pg_trigger_tgconstraint_index ON pg_catalog.pg_trigger USING btree (tgconstraint);
CREATE UNIQUE INDEX pg_trigger_tgrelid_tgname_index ON pg_catalog.pg_trigger USING btree (tgrelid, tgname);
CREATE UNIQUE INDEX pg_ts_config_cfgname_index ON pg_catalog.pg_ts_config USING btree (cfgname, cfgnamespace);
CREATE UNIQUE INDEX pg_ts_config_oid_index ON pg_catalog.pg_ts_config USING btree (oid);
CREATE UNIQUE INDEX pg_ts_config_map_index ON pg_catalog.pg_ts_config_map USING btree (mapcfg, maptokentype, mapseqno);
CREATE UNIQUE INDEX pg_ts_dict_dictname_index ON pg_catalog.pg_ts_dict USING btree (dictname, dictnamespace);
CREATE UNIQUE INDEX pg_ts_dict_oid_index ON pg_catalog.pg_ts_dict USING btree (oid);
CREATE UNIQUE INDEX pg_ts_parser_oid_index ON pg_catalog.pg_ts_parser USING btree (oid);
CREATE UNIQUE INDEX pg_ts_parser_prsname_index ON pg_catalog.pg_ts_parser USING btree (prsname, prsnamespace);
CREATE UNIQUE INDEX pg_ts_template_oid_index ON pg_catalog.pg_ts_template USING btree (oid);
CREATE UNIQUE INDEX pg_ts_template_tmplname_index ON pg_catalog.pg_ts_template USING btree (tmplname, tmplnamespace);
CREATE UNIQUE INDEX pg_type_oid_index ON pg_catalog.pg_type USING btree (oid);
CREATE UNIQUE INDEX pg_type_typname_nsp_index ON pg_catalog.pg_type USING btree (typname, typnamespace);
CREATE UNIQUE INDEX pg_user_mapping_oid_index ON pg_catalog.pg_user_mapping USING btree (oid);
CREATE UNIQUE INDEX pg_user_mapping_user_server_index ON pg_catalog.pg_user_mapping USING btree (umuser, umserver);
CREATE UNIQUE INDEX pk_auth_group ON public.auth_group USING btree (group_id);
CREATE UNIQUE INDEX uk_auth_group_1 ON public.auth_group USING btree (group_uuid);
CREATE UNIQUE INDEX uk_auth_group_2 ON public.auth_group USING btree (group_name);
CREATE UNIQUE INDEX pk_auth_role ON public.auth_role USING btree (role_id);
CREATE UNIQUE INDEX uk_auth_role2 ON public.auth_role USING btree (role_name);
CREATE UNIQUE INDEX uk_auth_role_1 ON public.auth_role USING btree (role_uuid);
CREATE INDEX "Ref1848" ON public.contact USING btree (participant_id);
CREATE UNIQUE INDEX pk_contact ON public.contact USING btree (contact_id);
CREATE INDEX "Ref1852" ON public.dataset USING btree (owner_participant_id);
CREATE INDEX "Ref345" ON public.dataset USING btree (subject_id);
CREATE UNIQUE INDEX pk_dataset ON public.dataset USING btree (dataset_id);
CREATE UNIQUE INDEX uk_dataset_1 ON public.dataset USING btree (dataset_uuid);
CREATE UNIQUE INDEX pk_dataset_definition ON public.dataset_definition USING btree (dataset_definition_id);
CREATE UNIQUE INDEX uk_dataset_definition_1 ON public.dataset_definition USING btree (dataset_definition_uuid);
CREATE UNIQUE INDEX uk_dataset_definition_2 ON public.dataset_definition USING btree (dataset_definition_name);
CREATE INDEX "Ref1829" ON public.endpoint USING btree (participant_id);
CREATE UNIQUE INDEX pk_endpoint ON public.endpoint USING btree (endpoint_id);
CREATE UNIQUE INDEX uk_endpoint_1 ON public.endpoint USING btree (certificate_dn);
CREATE UNIQUE INDEX uk_endpoint_2 ON public.endpoint USING btree (endpoint_uuid);
CREATE UNIQUE INDEX pk_permission_target_type ON public.grant_scope USING btree (grant_scope_id);
CREATE UNIQUE INDEX pk_participant ON public.participant USING btree (participant_id);
CREATE UNIQUE INDEX uk_participant_1 ON public.participant USING btree (participant_uuid);
CREATE UNIQUE INDEX pk_privilege_constraint ON public.privilege_allowed USING btree (privilege_allowed_id);
CREATE INDEX "Ref1860" ON public.subject USING btree (owner_participant_id);
CREATE INDEX "Ref4397" ON public.subject USING btree (dataset_definition_id);
CREATE UNIQUE INDEX pk_subject ON public.subject USING btree (subject_id);
CREATE UNIQUE INDEX uk_subject_1 ON public.subject USING btree (subject_name);
CREATE UNIQUE INDEX uk_subject_2 ON public.subject USING btree (subject_uuid);
CREATE INDEX "Ref1869" ON public.subject_policy USING btree (target_participant_id);
CREATE INDEX "Ref4396" ON public.subject_policy USING btree (dataset_definition_id);
CREATE UNIQUE INDEX pk_subject_creation_policy ON public.subject_policy USING btree (subject_policy_id);
CREATE UNIQUE INDEX uk_subject_creation_policy_1 ON public.subject_policy USING btree (subject_policy_uuid);
CREATE INDEX "Ref2882" ON public.subject_policy_acl_constraint USING btree (privilege_allowed_id);
CREATE INDEX "Ref3183" ON public.subject_policy_acl_constraint USING btree (grant_scope_id);
CREATE INDEX "Ref3271" ON public.subject_policy_acl_constraint USING btree (subject_policy_id);
CREATE UNIQUE INDEX pk_scp_constraint ON public.subject_policy_acl_constraint USING btree (subject_policy_acl_constraint_id);
CREATE UNIQUE INDEX scp_constraint_uk_1 ON public.subject_policy_acl_constraint USING btree (subject_policy_id, privilege_allowed_id);
CREATE INDEX "Ref3381" ON public.subject_policy_grant_allowed USING btree (subject_policy_acl_constraint_id);
CREATE UNIQUE INDEX pk_scp_permission_target ON public.subject_policy_grant_allowed USING btree (sp_grant_allowed_id);
CREATE INDEX "Ref164" ON public.subscription USING btree (owner_endpoint_id);
CREATE UNIQUE INDEX pk_subscription ON public.subscription USING btree (subscription_id);
CREATE UNIQUE INDEX uk_subscription ON public.subscription USING btree (subscription_name, owner_endpoint_id);
CREATE UNIQUE INDEX uk_subscription_2 ON public.subscription USING btree (subscription_uuid);
CREATE INDEX "Ref358" ON public.subscription_subject USING btree (subject_id);
CREATE INDEX "Ref527" ON public.subscription_subject USING btree (subscription_id);
CREATE UNIQUE INDEX pk_subscription_subject ON public.subscription_subject USING btree (subscription_subject_id);
CREATE UNIQUE INDEX uk_subscription_subject_1 ON public.subscription_subject USING btree (subscription_id, subject_id);

-- End of setup script
