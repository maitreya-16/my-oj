-- Adminer 6.0.1 PostgreSQL 15.19 dump

\connect "postgres";

DROP TABLE IF EXISTS "public"."events", "public"."leaderboards", "public"."problems", "public"."problemsamples", "public"."submissions", "public"."user";

CREATE TABLE "public"."events" (
    "id" serial NOT NULL,
    "name" character varying(255) NOT NULL,
    "start_time" timestamptz,
    "end_time" timestamptz,
    "is_active" boolean DEFAULT false NOT NULL,
    "created_at" timestamptz NOT NULL,
    "updated_at" timestamptz NOT NULL,
    CONSTRAINT "events_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);

CREATE UNIQUE INDEX events_name_key5 ON public.events USING btree (name);

CREATE UNIQUE INDEX events_name_key2 ON public.events USING btree (name);

CREATE UNIQUE INDEX events_name_key ON public.events USING btree (name);

CREATE UNIQUE INDEX events_name_key1 ON public.events USING btree (name);

CREATE UNIQUE INDEX events_name_key3 ON public.events USING btree (name);

CREATE UNIQUE INDEX events_name_key4 ON public.events USING btree (name);

CREATE UNIQUE INDEX events_name_key22 ON public.events USING btree (name);

CREATE UNIQUE INDEX events_name_key6 ON public.events USING btree (name);

CREATE UNIQUE INDEX events_name_key7 ON public.events USING btree (name);

CREATE UNIQUE INDEX events_name_key8 ON public.events USING btree (name);

CREATE UNIQUE INDEX events_name_key9 ON public.events USING btree (name);

CREATE UNIQUE INDEX events_name_key11 ON public.events USING btree (name);

CREATE UNIQUE INDEX events_name_key13 ON public.events USING btree (name);

CREATE UNIQUE INDEX events_name_key14 ON public.events USING btree (name);

CREATE UNIQUE INDEX events_name_key15 ON public.events USING btree (name);

CREATE UNIQUE INDEX events_name_key16 ON public.events USING btree (name);

CREATE UNIQUE INDEX events_name_key18 ON public.events USING btree (name);

CREATE UNIQUE INDEX events_name_key19 ON public.events USING btree (name);

CREATE UNIQUE INDEX events_name_key20 ON public.events USING btree (name);

CREATE UNIQUE INDEX events_name_key23 ON public.events USING btree (name);

CREATE UNIQUE INDEX events_name_key25 ON public.events USING btree (name);

CREATE UNIQUE INDEX events_name_key26 ON public.events USING btree (name);

CREATE UNIQUE INDEX events_name_key29 ON public.events USING btree (name);

CREATE UNIQUE INDEX events_name_key28 ON public.events USING btree (name);

CREATE UNIQUE INDEX events_name_key34 ON public.events USING btree (name);

CREATE UNIQUE INDEX events_name_key35 ON public.events USING btree (name);

CREATE UNIQUE INDEX events_name_key37 ON public.events USING btree (name);

CREATE UNIQUE INDEX events_name_key38 ON public.events USING btree (name);

CREATE UNIQUE INDEX events_name_key39 ON public.events USING btree (name);

CREATE UNIQUE INDEX events_name_key36 ON public.events USING btree (name);

CREATE UNIQUE INDEX events_name_key33 ON public.events USING btree (name);

CREATE UNIQUE INDEX events_name_key32 ON public.events USING btree (name);

CREATE UNIQUE INDEX events_name_key30 ON public.events USING btree (name);

CREATE UNIQUE INDEX events_name_key31 ON public.events USING btree (name);

CREATE UNIQUE INDEX events_name_key27 ON public.events USING btree (name);

CREATE UNIQUE INDEX events_name_key24 ON public.events USING btree (name);

CREATE UNIQUE INDEX events_name_key21 ON public.events USING btree (name);

CREATE UNIQUE INDEX events_name_key17 ON public.events USING btree (name);

CREATE UNIQUE INDEX events_name_key12 ON public.events USING btree (name);

CREATE UNIQUE INDEX events_name_key10 ON public.events USING btree (name);

DO $$ BEGIN PERFORM setval('"public"."events_id_seq"', 3); END $$;

INSERT INTO "events" ("id", "name", "start_time", "end_time", "is_active", "created_at", "updated_at") VALUES
(1,	'Programming Contest 2026',	'2026-09-01 10:00:00+00',	'2026-09-10 13:00:00+00',	'1',	'2026-09-03 09:28:15.287397+00',	'2026-09-03 09:28:15.287397+00');

CREATE TABLE "public"."leaderboards" (
    "id" serial NOT NULL,
    "teamname" character varying(255) DEFAULT 'TEAM' NOT NULL,
    "event_id" integer NOT NULL,
    "team_id" character varying(255),
    "problem_1" integer DEFAULT '0',
    "problem_2" integer DEFAULT '0',
    "problem_3" integer DEFAULT '0',
    "problem_4" integer DEFAULT '0',
    "total_submissions" integer DEFAULT '0',
    "total_score" integer DEFAULT '0',
    "last_submission_time" timestamptz,
    "isjunior" boolean DEFAULT false NOT NULL,
    "created_at" timestamptz NOT NULL,
    "updated_at" timestamptz NOT NULL,
    CONSTRAINT "leaderboards_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);

CREATE UNIQUE INDEX leaderboards_team_id_key38 ON public.leaderboards USING btree (team_id);

CREATE UNIQUE INDEX leaderboards_team_id_key36 ON public.leaderboards USING btree (team_id);

CREATE UNIQUE INDEX leaderboards_team_id_key33 ON public.leaderboards USING btree (team_id);

CREATE UNIQUE INDEX leaderboards_team_id_key32 ON public.leaderboards USING btree (team_id);

CREATE UNIQUE INDEX leaderboards_team_id_key18 ON public.leaderboards USING btree (team_id);

CREATE UNIQUE INDEX leaderboards_team_id_key19 ON public.leaderboards USING btree (team_id);

CREATE UNIQUE INDEX leaderboards_team_id_key22 ON public.leaderboards USING btree (team_id);

CREATE UNIQUE INDEX leaderboards_team_id_key23 ON public.leaderboards USING btree (team_id);

CREATE UNIQUE INDEX leaderboards_team_id_key25 ON public.leaderboards USING btree (team_id);

CREATE UNIQUE INDEX leaderboards_team_id_key28 ON public.leaderboards USING btree (team_id);

CREATE UNIQUE INDEX leaderboards_team_id_key26 ON public.leaderboards USING btree (team_id);

CREATE UNIQUE INDEX leaderboards_team_id_key29 ON public.leaderboards USING btree (team_id);

CREATE UNIQUE INDEX leaderboards_team_id_key30 ON public.leaderboards USING btree (team_id);

CREATE UNIQUE INDEX leaderboards_team_id_key27 ON public.leaderboards USING btree (team_id);

CREATE UNIQUE INDEX leaderboards_team_id_key24 ON public.leaderboards USING btree (team_id);

CREATE UNIQUE INDEX leaderboards_team_id_key21 ON public.leaderboards USING btree (team_id);

CREATE UNIQUE INDEX leaderboards_team_id_key17 ON public.leaderboards USING btree (team_id);

CREATE UNIQUE INDEX leaderboards_team_id_key16 ON public.leaderboards USING btree (team_id);

CREATE UNIQUE INDEX leaderboards_team_id_key12 ON public.leaderboards USING btree (team_id);

CREATE UNIQUE INDEX leaderboards_team_id_key9 ON public.leaderboards USING btree (team_id);

CREATE UNIQUE INDEX leaderboards_team_id_key ON public.leaderboards USING btree (team_id);

CREATE UNIQUE INDEX leaderboards_team_id_key1 ON public.leaderboards USING btree (team_id);

CREATE UNIQUE INDEX leaderboards_team_id_key2 ON public.leaderboards USING btree (team_id);

CREATE UNIQUE INDEX leaderboards_team_id_key14 ON public.leaderboards USING btree (team_id);

CREATE UNIQUE INDEX leaderboards_team_id_key20 ON public.leaderboards USING btree (team_id);

CREATE UNIQUE INDEX leaderboards_team_id_key15 ON public.leaderboards USING btree (team_id);

CREATE UNIQUE INDEX leaderboards_team_id_key31 ON public.leaderboards USING btree (team_id);

CREATE UNIQUE INDEX leaderboards_team_id_key3 ON public.leaderboards USING btree (team_id);

CREATE UNIQUE INDEX leaderboards_team_id_key4 ON public.leaderboards USING btree (team_id);

CREATE UNIQUE INDEX leaderboards_team_id_key5 ON public.leaderboards USING btree (team_id);

CREATE UNIQUE INDEX leaderboards_team_id_key39 ON public.leaderboards USING btree (team_id);

CREATE UNIQUE INDEX leaderboards_team_id_key6 ON public.leaderboards USING btree (team_id);

CREATE UNIQUE INDEX leaderboards_team_id_key7 ON public.leaderboards USING btree (team_id);

CREATE UNIQUE INDEX leaderboards_team_id_key8 ON public.leaderboards USING btree (team_id);

CREATE UNIQUE INDEX leaderboards_team_id_key10 ON public.leaderboards USING btree (team_id);

CREATE UNIQUE INDEX leaderboards_team_id_key11 ON public.leaderboards USING btree (team_id);

CREATE UNIQUE INDEX leaderboards_team_id_key13 ON public.leaderboards USING btree (team_id);

CREATE UNIQUE INDEX leaderboards_team_id_key34 ON public.leaderboards USING btree (team_id);

CREATE UNIQUE INDEX leaderboards_team_id_key35 ON public.leaderboards USING btree (team_id);

CREATE UNIQUE INDEX leaderboards_team_id_key37 ON public.leaderboards USING btree (team_id);

CREATE UNIQUE INDEX leaderboards_event_id_team_id ON public.leaderboards USING btree (event_id, team_id);

DO $$ BEGIN PERFORM setval('"public"."leaderboards_id_seq"', 33); END $$;

INSERT INTO "leaderboards" ("id", "teamname", "event_id", "team_id", "problem_1", "problem_2", "problem_3", "problem_4", "total_submissions", "total_score", "last_submission_time", "isjunior", "created_at", "updated_at") VALUES
(1,	'maitreya',	1,	'1',	200,	0,	0,	0,	19,	200,	'2026-09-03 10:21:25.871+00',	false,	'2026-09-03 10:20:58.763+00',	'2026-09-03 19:21:56.813+00');

CREATE TABLE "public"."problems" (
    "id" serial NOT NULL,
    "title" character varying(255) NOT NULL,
    "description" text NOT NULL,
    "score" integer DEFAULT '50' NOT NULL,
    "input_format" text,
    "output_format" text,
    "constraints" text,
    "isjunior" boolean DEFAULT false NOT NULL,
    "time_limit" integer DEFAULT '2',
    "memory_limit" integer DEFAULT '256',
    "event_id" integer NOT NULL,
    CONSTRAINT "problems_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);

DO $$ BEGIN PERFORM setval('"public"."problems_id_seq"', 3); END $$;

INSERT INTO "problems" ("id", "title", "description", "score", "input_format", "output_format", "constraints", "isjunior", "time_limit", "memory_limit", "event_id") VALUES
(1,	'The Mysterious Number',	'In the ancient city of Numera, a mysterious machine transforms a given number into another number. Nobody knows exactly what happens inside the machine, but a few examples have been recorded. Your task is to study the examples, uncover the hidden pattern, and determine the mysterious output for any given number.',	50,	'A single integer N.',	'A single integer representing the mysterious output produced by the machine.',	'1 <= N <= 10^5',	false,	1,	128,	1);

CREATE TABLE "public"."problemsamples" (
    "id" serial NOT NULL,
    "problem_id" integer NOT NULL,
    "input" text NOT NULL,
    "output" text NOT NULL,
    "explanation" text,
    CONSTRAINT "problemsamples_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);

DO $$ BEGIN PERFORM setval('"public"."problemsamples_id_seq"', 8); END $$;

INSERT INTO "problemsamples" ("id", "problem_id", "input", "output", "explanation") VALUES
(5,	1,	'2',	'4',	NULL),
(6,	1,	'3',	'9',	NULL),
(7,	1,	'5',	'25',	NULL),
(8,	1,	'10',	'100',	NULL);

CREATE TABLE "public"."submissions" (
    "id" serial NOT NULL,
    "team_id" character varying(255),
    "teamname" character varying(255) DEFAULT 'TEAM' NOT NULL,
    "problem_id" integer NOT NULL,
    "event_id" integer NOT NULL,
    "code" text NOT NULL,
    "language" character varying(255) NOT NULL,
    "failed_test_case" text,
    "result" text DEFAULT 'Pending' NOT NULL,
    "score" integer DEFAULT '0',
    "submitted_at" timestamptz,
    "verdict" character varying(255),
    "created_at" timestamptz,
    CONSTRAINT "submissions_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);

DO $$ BEGIN PERFORM setval('"public"."submissions_id_seq"', 206); END $$;

INSERT INTO "submissions" ("id", "team_id", "teamname", "problem_id", "event_id", "code", "language", "failed_test_case", "result", "score", "submitted_at", "verdict", "created_at") VALUES
(1,	'1',	'maitreya',	1,	1,	'cHJpbnQoIkhlbGxvLCBXb3JsZCEiKQ==',	'python',	'1',	'wrong',	0,	'2026-09-03 10:20:57.945+00',	'Failed Testcase',	'2026-09-03 10:20:57.945+00'),
(2,	'1',	'maitreya',	1,	1,	'biA9IGludChpbnB1dCgpKQ0KcHJpbnQobipuKQ==',	'python',	'0',	'accepted',	200,	'2026-09-03 10:21:25.066+00',	NULL,	'2026-09-03 10:21:25.066+00'),
(34,	'1',	'maitreya',	1,	1,	'd2hpbGUgVHJ1ZToNCiAgcHJpbnQoImhlbGxvIHRpbWUiKQ==',	'python',	'1',	'timeout',	0,	'2026-09-03 10:38:09.114+00',	'Time Limit Exceeded',	'2026-09-03 10:38:09.114+00'),
(35,	'1',	'maitreya',	1,	1,	'I2luY2x1ZGUgPGlvc3RyZWFtPgoKLy8gRnVuY3Rpb24gdGhhdCBjYWxjdWxhdGVzIGFuZCByZXR1cm5zIHRoZSBzcXVhcmUgb2YgYSBudW1iZXIKZG91YmxlIHNxdWFyZShkb3VibGUgbnVtYmVyKSB7CiAgICByZXR1cm4gbnVtYmVyICogbnVtYmVyOwp9CgppbnQgbWFpbigpIHsKICAgIGRvdWJsZSBudW0xOwogICAgc3RkOjpjaW4gPj4gbnVtMTsKICAgIHN0ZDo6Y291dCA8PCAiNCIgOwogICAgcmV0dXJuIDA7Cn0K',	'cpp',	'2',	'wrong',	10,	'2026-09-03 17:07:16.985+00',	'Failed Testcase',	'2026-09-03 17:07:16.985+00'),
(68,	'1',	'maitreya',	1,	1,	'I2luY2x1ZGUgPGlvc3RyZWFtPgoKLy8gRnVuY3Rpb24gdGhhdCBjYWxjdWxhdGVzIGFuZCByZXR1cm5zIHRoZSBzcXVhcmUgb2YgYSBudW1iZXIKZG91YmxlIHNxdWFyZShkb3VibGUgbnVtYmVyKSB7CiAgICByZXR1cm4gbnVtYmVyICogbnVtYmVyOwp9CgppbnQgbWFpbigpIHsKICAgIGRvdWJsZSBudW0xOwogICAgc3RkOjpjaW4gPj4gbnVtMTsKICAgIHN0ZDo6Y291dCA8PCAiNCIgOwogICAgcmV0dXJuIDA7Cn0K',	'cpp',	'2',	'wrong',	10,	'2026-09-03 17:08:58.761+00',	'Failed Testcase',	'2026-09-03 17:08:58.761+00'),
(69,	'1',	'maitreya',	1,	1,	'I2luY2x1ZGUgPGlvc3RyZWFtPgoKLy8gRnVuY3Rpb24gdGhhdCBjYWxjdWxhdGVzIGFuZCByZXR1cm5zIHRoZSBzcXVhcmUgb2YgYSBudW1iZXIKZG91YmxlIHNxdWFyZShkb3VibGUgbnVtYmVyKSB7CiAgICByZXR1cm4gbnVtYmVyICogbnVtYmVyOwp9CgppbnQgbWFpbigpIHsKICAgIGRvdWJsZSBudW0xOwogICAgc3RkOjpjaW4gPj4gbnVtMTsKICAgIHN0ZDo6Y291dCA8PCAiNCIgOwogICAgcmV0dXJuIDA7Cn0K',	'cpp',	'2',	'wrong',	10,	'2026-09-03 17:11:11.473+00',	'Failed Testcase',	'2026-09-03 17:11:11.473+00'),
(70,	'1',	'maitreya',	1,	1,	'I2luY2x1ZGUgPGlvc3RyZWFtPgoKLy8gRnVuY3Rpb24gdGhhdCBjYWxjdWxhdGVzIGFuZCByZXR1cm5zIHRoZSBzcXVhcmUgb2YgYSBudW1iZXIKZG91YmxlIHNxdWFyZShkb3VibGUgbnVtYmVyKSB7CiAgICByZXR1cm4gbnVtYmVyICogbnVtYmVyOwp9CgppbnQgbWFpbigpIHsKICAgIGRvdWJsZSBudW0xOwogICAgc3RkOjpjaW4gPj4gbnVtMTsKICAgIHN0ZDo6Y291dCA8PCAiNCIgOwogICAgcmV0dXJuIDA7Cn0K',	'cpp',	'2',	'wrong',	10,	'2026-09-03 17:19:23.976+00',	'Failed Testcase',	'2026-09-03 17:19:23.976+00'),
(103,	'1',	'maitreya',	1,	1,	'I2luY2x1ZGUgPGlvc3RyZWFtPgoKLy8gRnVuY3Rpb24gdGhhdCBjYWxjdWxhdGVzIGFuZCByZXR1cm5zIHRoZSBzcXVhcmUgb2YgYSBudW1iZXIKZG91YmxlIHNxdWFyZShkb3VibGUgbnVtYmVyKSB7CiAgICByZXR1cm4gbnVtYmVyICogbnVtYmVyOwp9CgppbnQgbWFpbigpIHsKICAgIGRvdWJsZSBudW0xOwogICAgc3RkOjpjaW4gPj4gbnVtMTsKICAgIHN0ZDo6Y291dCA8PCAiNCIgOwogICAgcmV0dXJuIDA7Cn0K',	'cpp',	'2',	'wrong',	10,	'2026-09-03 17:21:40.814+00',	'Failed Testcase',	'2026-09-03 17:21:40.814+00'),
(136,	'1',	'maitreya',	1,	1,	'I2luY2x1ZGUgPGlvc3RyZWFtPgoKLy8gRnVuY3Rpb24gdGhhdCBjYWxjdWxhdGVzIGFuZCByZXR1cm5zIHRoZSBzcXVhcmUgb2YgYSBudW1iZXIKZG91YmxlIHNxdWFyZShkb3VibGUgbnVtYmVyKSB7CiAgICByZXR1cm4gbnVtYmVyICogbnVtYmVyOwp9CgppbnQgbWFpbigpIHsKICAgIGRvdWJsZSBudW0xOwogICAgc3RkOjpjaW4gPj4gbnVtMTsKICAgIHN0ZDo6Y291dCA8PCAiNCIgOwogICAgcmV0dXJuIDA7Cn0K',	'cpp',	'2',	'wrong',	10,	'2026-09-03 17:25:07.082+00',	'Failed Testcase',	'2026-09-03 17:25:07.083+00'),
(169,	'1',	'maitreya',	1,	1,	'I2luY2x1ZGUgPGlvc3RyZWFtPgoKLy8gRnVuY3Rpb24gdGhhdCBjYWxjdWxhdGVzIGFuZCByZXR1cm5zIHRoZSBzcXVhcmUgb2YgYSBudW1iZXIKZG91YmxlIHNxdWFyZShkb3VibGUgbnVtYmVyKSB7CiAgICByZXR1cm4gbnVtYmVyICogbnVtYmVyOwp9CgppbnQgbWFpbigpIHsKICAgIGRvdWJsZSBudW0xOwogICAgc3RkOjpjaW4gPj4gbnVtMTsKICAgIHN0ZDo6Y291dCA8PCAiNCIgOwogICAgcmV0dXJuIDA7Cn0K',	'cpp',	'2',	'wrong',	10,	'2026-09-03 17:29:30.635+00',	'Failed Testcase',	'2026-09-03 17:29:30.635+00'),
(170,	'1',	'maitreya',	1,	1,	'I2luY2x1ZGUgPGlvc3RyZWFtPgoKLy8gRnVuY3Rpb24gdGhhdCBjYWxjdWxhdGVzIGFuZCByZXR1cm5zIHRoZSBzcXVhcmUgb2YgYSBudW1iZXIKZG91YmxlIHNxdWFyZShkb3VibGUgbnVtYmVyKSB7CiAgICByZXR1cm4gbnVtYmVyICogbnVtYmVyOwp9CgppbnQgbWFpbigpIHsKICAgIGRvdWJsZSBudW0xOwogICAgc3RkOjpjaW4gPj4gbnVtMTsKICAgIHN0ZDo6Y291dCA8PCAiNCIgOwogICAgcmV0dXJuIDA7Cn0K',	'cpp',	'2',	'wrong',	10,	'2026-09-03 17:30:17.435+00',	'Failed Testcase',	'2026-09-03 17:30:17.435+00'),
(171,	'1',	'maitreya',	1,	1,	'I2luY2x1ZGUgPGlvc3RyZWFtPgoKLy8gRnVuY3Rpb24gdGhhdCBjYWxjdWxhdGVzIGFuZCByZXR1cm5zIHRoZSBzcXVhcmUgb2YgYSBudW1iZXIKZG91YmxlIHNxdWFyZShkb3VibGUgbnVtYmVyKSB7CiAgICByZXR1cm4gbnVtYmVyICogbnVtYmVyOwp9CgppbnQgbWFpbigpIHsKICAgIGRvdWJsZSBudW0xOwogICAgc3RkOjpjaW4gPj4gbnVtMTsKICAgIHN0ZDo6Y291dCA8PCAiNCIgOwogICAgcmV0dXJuIDA7Cn0K',	'cpp',	'2',	'wrong',	10,	'2026-09-03 17:31:13.273+00',	'Failed Testcase',	'2026-09-03 17:31:13.273+00'),
(172,	'1',	'maitreya',	1,	1,	'I2luY2x1ZGUgPGlvc3RyZWFtPgoKLy8gRnVuY3Rpb24gdGhhdCBjYWxjdWxhdGVzIGFuZCByZXR1cm5zIHRoZSBzcXVhcmUgb2YgYSBudW1iZXIKZG91YmxlIHNxdWFyZShkb3VibGUgbnVtYmVyKSB7CiAgICByZXR1cm4gbnVtYmVyICogbnVtYmVyOwp9CgppbnQgbWFpbigpIHsKICAgIGRvdWJsZSBudW0xOwogICAgc3RkOjpjaW4gPj4gbnVtMTsKICAgIHN0ZDo6Y291dCA8PCAiNCIgOwogICAgcmV0dXJuIDA7Cn0K',	'cpp',	'2',	'wrong',	10,	'2026-09-03 17:31:42.316+00',	'Failed Testcase',	'2026-09-03 17:31:42.316+00'),
(173,	'1',	'maitreya',	1,	1,	'I2luY2x1ZGUgPGlvc3RyZWFtPgoKLy8gRnVuY3Rpb24gdGhhdCBjYWxjdWxhdGVzIGFuZCByZXR1cm5zIHRoZSBzcXVhcmUgb2YgYSBudW1iZXIKZG91YmxlIHNxdWFyZShkb3VibGUgbnVtYmVyKSB7CiAgICByZXR1cm4gbnVtYmVyICogbnVtYmVyOwp9CgppbnQgbWFpbigpIHsKICAgIGRvdWJsZSBudW0xOwogICAgc3RkOjpjaW4gPj4gbnVtMTsKICAgIHN0ZDo6Y291dCA8PCAiNCIgOwogICAgcmV0dXJuIDA7Cn0K',	'cpp',	'2',	'wrong',	10,	'2026-09-03 17:31:53.357+00',	'Failed Testcase',	'2026-09-03 17:31:53.357+00'),
(202,	'1',	'maitreya',	1,	1,	'I2luY2x1ZGUgPGlvc3RyZWFtPgoKLy8gRnVuY3Rpb24gdGhhdCBjYWxjdWxhdGVzIGFuZCByZXR1cm5zIHRoZSBzcXVhcmUgb2YgYSBudW1iZXIKZG91YmxlIHNxdWFyZShkb3VibGUgbnVtYmVyKSB7CiAgICByZXR1cm4gbnVtYmVyICogbnVtYmVyOwp9CgppbnQgbWFpbigpIHsKICAgIGRvdWJsZSBudW0xOwogICAgc3RkOjpjaW4gPj4gbnVtMTsKICAgIHN0ZDo6Y291dCA8PCAiNCIgOwogICAgcmV0dXJuIDA7Cn0K',	'cpp',	'2',	'wrong',	10,	'2026-09-03 17:35:02.696+00',	'Failed Testcase',	'2026-09-03 17:35:02.696+00'),
(203,	'1',	'maitreya',	1,	1,	'cHJpbnQoIkhlbGxvLCBXb3JsZCEiKQ==',	'python',	'1',	'wrong',	0,	'2026-09-03 18:14:56.247+00',	'Failed Testcase',	'2026-09-03 18:14:56.247+00'),
(204,	'1',	'maitreya',	1,	1,	'I2luY2x1ZGUgPGlvc3RyZWFtPg0KdXNpbmcgbmFtZXNwYWNlIHN0ZDsNCg0KaW50IG1haW4oKSB7DQogIHdoaWxlKHRydWUpew0KICAgIGNvdXQgPDwgIkhlbGxvLCBXb3JsZCEiIDw8IGVuZGw7DQoNCiAgfQ0KICAgIHJldHVybiAwOw0KfQ==',	'cpp',	'1',	'timeout',	0,	'2026-09-03 18:15:19.125+00',	'Time Limit Exceeded',	'2026-09-03 18:15:19.125+00'),
(205,	'1',	'maitreya',	1,	1,	'I2luY2x1ZGUgPGlvc3RyZWFtPg0KdXNpbmcgbmFtZXNwYWNlIHN0ZDsNCg0KaW50IG1haW4oKSB7DQogIHdoaWxlKHRydWUpew0KICAgIGNvdXQgPDwgIkhlbGxvLCBXb3JsZCEiIDw8IGVuZGw7DQogIH0NCiAgICByZXR1cm4gMDsNCn0=',	'cpp',	'1',	'timeout',	0,	'2026-09-03 18:21:47.928+00',	'Time Limit Exceeded',	'2026-09-03 18:21:47.928+00'),
(206,	'1',	'maitreya',	1,	1,	'cHJpbnQoIkhlbGxvLCBXb3JsZCEiKQ==',	'python',	'1',	'wrong',	0,	'2026-09-03 19:21:55.971+00',	'Failed Testcase',	'2026-09-03 19:21:55.971+00');

CREATE TABLE "public"."user" (
    "id" serial NOT NULL,
    "username" character varying(255),
    "teamname" character varying(255) DEFAULT 'TEAM' NOT NULL,
    "password" character varying(255),
    "rc" character varying(255),
    "isjunior" boolean DEFAULT false NOT NULL,
    "role" character varying(100) DEFAULT 'USER' NOT NULL,
    CONSTRAINT "user_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);

DO $$ BEGIN PERFORM setval('"public"."user_id_seq"', 1); END $$;

INSERT INTO "user" ("id", "username", "teamname", "password", "rc", "isjunior", "role") VALUES
(1,	'maitreya',	'maitreya',	'$2a$10$gOH1RDZH25Va7sTxhdxHdOBBHM65.c0/VeUX7nP0/zI4WWAznw.gy',	'1',	false,	'USER');

ALTER TABLE ONLY "public"."leaderboards" ADD CONSTRAINT "leaderboards_event_id_fkey" FOREIGN KEY (event_id) REFERENCES "public".events(id);

ALTER TABLE ONLY "public"."problems" ADD CONSTRAINT "problems_event_id_fkey" FOREIGN KEY (event_id) REFERENCES "public".events(id) ON UPDATE CASCADE ON DELETE RESTRICT;

ALTER TABLE ONLY "public"."problemsamples" ADD CONSTRAINT "problemsamples_problem_id_fkey" FOREIGN KEY (problem_id) REFERENCES "public".problems(id) ON UPDATE CASCADE ON DELETE RESTRICT;

ALTER TABLE ONLY "public"."submissions" ADD CONSTRAINT "submissions_event_id_fkey" FOREIGN KEY (event_id) REFERENCES "public".events(id);
ALTER TABLE ONLY "public"."submissions" ADD CONSTRAINT "submissions_problem_id_fkey" FOREIGN KEY (problem_id) REFERENCES "public".problems(id);

-- 2026-09-03 19:38:05 UTC
