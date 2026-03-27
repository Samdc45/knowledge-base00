# NZCI Knowledge Base

Production-ready LMS for New Zealand civil engineering training.

## Quick Start

```bash
# Local
python app.py

# Docker
docker build -t south-lms .
docker run -p 6000:6000 south-lms

# Railway
git push origin main
```

## API Endpoints

```bash
# Health
curl https://south-lms-production.up.railway.app/health

# Get courses
curl -H "X-API-Key: YOUR_KEY" https://south-lms-production.up.railway.app/api/courses

# Get specific course
curl -H "X-API-Key: YOUR_KEY" https://south-lms-production.up.railway.app/api/courses/nzci_flexi

# Get modules
curl -H "X-API-Key: YOUR_KEY" https://south-lms-production.up.railway.app/api/courses/nzci_health_safety/modules
```

## Courses

- **nzci_flexi** - Flexitime Construction (beginner, 12 weeks)
- **nzci_advanced** - Advanced Construction Management (advanced, 16 weeks)
- **nzci_health_safety** - Health & Safety Excellence (intermediate, 8 weeks)
- **nzci_infrastructure** - Infrastructure & Transportation (intermediate, 14 weeks)

## Environment Variables

- `PORT` (default: 6000)
- `API_KEY` (optional, for authentication)
- `FLASK_ENV` (production/development)

## License

MIT
