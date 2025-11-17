# SaytNorsk – Norwegian Spelling Test Platform

Modern full-stack app for practicing Norwegian spelling. Django REST backend + Next.js frontend with bilingual UI (EN/NO) and ready-made A1 sample lessons/tests.

---

## Features
- Lessons and tests (fill-in-the-blank, extendable to MCQ/drag-drop/error-find)
- Auto scoring with letter grades; review answers
- Multilingual UI (EN/NO); sample Norwegian content included
- Admin panel (Jazzmin) to manage lessons/tests/questions/answers

## Tech stack
- **Backend:** Django 5, DRF, Jazzmin, SQLite (local) / Postgres-ready
- **Frontend:** Next.js 15 (Pages), React 18, Tailwind CSS
- **Auth:** JWT + Session-ready
- **Infra:** Docker & Docker Compose

---

## Quick start

### Docker (recommended)
```bash
cp backend/.env.example backend/.env
docker compose up --build
```
Access:
- Frontend: http://localhost:3000
- API: http://localhost:8000/api/
- Admin: http://localhost:8000/admin/ (create superuser after start)

### Local (SQLite)
Backend:
```bash
cd backend
python -m venv venv
.\venv\Scripts\activate           # PowerShell (Windows)
pip install --upgrade pip
pip install -r requirements.txt

set DB_ENGINE=django.db.backends.sqlite3
set DB_NAME=%cd%\db.sqlite3

python manage.py migrate
python manage.py createsuperuser
python create_test_data.py        # seed demo data
python manage.py runserver
```

Frontend:
```bash
cd frontend
npm ci
npm run dev                       # http://localhost:3000
```

---

## Demo data
`backend/create_test_data.py` seeds:
- 3 lessons (A1: greetings, verbs, vowels)
- 3 tests, 9 questions, 14 answers

Run after migrations (from repo root or backend dir). Uses/creates `admin` user if missing.

---

## Useful commands
- Backend checks/tests: `cd backend && python manage.py check && python manage.py test`
- Frontend lint: `cd frontend && npm run lint`
- Seed data: `python backend/create_test_data.py`

---

## CI (GitHub Actions)
- **Frontend CI:** install deps, `npm run lint`.
- **Backend CI:** install deps, SQLite migrate, `manage.py check`, `manage.py test`.

---

## Configuration
- Backend env template: `backend/.env.example`
- For Postgres: set `DB_ENGINE=django.db.backends.postgresql` and configure `DB_*` vars.
- Keep real secrets (.env) out of Git.

---

## Production hints
- Backend: collect static (`python manage.py collectstatic --noinput`), serve via gunicorn (`gunicorn config.wsgi:application --bind 0.0.0.0:8000`).
- Frontend: `npm ci && npm run build`, serve with `npm run start`.
- Set `NEXT_PUBLIC_API_URL` to the backend API URL.
