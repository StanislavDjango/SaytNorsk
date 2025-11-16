# 🚀 SaytNorsk - Quick Start Guide

Welcome to **SaytNorsk** - the Norwegian spelling test platform! Follow this guide to get up and running in minutes.

## ⚡ 5-Minute Quick Start

### Prerequisites
- Docker & Docker Compose installed
- Basic terminal/command prompt knowledge

### Step 1: Clone and Setup (1 min)
```bash
cd SaytNorsk
cp backend/.env.example backend/.env
```

### Step 2: Start Services (1 min)
```bash
# On Windows:
setup.bat

# On Mac/Linux:
bash setup.sh
```

Or manually:
```bash
docker-compose up --build
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser
```

### Step 3: Create Test Data (2 min)

1. **Open Admin Panel**: http://localhost:8000/admin
   - Login with superuser credentials

2. **Create a Lesson**:
   - Click "+ Lesson"
   - Title: "Basic Norwegian"
   - Level: "A1"
   - Save

3. **Create a Test**:
   - Click "+ Test"
   - Lesson: "Basic Norwegian"
   - Title: "Verb Practice"
   - Test Type: "Fill in the Blank"
   - Save

4. **Add Questions**:
   - Click "+ Question"
   - Text: "Jeg [går] til skolen"
   - Click "+ Answer": "går" (mark is_correct)
   - Click "+ Answer": "gikk"
   - Save

5. **Test It**: http://localhost:3000
   - Select your lesson
   - Take the test
   - See results with scoring

### Step 4: Access Your App (Done!)

| Service | URL |
|---------|-----|
| **Student App** | http://localhost:3000 |
| **Admin Panel** | http://localhost:8000/admin |
| **API** | http://localhost:8000/api |

---

## 📚 Understanding the Structure

### Frontend (Next.js)
- Student-facing interface
- No login required to take tests
- Multi-language support (EN/RU)
- Visit: http://localhost:3000

### Admin (Django Jazzmin)
- Teachers create lessons/tests
- Manage questions and answers
- Upload images/audio
- View student results
- Visit: http://localhost:8000/admin

### Backend (Django REST API)
- Serves test data
- Calculates scores
- Stores results
- Auto-grading logic

---

## 🎓 Creating Your First Complete Test

### Complete Workflow Example

**Goal**: Create a fill-in-the-blank test about Norwegian pronouns

#### 1. Login to Admin Panel
- Go to: http://localhost:8000/admin
- Enter superuser credentials

#### 2. Create Lesson
```
Title: "Norwegian Pronouns"
Description: "Learn Norwegian personal pronouns"
Level: A1
```

#### 3. Create Test
```
Lesson: Norwegian Pronouns
Title: "Pronoun Fill-in-the-Blank"
Description: "Fill in the correct pronoun"
Test Type: Fill in the Blank
Duration: 10 minutes
Show Correct Answers: ✓ Checked
Show Errors Breakdown: ✓ Checked
```

#### 4. Add Question 1
```
Text: "_______ er student" (_____ is a student)
Order: 1
Difficulty: 1

Answers:
  ✓ "Jeg" (I) - is_correct: YES
    "Du" (You)
    "Han" (He)
```

#### 5. Add Question 2
```
Text: "Han er fra Norge og _______ snakker norsk"
Order: 2
Difficulty: 2

Answers:
  "eg" (I)
  ✓ "han" (he) - is_correct: YES
    "hun" (she)
```

#### 6. Repeat for Questions 3-5
Add more questions following the same pattern.

#### 7. Test as Student
1. Visit http://localhost:3000
2. Click "Norwegian Pronouns" lesson
3. Click "Start Test"
4. Enter your name (optional)
5. Answer the questions
6. Submit and see results!

---

## 🌐 Language Support

### English Interface (Default)
Already set up. Students see English prompts.

### Russian Interface
1. Click language switcher (top right)
2. Select "RU"
3. Interface switches to Russian

### Adding More Languages
See [DEVELOPMENT.md](./DEVELOPMENT.md) section "Adding New Language"

---

## 🎯 Test Types Overview

### Currently Available

