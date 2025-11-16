#!/bin/bash
# Stop all services
docker-compose down

# Remove Docker volumes (WARNING: this deletes the database!)
# Uncomment the line below if you want to reset everything
# docker-compose down -v

echo "Services stopped."
echo "To remove all data (including database), run: docker-compose down -v"
