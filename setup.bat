@echo off
REM SaytNorsk Setup Script for Windows

echo.
echo 🚀 SaytNorsk Setup Script
echo =========================
echo.

REM Check if Docker is installed
where docker >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Docker is not installed. Please install Docker Desktop for Windows first.
    exit /b 1
)

echo Step 1: Creating environment file
if not exist "backend\.env" (
    copy backend\.env.example backend\.env
    echo ✓ Created backend\.env
    echo   ⚠️  Please update sensitive values in backend\.env
) else (
    echo ✓ backend\.env already exists
)

echo.
echo Step 2: Building Docker images
docker-compose build
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Failed to build Docker images
    exit /b 1
)
echo ✓ Docker images built

echo.
echo Step 3: Starting services
docker-compose up -d
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Failed to start services
    exit /b 1
)
echo ✓ Services started

echo.
echo Step 4: Running migrations
timeout /t 5 /nobreak
docker-compose exec -T backend python manage.py migrate
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Failed to run migrations
    exit /b 1
)
echo ✓ Migrations complete

echo.
echo Step 5: Creating superuser
echo Please enter superuser credentials:
docker-compose exec backend python manage.py createsuperuser
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Failed to create superuser
    exit /b 1
)
echo ✓ Superuser created

echo.
echo ✅ Setup complete!
echo.
echo 📍 Access your application:
echo    Frontend:  http://localhost:3000
echo    Admin:     http://localhost:8000/admin
echo    API:       http://localhost:8000/api
echo.
echo 📚 Next steps:
echo    1. Log in to admin panel at http://localhost:8000/admin
echo    2. Create a Lesson
echo    3. Create a Test in that lesson
echo    4. Add Questions with Answers
echo    5. Visit http://localhost:3000 to try the test
echo.
echo 📖 For more information, see README.md and DEVELOPMENT.md
echo.
