# Jenkins CI/CD Setup for Fuel Cost Calculator

This project now includes Jenkins CI/CD pipeline setup with Docker integration.

## Quick Start

### 1. Start Jenkins
```bash
docker-compose up -d jenkins
```

### 2. Access Jenkins
- Open http://localhost:8090
- Get initial admin password:
```bash
docker exec jenkins-controller cat /var/jenkins_home/secrets/initialAdminPassword
```

### 3. Setup Jenkins
1. Install suggested plugins
2. Create admin user
3. Install additional plugins:
   - Docker Pipeline
   - Git plugin
   - Pipeline plugin

### 4. Create Pipeline Job
1. New Item → Pipeline
2. Pipeline → Pipeline script from SCM
3. SCM: Git
4. Repository URL: your git repo
5. Script Path: Jenkinsfile

## Pipeline Stages

The Jenkinsfile includes these stages:
1. **Checkout** - Gets source code
2. **Install Dependencies** - Sets up Python environment
3. **Lint & Test** - Code quality checks (add your tools)
4. **Security Scan** - Dependency vulnerability scan
5. **Build Docker Image** - Creates container image
6. **Test Docker Image** - Basic container testing
7. **Push to Registry** - Pushes image (main branch only)
8. **Deploy** - Deploys using docker-compose (main branch only)

## Customization

### Add Tests
Uncomment and modify in Jenkinsfile:
```bash
# python -m pytest tests/
```

### Add Linting
Uncomment and modify in Jenkinsfile:
```bash
# python -m flake8 app.py
```

### Configure Registry
Update `DOCKER_REGISTRY` environment variable in Jenkinsfile and uncomment push commands.

## Commands

```bash
# Start everything
docker-compose up -d

# Start only app
docker-compose up -d fuel-calculator

# Start only Jenkins
docker-compose up -d jenkins

# View logs
docker-compose logs -f jenkins

# Stop all
docker-compose down
```

## URLs
- App: http://localhost:8080
- Jenkins: http://localhost:8090

## Notes
- Jenkins runs as root to access Docker socket
- Persistent data stored in `jenkins_home` volume
- Pipeline automatically deploys on main branch
- Security scan uses `safety` to check dependencies