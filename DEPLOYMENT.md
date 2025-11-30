# FastFoodie Backend - Deployment Guide

## Quick Start with Docker Compose

The easiest way to run the entire stack (API + MySQL + Redis):

### 1. Set Environment Variables

Create a `.env` file in the project root:

```env
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_REGION=us-east-1
S3_BUCKET_NAME=fastfoodie-uploads
```

### 2. Start All Services

```bash
docker-compose up -d
```

This will start:
- MySQL database on port 3306
- Redis on port 6379
- FastAPI application on port 8000

### 3. Check Service Status

```bash
docker-compose ps
```

### 4. View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f api
```

### 5. Stop Services

```bash
docker-compose down
```

### 6. Stop and Remove Volumes

```bash
docker-compose down -v
```

## Manual Deployment

### Prerequisites

- Python 3.9+
- MySQL 8.0+
- Redis (optional)

### Steps

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Setup Database**
   ```bash
   mysql -u root -p < database_schema.sql
   ```

3. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

4. **Run Migrations**
   ```bash
   python migrate.py
   ```

5. **Start Application**
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

## Production Deployment

### Using Gunicorn

```bash
pip install gunicorn
gunicorn app.main:app \
  -w 4 \
  -k uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --access-logfile - \
  --error-logfile -
```

### Using Systemd Service

Create `/etc/systemd/system/fastfoodie.service`:

```ini
[Unit]
Description=FastFoodie API
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/fastfoodie-backend
Environment="PATH=/var/www/fastfoodie-backend/venv/bin"
ExecStart=/var/www/fastfoodie-backend/venv/bin/gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl enable fastfoodie
sudo systemctl start fastfoodie
sudo systemctl status fastfoodie
```

### Nginx Configuration

Create `/etc/nginx/sites-available/fastfoodie`:

```nginx
server {
    listen 80;
    server_name api.fastfoodie.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /orders/live {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Enable site:

```bash
sudo ln -s /etc/nginx/sites-available/fastfoodie /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## AWS Deployment

### Using EC2

1. Launch EC2 instance (Ubuntu 22.04)
2. Install Docker and Docker Compose
3. Clone repository
4. Configure environment variables
5. Run `docker-compose up -d`

### Using ECS (Elastic Container Service)

1. Build and push Docker image to ECR
2. Create ECS task definition
3. Create ECS service
4. Configure load balancer
5. Set up RDS for MySQL
6. Set up ElastiCache for Redis

### Using Elastic Beanstalk

1. Install EB CLI
2. Initialize: `eb init`
3. Create environment: `eb create fastfoodie-api`
4. Deploy: `eb deploy`

## Database Backup

### Manual Backup

```bash
docker-compose exec mysql mysqldump -u root -p fastfoodie > backup.sql
```

### Automated Backup Script

Create `backup.sh`:

```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups"
docker-compose exec -T mysql mysqldump -u root -prootpassword fastfoodie > $BACKUP_DIR/fastfoodie_$DATE.sql
find $BACKUP_DIR -name "fastfoodie_*.sql" -mtime +7 -delete
```

Add to crontab:

```bash
0 2 * * * /path/to/backup.sh
```

## Monitoring

### Health Check Endpoint

```bash
curl http://localhost:8000/health
```

### Application Logs

```bash
# Docker
docker-compose logs -f api

# Systemd
sudo journalctl -u fastfoodie -f
```

### Database Monitoring

```bash
docker-compose exec mysql mysql -u root -p -e "SHOW PROCESSLIST;"
```

## Scaling

### Horizontal Scaling

1. Use load balancer (Nginx, AWS ALB)
2. Run multiple API instances
3. Share Redis for WebSocket pub/sub
4. Use managed database (RDS)

### Vertical Scaling

Increase resources in docker-compose.yml:

```yaml
api:
  deploy:
    resources:
      limits:
        cpus: '2'
        memory: 4G
```

## Security Checklist

- [ ] Change default SECRET_KEY
- [ ] Use strong database passwords
- [ ] Enable HTTPS/SSL
- [ ] Restrict CORS origins
- [ ] Set up firewall rules
- [ ] Enable database encryption
- [ ] Use AWS IAM roles for S3
- [ ] Implement rate limiting
- [ ] Enable API authentication
- [ ] Regular security updates

## Troubleshooting

### Database Connection Issues

```bash
# Check MySQL is running
docker-compose ps mysql

# Check connection
docker-compose exec mysql mysql -u root -p -e "SELECT 1;"
```

### API Not Starting

```bash
# Check logs
docker-compose logs api

# Restart service
docker-compose restart api
```

### WebSocket Connection Issues

```bash
# Check Redis
docker-compose exec redis redis-cli ping

# Test WebSocket
wscat -c "ws://localhost:8000/orders/live?token=YOUR_TOKEN"
```

## Performance Optimization

1. **Database Indexing**: Already configured in schema
2. **Connection Pooling**: Configured in SQLAlchemy
3. **Caching**: Use Redis for frequently accessed data
4. **CDN**: Use CloudFront for S3 assets
5. **Database Read Replicas**: For high read loads

## Support

For deployment issues, check:
- Application logs
- Database logs
- System resources (CPU, Memory, Disk)
- Network connectivity
