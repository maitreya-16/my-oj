# Online Judge Node Backend

Express API for the online judge application. The service manages users, teams,
problems, submissions, results, leaderboards, event timing, and worker webhooks.
Submission execution is handled by the Flask services in the repository; this
service receives their webhook updates and exposes results through Server-Sent
Events (SSE).

## Requirements

- Docker
- Docker Compose

## Start

From the repository root, run:

```bash
docker pull gcc:latest
docker pull python:3.9-alpine
docker pull eclipse-temurin:21-jdk
docker compose up --build
