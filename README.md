# SaytNorsk - Norwegian Spelling Test Platform

A modern, extensible web platform for Norwegian language testing with multilingual support (English/Russian interface, with Norwegian content). Built with Django, Next.js, and PostgreSQL.

## 🎯 Features

### Core Functionality
- **Fill-in-the-blank** questions (MVP)
- **Multiple choice** (built-in, easy to enable)
- **Drag & drop** (ready for implementation)
- **Error finding** (ready for implementation)
- **Audio support** (ready for implementation)

### Learning Management
- **Lessons** organized by proficiency level (A1-C2)
- **Tests** with various question types
- **Automatic scoring** with letter grades (A-F)
- **Error breakdown** showing correct/incorrect answers
- **Student tracking** (anonymous or named)

### Multi-language Support
- **EN/RU** language switching on frontend
- **Django i18n** for server translations
- Easy to add more languages

### Admin Dashboard
- **Django Jazzmin** beautiful admin interface
- Manage lessons, tests, questions, and answers
- Upload images and audio files
- Configure test settings

## 🛠️ Technology Stack

- **Backend**: Django 5.0 + Django REST Framework
- **Frontend**: Next.js 15 + React 18 + Tailwind CSS
- **Database**: PostgreSQL
- **Admin**: Django Jazzmin
- **Authentication**: JWT + Session
- **Containerization**: Docker & Docker Compose
- **Translations**: Django i18n + next-i18next

## 📋 Project Structure

```
SaytNorsk/
├── backend/
│   ├── config/              # Django configuration
│   ├── apps/
│   │   ├── core/           # Core utilities
│   │   ├── tests/          # Tests app (models, serializers, views)
│   │   └── users/          # Users/roles
│   ├── locale/             # Translation files
│   ├── manage.py
│   └── requirements.txt
├── frontend/
│   ├── app/                # Next.js app directory
│   ├── pages/              # Page components
│   ├── components/         # React components
│   ├── lib/                # API utilities
│   ├── public/
│   │   └── locales/        # i18n translations
│   ├── tailwind.config.ts
│   ├── next.config.js
│   └── package.json
├── docker-compose.yml      # Container orchestration
├── Dockerfile.backend      # Backend container
├── Dockerfile.frontend     # Frontend container
└── README.md

```

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Or: Python 3.11+, Node.js 20+

### Using Docker (Recommended)

1. **Clone and setup**:
   ```bash
   cd SaytNorsk
   cp backend/.env.example backend/.env
   ```

2. **Start services**:
   ```bash
   docker-compose up --build
   ```

3. **Create superuser**:
   ```bash
   docker-compose exec backend python manage.py createsuperuser
   ```

4. **Access**:
   - Frontend: http://localhost:3000
   - Admin: http://localhost:8000/admin
   - API: http://localhost:8000/api

### Local Development

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

**Frontend**:
```bash
cd frontend
npm install
npm run dev
```

## 📚 Database Models

### Lesson
- `title`: Lesson name
- `description`: Lesson overview
- `level`: A1-C2 proficiency level
- `created_by`: Teacher who created it
- Timestamps: created_at, updated_at

### Test
- `lesson`: Foreign key to Lesson
- `title`: Test name
- `test_type`: fill-in-the-blank, multiple-choice, etc.
- `show_correct_answers`: Boolean to reveal answers
- `show_errors_breakdown`: Boolean to show error details
- `duration_minutes`: Time limit
- Timestamps: created_at, updated_at

### Question
- `test`: Foreign key to Test
- `text`: Question/sentence text (use [...] for blanks)
- `audio_file`: Optional audio for listening questions
- `image`: Optional image
- `order`: Question sequence
- `difficulty`: 1-5 scale
- `explanation`: Optional explanation
- Related: `answers` (reverse relation)

### Answer
- `question`: Foreign key to Question
- `text`: Answer text
- `is_correct`: Boolean flag
- `explanation`: Why correct/incorrect
- `order`: Display order

### StudentResult
- `student_name`: Student name (optional)
- `test`: Foreign key to Test
- `total_questions`: Number of questions
- `correct_answers`: Number correct
- `score_percentage`: 0-100
- `score_letter`: A-F grade
- `completed_at`: Timestamp
- Related: `answers` (reverse relation - StudentAnswer)

### StudentAnswer
- `result`: Foreign key to StudentResult
- `question`: Foreign key to Question
- `student_answer`: What student submitted
- `correct_answer`: Correct response
- `is_correct`: Boolean flag

