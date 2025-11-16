# SaytNorsk – Norwegian Spelling Test Platform

Full-stack playground for Norwegian language practice. Django REST backend + Next.js frontend, multilingual UI (EN/NO), and sample A1 lessons/tests preloaded via script.

## Stack
- Backend: Django 5, DRF, SQLite (local) / Postgres-ready, Jazzmin admin
- Frontend: Next.js 15 (App Router disabled; Pages directory), React 18, Tailwind CSS
- Auth: JWT + Session (ready)
- Containerization: Docker/Docker Compose

## Quick start

### Option 1: Docker (recommended)
```bash
cp backend/.env.example backend/.env
docker compose up --build
```
Access:
- Frontend: http://localhost:3000
- API: http://localhost:8000/api/
- Admin: http://localhost:8000/admin/ (create a superuser after containers start)

### Option 2: Local setup

Backend (SQLite):
```bash
cd backend
python -m venv venv
.\venv\Scripts\activate           # PowerShell (Windows)
pip install --upgrade pip
pip install -r requirements.txt

# Env vars (uses SQLite by default)
set DB_ENGINE=django.db.backends.sqlite3
set DB_NAME=%cd%\db.sqlite3

python manage.py migrate
python manage.py createsuperuser   # admin account
python create_test_data.py         # load demo lessons/tests
python manage.py runserver
```

Frontend:
```bash
cd frontend
npm ci
npm run dev                        # http://localhost:3000
```

## Demo data
Script `backend/create_test_data.py` seeds:
- 3 lessons (A1: greetings, verbs, vowels)
- 3 tests, 9 questions, 14 answers

Run it from repo root or backend folder after migrations. Default superuser used/created by script: `admin` (if absent).

## Commands
- Backend checks/tests: `cd backend && python manage.py check && python manage.py test`
- Frontend lint: `cd frontend && npm run lint`
- Seed data: `python backend/create_test_data.py`

## CI (GitHub Actions)
- `Frontend CI` – installs deps and runs `npm run lint`.
- `Backend CI` – installs deps, runs migrations (SQLite), `manage.py check`, and tests.

## Notes
- `.env.example` provided for backend; keep real secrets out of git.
- For Postgres, set `DB_ENGINE=django.db.backends.postgresql` and configure DB_* vars.
