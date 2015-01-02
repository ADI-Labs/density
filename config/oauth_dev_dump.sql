\connect density;

--
-- Name: oauth_data; Type: TABLE; Schema: public; Owner: adicu; Tablespace: 
--

DROP TABLE oauth_data CASCADE;
CREATE TABLE oauth_data (
  uni text NOT NULL,
  code text NOT NULL
);

ALTER TABLE public.oauth_data OWNER to adicu;

COPY oauth_data (uni, code) FROM stdin;
abc1234	abcdefghjijklmnopqrstuvwxyz
\.