**Fill-in-the-Blank** ✅
- Student types missing word
- Auto-graded
- Example: "Jeg [____] på skolen"

### Coming Soon

**Multiple Choice**
- Student selects from 3-4 options
- Auto-graded

**Drag & Drop**
- Reorder words/letters
- Visual interaction

**Find Error**
- Highlight wrong word
- Select correction

**Listening**
- Play audio clip
- Student types what they hear

---

## 📊 Grading System

### Automatic Scoring

Percentage → Letter Grade:
- **90-100%** → A
- **80-89%** → B
- **70-79%** → C
- **60-69%** → D
- **50-59%** → E
- **Below 50%** → F

### Example
```
Student answers 17 out of 20 questions correctly:
17/20 = 85%
Grade: B (80-89% range)
```

---

## 🔧 Useful Commands

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Access Database
```bash
# PostgreSQL shell
docker-compose exec db psql -U postgres -d saytnorsk_db
```

### Run Django Management Commands
```bash
# Create another admin user
docker-compose exec backend python manage.py createsuperuser

# Check migrations
docker-compose exec backend python manage.py showmigrations

# Run tests
docker-compose exec backend python manage.py test apps.tests
```

### Stop Services
```bash
# On Windows:
stop.bat

# On Mac/Linux:
bash stop.sh

# Or manually:
docker-compose down
```

---

## 🐛 Troubleshooting

### "Can't connect to localhost:3000"
- **Check if frontend is running**: `docker-compose logs frontend`
- **Rebuild**: `docker-compose up --build frontend`
- **Wait**: Sometimes frontend takes 30 seconds to start

### "Admin panel shows error"
- **Check migrations**: `docker-compose exec backend python manage.py migrate`
- **Restart backend**: `docker-compose restart backend`

### "Database connection refused"
- **Wait 10 seconds** for database startup
- **Check db logs**: `docker-compose logs db`
- **Rebuild everything**: `docker-compose down && docker-compose up --build`

### "Port already in use"
```bash
# Kill process on port
# On Windows:
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# On Mac/Linux:
lsof -ti:3000 | xargs kill -9
```

---

## 📈 Next Steps

After completing quick start:

1. **Create More Tests**
   - Follow the workflow above
   - Create 3-5 tests per lesson
   - Different difficulty levels

2. **Add Media**
   - Upload images with questions
   - Add pronunciation audio files
   - Enhance visual experience

3. **Customize**
   - Change Tailwind colors
   - Add your school logo
   - Customize admin interface

4. **Deploy**
   - See [README.md](./README.md) Deployment section
   - Set up on server
   - Enable HTTPS

5. **Extend Features**
   - Add new question types
   - Student statistics
   - Teacher dashboard
   - Mobile app

---

## 📖 Documentation

- **Full Setup**: [README.md](./README.md)
- **Development**: [DEVELOPMENT.md](./DEVELOPMENT.md)
- **API Reference**: [README.md - API Endpoints](./README.md#-api-endpoints)
- **Database Schema**: [DEVELOPMENT.md - Database Schema](./DEVELOPMENT.md#database-schema)

---

## 💡 Pro Tips

✅ **Tip 1**: Use `[...]` for fill-in-the-blank questions
```
Good: "Jeg [...] på skolen" 
Bad: "Jeg ____ på skolen"
```

✅ **Tip 2**: Add explanations to answers
```
Answer: "går"
Explanation: "Present tense of 'å gå' (to go)"
```

✅ **Tip 3**: Set difficulty levels
```
Level 1: Basic vocabulary
Level 3: Regular verbs
Level 5: Irregular verbs
```

✅ **Tip 4**: Use order numbers for question sequence
```
Q1: Order 1
Q2: Order 2
...
```

✅ **Tip 5**: Preview as student frequently
Test your own content before students use it!

---

## 🎉 You're Ready!

Congratulations! 🎊

You now have a fully functional Norwegian test platform. Start creating lessons and tests, and share the student link (http://localhost:3000) with learners.

**Questions?** See the [README.md](./README.md) or [DEVELOPMENT.md](./DEVELOPMENT.md) for more details.

**Happy teaching!** 📚✨
