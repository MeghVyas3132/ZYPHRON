# 🚀 Zyphron CI/CD Pipeline - Quick Reference

## Current Status

✅ **All infrastructure is ready!**

- Backend API: http://localhost:8000
- Frontend: http://localhost:3000
- Jenkins: http://localhost:8080
- Database: PostgreSQL (port 5432)
- Redis: (port 6379)

## 🎯 What's Ready to Deploy

Three repositories registered and waiting to be deployed:

1. **megh1** → MeghOS-Portfolio
2. **megh2** → test-express-api  
3. **megh3** → test-vue-app

## 🚀 Quick Start (5 Steps)

### Step 1: Get Jenkins Admin Password
```bash
docker exec zyphron_jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

### Step 2: Access Jenkins
Visit: http://localhost:8080

Paste the password above and create admin account

### Step 3: Install Plugins
- Manage Jenkins → Manage Plugins
- Install: Docker Pipeline, Git, GitHub Integration, HTTP Request Plugin

### Step 4: Create Pipeline Job
1. New Item → Name: `zyphron-deploy` → Pipeline
2. Pipeline section:
   - Pipeline script from SCM
   - Git: https://github.com/MeghVyas3132/ZYPHRON.git
   - Branch: */main
   - Script Path: Jenkinsfile
3. Save

### Step 5: Deploy!
```bash
# Deploy test-vue-app to megh3.zyphron.space
curl -X POST http://localhost:8000/api/v1/deployments \
  -H "Content-Type: application/json" \
  -d '{
    "project_name": "Test Vue App",
    "subdomain": "megh3",
    "repo_url": "https://github.com/MeghVyas3132/test-vue-app",
    "repo_branch": "main",
    "repo_type": "github"
  }'
```

## 📊 Pipeline Capabilities

Once set up, Jenkins will automatically:

✅ Clone GitHub repositories
✅ Detect project type (Node/Vue/React/Python/Go/Ruby)
✅ Build Docker containers
✅ Run health checks
✅ Deploy to infrastructure
✅ Update database with status
✅ Make apps available at subdomains

## 🔍 Monitor Progress

### Check Jenkins Build
Visit: http://localhost:8080/job/zyphron-deploy/

### View Deployments
```bash
curl http://localhost:8000/api/v1/deployments | jq
```

### Check Running Containers
```bash
docker ps
```

### View Container Logs
```bash
docker logs zyphron-megh3
```

## 📚 Files Reference

| File | Purpose |
|------|---------|
| `Jenkinsfile` | Pipeline definition |
| `docker-compose.yml` | Infrastructure setup |
| `docs/JENKINS_SETUP.md` | Detailed Jenkins config |
| `PIPELINE_SETUP.md` | Complete setup guide |
| `backend/app/api/v1/routers/deployments.py` | Deployment API |

## 🎯 Expected Flow

```
1. User creates deployment via API
   ↓
2. Backend sends HTTP request to Jenkins
   ↓
3. Jenkins clones repository
   ↓
4. Detects project type (e.g., Vue)
   ↓
5. Generates Dockerfile if needed
   ↓
6. Builds Docker image
   ↓
7. Starts container in Docker
   ↓
8. Runs health checks
   ↓
9. Sends status update back to backend
   ↓
10. Frontend shows deployment as active
    ↓
11. App accessible at subdomain (megh3.zyphron.space)
```

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Jenkins won't start | `docker logs zyphron_jenkins` |
| Build fails | Check Jenkins console output |
| Can't reach app | `docker logs zyphron-megh3` |
| Docker socket error | Verify `/var/run/docker.sock` mounted |

## 📋 Deployment Examples

### Example 1: Node.js App
```bash
curl -X POST http://localhost:8000/api/v1/deployments \
  -H "Content-Type: application/json" \
  -d '{
    "project_name": "Express API",
    "subdomain": "megh2",
    "repo_url": "https://github.com/MeghVyas3132/test-express-api",
    "repo_branch": "main",
    "repo_type": "github"
  }'
```

### Example 2: Next.js App
```bash
curl -X POST http://localhost:8000/api/v1/deployments \
  -H "Content-Type: application/json" \
  -d '{
    "project_name": "MeghOS Portfolio",
    "subdomain": "megh1",
    "repo_url": "https://github.com/MeghVyas3132/MeghOS-Portfolio",
    "repo_branch": "main",
    "repo_type": "github"
  }'
```

## ✅ Success Checklist

- [ ] Jenkins running at http://localhost:8080
- [ ] Admin account created in Jenkins
- [ ] Required plugins installed
- [ ] `zyphron-deploy` pipeline job created
- [ ] Can see job in Jenkins dashboard
- [ ] Deployment triggers Jenkins build
- [ ] Container appears in `docker ps`
- [ ] Health checks pass
- [ ] App accessible at subdomain

## 🎊 You're All Set!

The infrastructure is complete. Time to deploy! 🚀

Questions? Check `PIPELINE_SETUP.md` and `docs/JENKINS_SETUP.md`
