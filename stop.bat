@echo off
REM Stop all services

docker-compose down

REM Remove Docker volumes (WARNING: this deletes the database!)
REM Uncomment the line below if you want to reset everything
REM docker-compose down -v

echo Services stopped.
echo To remove all data (including database), run: docker-compose down -v
