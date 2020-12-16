CREATE TABLE public.env_sequence_elements
(
    pri_seq integer[] NOT NULL,
    seq_id integer NOT NULL,
    CONSTRAINT env_sequence_elements_pkey PRIMARY KEY (seq_id)
);
INSERT INTO public.env_sequence_elements(
	pri_seq, seq_id)
	VALUES ('{2267, 4654, 3637, 7706, 7701, 5019, 8253, 2060, 6254, 8635}', 1);
	INSERT INTO public.env_sequence_elements(
	pri_seq, seq_id)
	VALUES ('{5018, 8252, 2059, 6253, 8634, 2266, 4653, 3636, 7705, 7700}', 1);