## 🎓 Admin Panel Usage

1. **Login**: Navigate to `http://localhost:8000/admin`

2. **Create Lesson**:
   - Click "+ Lesson"
   - Fill in title, description, level
   - Save

3. **Create Test**:
   - Click "+ Test"
   - Select lesson
   - Set test type (e.g., "Fill in the Blank")
   - Configure: show_correct_answers, show_errors_breakdown
   - Save

4. **Add Questions**:
   - Click "+ Question"
   - Select test
   - Write question text (use `[...]` for fill-in-the-blank)
   - Add answers:
     - Mark one as "is_correct"
     - Add all options

5. **View Results**:
   - Go to "Student Results"
   - See scores, grades, student answers
   - Click result to see answer breakdown

## 📝 API Endpoints

### Lessons
- `GET /api/lessons/` - List all lessons
- `GET /api/lessons/{id}/` - Get lesson details
- `GET /api/lessons/?level=A1` - Filter by level

### Tests
- `GET /api/tests/` - List all tests
- `GET /api/tests/{id}/` - Get test details
- `POST /api/tests/{id}/submit_answers/` - Submit test

### Questions
- `GET /api/questions/?test={test_id}` - Get questions for test

### Submit Test Endpoint

```json
POST /api/tests/{id}/submit_answers/
{
  "student_name": "John Doe",  // optional
  "answers": [
    {
      "question_id": 1,
      "answer": "student response"
    },
    ...
  ]
}

Response:
{
  "id": 1,
  "score_percentage": 85.5,
  "score_letter": "B",
  "correct_answers": 17,
  "total_questions": 20,
  "answers": [
    {
      "question": 1,
      "student_answer": "response",
      "correct_answer": "correct",
      "is_correct": true
    },
    ...
  ]
}
```

## 🌐 Internationalization

### Adding New Language

1. **Backend** (Django):
   ```bash
   cd backend
   python manage.py makemessages -l fr
   # Edit locale/fr/LC_MESSAGES/django.po
   python manage.py compilemessages
   ```

2. **Frontend** (Next.js i18next):
   - Create `frontend/public/locales/fr/common.json`
   - Add translations

3. **Update config**:
   - `backend/config/settings.py`: Add to `LANGUAGES`
   - `frontend/next-i18next.config.js`: Add to `locales`

## 🔐 Authentication

Currently supports:
- **No auth required** for students taking tests
- **Session auth** for admin access
- **JWT tokens** available (can be enabled for API access)

To enable JWT:
1. User obtains token via `/api/token/` endpoint
2. Send token in header: `Authorization: Bearer <token>`

## 🐳 Docker Deployment

### Environment Variables

Create `.env` file in backend:
```
DEBUG=False
SECRET_KEY=your-secret-key-here
DB_NAME=saytnorsk_db
DB_USER=postgres
DB_PASSWORD=your-secure-password
DB_HOST=db
DB_PORT=5432
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
CORS_ALLOWED_ORIGINS=https://yourdomain.com
```

### Build and Run

```bash
docker-compose -f docker-compose.yml up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## 📈 Extending the Platform

### Add New Question Type

1. **Update model** in `apps/tests/models.py`:
   ```python
   TEST_TYPE_CHOICES = [
       ...
       ('new-type', 'New Type'),
   ]
   ```

2. **Create component** in `frontend/components/NewType.tsx`

3. **Update test page** `frontend/pages/test/[id].tsx`:
   ```tsx
   if (test.test_type === 'new-type') {
     return <NewType ... />
   }
   ```

4. **Update scoring logic** in `apps/tests/views.py` if needed

### Add Features

Examples for future implementation:
- **Listening**: Upload MP3, show waveform, time limit
- **Drag & drop**: Reorder words/letters using React Beautiful DND
- **Error finding**: Highlight clickable words, select replacement
- **Statistics**: Per-student progress, class analytics
- **Certificates**: Generate PDF completion certificates
- **Leaderboards**: Score rankings by lesson
- **Mobile app**: React Native version
- **Teacher dashboard**: View all student results
- **Automatic grading reports**: Email summaries

## 🤝 Contributing

1. Create feature branch: `git checkout -b feature/name`
2. Make changes following code style
3. Test thoroughly
4. Create pull request

## 📞 Support

For issues, questions, or suggestions:
1. Check existing documentation
2. Review admin panel guides
3. Check API endpoint examples
4. Submit issue with details

## 📄 License

This project is provided as-is for educational and commercial use.

---

**Built with ❤️ for Norwegian language learners**
