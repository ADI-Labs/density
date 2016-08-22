\connect density;

--
-- Name: oauth_data; Type: TABLE; Schema: public; Owner: adicu; Tablespace: 
--

DROP TABLE oauth_data CASCADE;
CREATE TABLE oauth_data (
  uni text NOT NULL,
  code varchar(64) NOT NULL
);

CREATE UNIQUE INDEX on oauth_data (code);

ALTER TABLE public.oauth_data OWNER to adi;

COPY oauth_data (uni, code) FROM stdin;
abc1234	l7QGxn6doncC9Z9iPk7hykbMilRg2uV0JoIxYljtEai4o7rjVP1J9KDTudwYDNKl
\.
