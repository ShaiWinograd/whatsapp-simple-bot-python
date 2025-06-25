# Deployment Guide

This guide covers deploying the WhatsApp bot service to production.

## Prerequisites

- Python 3.7+
- PostgreSQL 12+
- Redis 6+
- WhatsApp Business API credentials
- SSL certificate
- Docker & Docker Compose (optional)

## Environment Setup

1. Create environment file:
```bash
cp .env.template .env
```

2. Configure environment variables:
```env
# WhatsApp Configuration
WHATSAPP_API_TOKEN=your_token_here
WHATSAPP_VERIFY_TOKEN=your_verify_token
WHATSAPP_PHONE_NUMBER_ID=your_phone_number_id

# Label IDs
WHATSAPP_BOT_NEW_CONVERSATION_LABEL_ID=label_id_1
WHATSAPP_URGENT_SUPPORT_LABEL_ID=label_id_2
WHATSAPP_WAITING_CALL_BEFORE_QUOTE_LABEL_ID=label_id_3
WHATSAPP_MOVING_LABEL_ID=label_id_4
WHATSAPP_ORGANIZATION_LABEL_ID=label_id_5

# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/whatsapp_bot

# Redis Configuration
REDIS_URL=redis://localhost:6379/0

# Application Settings
DEBUG=false
LOG_LEVEL=INFO
CONVERSATION_TIMEOUT_MINUTES=300
```

## Database Setup

1. Create database:
```sql
CREATE DATABASE whatsapp_bot;
```

2. Run migrations:
```bash
python manage.py migrate
```

## Docker Deployment

1. Build image:
```bash
docker build -t whatsapp-bot .
```

2. Run with Docker Compose:
```bash
docker-compose up -d
```

Docker Compose configuration (`docker-compose.yml`):
```yaml
version: '3.8'
services:
  app:
    build: .
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/whatsapp_bot
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis
    ports:
      - "8000:8000"

  db:
    image: postgres:12
    environment:
      - POSTGRES_DB=whatsapp_bot
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
    volumes:
      - pgdata:/var/lib/postgresql/data

  redis:
    image: redis:6
    volumes:
      - redisdata:/data

volumes:
  pgdata:
  redisdata:
```

## Manual Deployment

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run application:
```bash
gunicorn app:app --workers 4 --threads 2
```

## Nginx Configuration

```nginx
server {
    listen 443 ssl;
    server_name your-domain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Monitoring Setup

1. Configure logging:
```python
# config/logging.py
LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'app.log',
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 5,
        }
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    }
}
```

2. Set up monitoring:
- Install monitoring agent
- Configure metrics collection
- Set up alerts

## Security Checklist

- [ ] SSL/TLS enabled
- [ ] Environment variables secured
- [ ] Database credentials rotated
- [ ] WhatsApp token secured
- [ ] Rate limiting configured
- [ ] Input validation enabled
- [ ] Error logging configured
- [ ] Backups configured

## Backup Configuration

1. Database backups:
```bash
# /etc/cron.daily/backup-db
pg_dump whatsapp_bot > /backups/whatsapp_bot_$(date +%Y%m%d).sql
```

2. Log rotation:
```
/var/log/whatsapp_bot/*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
}
```

## Scaling Considerations

- Use load balancer for multiple instances
- Configure Redis for session management
- Monitor database connections
- Set up read replicas if needed
- Configure proper caching

## Maintenance

- Monitor disk usage
- Rotate logs
- Update dependencies
- Backup verification
- SSL certificate renewal

## Troubleshooting

1. Check logs:
```bash
tail -f /var/log/whatsapp_bot/app.log
```

2. Check service status:
```bash
systemctl status whatsapp-bot
```

3. Monitor metrics:
```bash
curl localhost:8000/metrics
```

4. Debug mode:
```bash
DEBUG=true python app.py
```

## Recovery Procedures

1. Database restore:
```bash
psql whatsapp_bot < backup.sql
```

2. Service restart:
```bash
systemctl restart whatsapp-bot
```

3. Roll back deployment:
```bash
docker-compose down
docker-compose up -d --build