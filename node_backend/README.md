# Online Judge Node Backend

Express API for the online judge application. The service manages users, teams,
problems, submissions, results, leaderboards, event timing, and worker webhooks.
Submission execution is handled by the Flask services in the repository; this
service receives their webhook updates and exposes results through Server-Sent
Events (SSE).

## Requirements

- Node.js 18 or later
- PostgreSQL 15 or a compatible PostgreSQL server
- The Flask server and workers when running submission execution locally

## Install and run locally

From this directory:

```bash
npm install
npm run dev
```

The API listens on `http://localhost:3000` by default. Set `PORT` to use a
different port.

The server connects to PostgreSQL before it starts listening. Create a `.env`
file in `node_backend` with at least:

```env
PORT=3000
NODE_ENV=development
DB_URL=postgres://postgres:password@localhost:5432/postgres
JWT_SECRET=replace-with-a-long-random-secret
FLASK_API_BASE=http://localhost:5000
FRONTEND_URL=http://localhost:5173
```

`DB_URL` and `JWT_SECRET` are required for normal operation. `FLASK_API_BASE`
and `FRONTEND_URL` are used for service communication and CORS respectively.

## Production

The production command is:

```bash
npm start
```

The Docker image uses this command automatically. From the repository root,
start the complete stack with:

```bash
docker compose up --build
```

The Compose stack exposes the Node API on port `3000`, PostgreSQL on `5432`,
and Adminer on `8080`. In the Compose network, the backend connects to
PostgreSQL using the `postgres` hostname and the workers call the backend at
`http://backend:3000`.

For deployment, replace the example `JWT_SECRET` and database credentials in
the Compose configuration with secret values. The application binds to
`0.0.0.0` so it can receive traffic from Docker and a reverse proxy.

## API routes

All routes are prefixed as shown below. Routes marked **auth** require the JWT
cookie created during login. Admin routes require an admin-authenticated user.

| Prefix | Purpose |
| --- | --- |
| `/` | Health response |
| `/user` | Register, login, logout, profile, password, and history |
| `/admin` | Admin login and management of problems, users, teams, and events |
| `/problems` | Create, list, view, update, and delete problems and samples |
| `/submission` | Run code, submit code, and stream submission results |
| `/result` | Team results (**auth**) |
| `/leaderboard` | Leaderboard (**auth**) |
| `/time` | Event time remaining (**auth**) |
| `/webhook` | Run, system, and submit callbacks from the worker service |
| `/verify` | Verify the current JWT cookie (**auth**) |

### Submission result streaming

Clients can listen for a submission result using:

```text
GET /submission/sse/:submission_id
```

The endpoint returns an `text/event-stream` response. Result events are sent by
the worker webhook handlers at `/webhook/run`, `/webhook/system`, and
`/webhook/submit`.

## Available scripts

| Command | Description |
| --- | --- |
| `npm start` | Start the server for production |
| `npm run dev` | Start the server locally |
| `npm test` | Placeholder; no automated tests are configured |

## Project structure

```text
server.js             Express application and startup
config/               Database configuration
controllers/          Request handlers and SSE service
middlewares/          Authentication and submission validation
models/               Sequelize models and database synchronization
routes/               API route definitions
Dockerfile            Production container image
```

## Troubleshooting

- If startup fails before the server listens, check `DB_URL` and PostgreSQL availability.
- If protected routes return `403`, log in first and send the returned JWT cookie.
- If workers cannot report results, verify `BACKEND_URL` and that port `3000` is reachable from the worker container.
- Run `node --check server.js` for a quick syntax check.
