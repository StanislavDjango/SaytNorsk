# SaytNorsk Development Setup

## Project Overview

**SaytNorsk** is a comprehensive Norwegian language testing platform with:
- Modern web interface (Next.js 15 + React 18)
- Powerful admin panel (Django Jazzmin)
- RESTful API (Django REST Framework)
- Multi-language support (EN/RU interface)
- Extensible architecture for any school assignments

## Quick Links

- 📖 [Full Documentation](./README.md)
- 🏗️ Backend: `./backend/`
- 🎨 Frontend: `./frontend/`
- 🐳 Docker: `docker-compose.yml`

## Directory Structure

```
SaytNorsk/
├── backend/                    # Django REST API
│   ├── config/                # Django settings
│   ├── apps/
│   │   ├── core/              # Shared utilities
│   │   ├── tests/             # Lessons & Tests models
│   │   └── users/             # User management
│   ├── locale/                # Translations (i18n)
│   ├── media/                 # User uploads
│   ├── staticfiles/           # Compiled static files
│   ├── manage.py
│   └── requirements.txt
│
├── frontend/                   # Next.js 15 frontend
│   ├── app/                   # Next.js app directory
│   ├── pages/                 # Page routes
│   ├── components/            # React components
│   ├── lib/                   # Utilities & API calls
│   ├── public/
│   │   └── locales/           # Translation JSON files
│   ├── styles/                # Tailwind styles
│   └── package.json
│
├── docker-compose.yml         # Multi-container setup
├── Dockerfile.backend         # Backend image
├── Dockerfile.frontend        # Frontend image
├── .env.example              # Environment template
├── .gitignore
├── README.md
└── DEVELOPMENT.md            # This file
```

## Database Schema

### Core Models

**Lesson** - Course/unit
- title, description, level (A1-C2), created_by, timestamps

**Test** - Quiz/exam
- lesson, title, description, test_type, settings, timestamps

**Question** - Individual item
- test, text, audio_file, image, order, difficulty, explanation

**Answer** - Possible responses
- question, text, is_correct, explanation, order

**StudentResult** - Test completion
- student_name, test, scores, grade, answers, timestamp

**StudentAnswer** - Individual response
- result, question, student_answer, correct_answer, is_correct

## API Examples

### Get Lessons
```bash
curl http://localhost:8000/api/lessons/
```

### Get Test with Questions
```bash
curl http://localhost:8000/api/tests/1/
```

### Submit Test Answers
```bash
curl -X POST http://localhost:8000/api/tests/1/submit_answers/ \
  -H "Content-Type: application/json" \
  -d '{
    "student_name": "John",
    "answers": [
      {"question_id": 1, "answer": "svaret"},
      {"question_id": 2, "answer": "annet svar"}
    ]
  }'
```

## Frontend Components

### Pages
- `/` - Home (lessons list)
- `/lesson/[id]` - Lesson details with tests
- `/test/[id]` - Test interface

### Components
- `Header` - Navigation & language switcher
- `FillInTheBlank` - Question input UI
- `Results` - Score display & error breakdown
- `ProgressBar` - Question counter

## Languages & i18n

### Backend (Django i18n)
Located in `backend/locale/`:
- `en/LC_MESSAGES/django.po` - English
- `ru/LC_MESSAGES/django.po` - Russian
- `no/LC_MESSAGES/django.po` - Norwegian

### Frontend (next-i18next)
Located in `frontend/public/locales/`:
- `en/common.json`
- `ru/common.json`

To add a language:
1. Create locale folder in both backend & frontend
2. Add translation files
3. Update config files:
   - `backend/config/settings.py`: Add to LANGUAGES
   - `frontend/next-i18next.config.js`: Add to locales array

## Admin Panel

Access at: `http://localhost:8000/admin/`

### Features
- Create/edit lessons and tests
- Manage questions and answers
- Upload images and audio
- View student results
- Configure test settings
- Beautiful UI with Jazzmin

### Creating a Test

1. **Create Lesson**
   - Admin → Lessons → + Add Lesson
   - Set title, description, level

2. **Create Test**
   - Admin → Tests → + Add Test
   - Select lesson, set type, configure settings

3. **Add Questions**
   - Admin → Questions → + Add Question
   - Write question text (use `[...]` for blanks)
   - Add answers (mark correct one)
   - Upload images/audio if needed

4. **Test It**
   - Visit student frontend at http://localhost:3000
   - Start the test

## Example: Creating a Fill-in-the-Blank Test

