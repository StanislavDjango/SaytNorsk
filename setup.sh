#!/bin/bash
# SaytNorsk Setup Script

set -e

echo "🚀 SaytNorsk Setup Script"
echo "========================="
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

echo -e "${BLUE}Step 1: Creating environment file${NC}"
if [ ! -f "backend/.env" ]; then
    cp backend/.env.example backend/.env
    echo -e "${GREEN}✓ Created backend/.env${NC}"
    echo "  ⚠️  Please update sensitive values in backend/.env"
else
    echo -e "${GREEN}✓ backend/.env already exists${NC}"
fi

echo ""
echo -e "${BLUE}Step 2: Building Docker images${NC}"
docker-compose build
echo -e "${GREEN}✓ Docker images built${NC}"

echo ""
echo -e "${BLUE}Step 3: Starting services${NC}"
docker-compose up -d
echo -e "${GREEN}✓ Services started${NC}"

echo ""
echo -e "${BLUE}Step 4: Running migrations${NC}"
sleep 5  # Wait for database to be ready
docker-compose exec -T backend python manage.py migrate
echo -e "${GREEN}✓ Migrations complete${NC}"

echo ""
echo -e "${BLUE}Step 5: Creating superuser${NC}"
echo "Please enter superuser credentials:"
docker-compose exec backend python manage.py createsuperuser
echo -e "${GREEN}✓ Superuser created${NC}"

echo ""
echo -e "${GREEN}✅ Setup complete!${NC}"
echo ""
echo "📍 Access your application:"
echo "   Frontend:  http://localhost:3000"
echo "   Admin:     http://localhost:8000/admin"
echo "   API:       http://localhost:8000/api"
echo ""
echo "📚 Next steps:"
echo "   1. Log in to admin panel at http://localhost:8000/admin"
echo "   2. Create a Lesson"
echo "   3. Create a Test in that lesson"
echo "   4. Add Questions with Answers"
echo "   5. Visit http://localhost:3000 to try the test"
echo ""
echo "📖 For more information, see README.md and DEVELOPMENT.md"
echo ""