### Step 1: Create Lesson (Admin)
- Title: "Basic Norwegian Verbs"
- Level: "A1"
- Description: "Learn common Norwegian verbs"

### Step 2: Create Test
- Title: "Verb Practice"
- Type: "Fill in the Blank"
- Questions: 5
- Settings: show_correct_answers=True

### Step 3: Add Questions
Question 1:
- Text: "Jeg [...] på skolen i dag" (I [go] to school today)
- Answer 1: "gå" (is_correct: True)
- Answer 2: "går" (is_correct: False)

Question 2:
- Text: "Han [...] kaffen sin" (He [drinks] his coffee)
- Answer 1: "drikk" (is_correct: False)
- Answer 2: "drikker" (is_correct: True)

### Step 4: Test as Student
1. Visit http://localhost:3000
2. Click lesson "Basic Norwegian Verbs"
3. Click test "Verb Practice"
4. Enter name
5. Fill in blanks
6. View results

## Running Locally

### Option 1: Docker (Recommended)

```bash
# Build and start
docker-compose up --build

# Migrations (first time)
docker-compose exec backend python manage.py migrate

# Create superuser
docker-compose exec backend python manage.py createsuperuser

# Access
# Frontend: http://localhost:3000
# Admin: http://localhost:8000/admin
# API: http://localhost:8000/api
```

### Option 2: Local Development

**Backend**:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

**Frontend** (new terminal):
```bash
cd frontend
npm install
npm run dev
```

## Development Workflow

### Making Changes

1. **Backend Changes**
   - Edit models in `apps/tests/models.py`
   - Run: `python manage.py makemigrations`
   - Run: `python manage.py migrate`
   - Update admin/serializers as needed
   - Restart server

2. **Frontend Changes**
   - Edit components in `components/`
   - Changes auto-reload with Next.js dev server
   - Update translations in `public/locales/`

3. **Adding Translations**
   - Backend: Edit `.po` files, compile with `compilemessages`
   - Frontend: Update JSON files

### Testing Admin Panel

1. Create test data via admin panel
2. View at http://localhost:8000/admin
3. Test frontend at http://localhost:3000

### Testing API

Use curl, Postman, or Thunder Client:
```bash
# List all tests
GET http://localhost:8000/api/tests/

# Get specific test
GET http://localhost:8000/api/tests/1/

# Submit answers
POST http://localhost:8000/api/tests/1/submit_answers/
```

## Extending the Platform

### Add New Question Type

1. Update `TEST_TYPE_CHOICES` in `models.py`
2. Create component in `frontend/components/`
3. Update `frontend/pages/test/[id].tsx` to render it
4. Update scoring logic in views if needed

### Add New Feature

Examples:
- **Listening**: Add audio UI component
- **Drag & Drop**: Integrate React Beautiful DND
- **Statistics**: Create analytics dashboard
- **Mobile**: Add React Native app
- **Certificates**: Generate PDF
- **Leaderboard**: Add scoring page

## Troubleshooting

### Database Issues
```bash
# Reset database (WARNING: deletes all data)
python manage.py flush
python manage.py migrate

# Check migrations
python manage.py showmigrations
```

### Missing Dependencies
```bash
# Backend
pip install -r requirements.txt

# Frontend
npm install
```

### Port Already in Use
```bash
# Change port in manage.py runserver or next dev
# Backend: python manage.py runserver 8001
# Frontend: npm run dev -- -p 3001
```

### Docker Issues
```bash
# Restart services
docker-compose restart

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Clean rebuild
docker-compose down -v
docker-compose up --build
```

## Useful Commands

### Backend

```bash
# Create admin user
python manage.py createsuperuser

# Run migrations
python manage.py migrate

# Create new app
python manage.py startapp appname

# Make messages for translation
python manage.py makemessages -l ru

# Compile translations
python manage.py compilemessages

# Collect static files
python manage.py collectstatic

# Run shell
python manage.py shell
```

### Frontend

```bash
# Install dependencies
npm install

# Development server
npm run dev

# Build
npm run build

# Production server
npm start

# Linting
npm run lint

# Type check
npm run type-check
```

## Deployment

See README.md for Docker deployment and production checklist.

## Next Steps

1. **Start with admin**: Create some lessons/tests
2. **Test student flow**: Try taking a test
3. **Customize styling**: Update Tailwind config
4. **Add languages**: Extend translations
5. **Extend features**: Add new question types
6. **Deploy**: Use Docker for production

## Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Next.js Documentation](https://nextjs.org/docs)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [next-i18next](https://github.com/i18next/next-i18next)

---

Happy coding! 🚀
