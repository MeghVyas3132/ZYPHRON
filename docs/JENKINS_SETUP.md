# Jenkins CI/CD Pipeline Setup for Zyphron

## 📋 Overview

Jenkins is now integrated with Zyphron to automate deployment of registered repositories. When a new deployment is created via the API, Jenkins automatically clones the repository, detects the project type, builds a Docker image, and deploys it.

## 🚀 Quick Start

### 1. Access Jenkins Dashboard
- **URL**: http://localhost:8080
- **Initial Admin Password**: Check below

### 2. Get Initial Admin Password

```bash
docker exec zyphron_jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

Then:
1. Paste the password in the Jenkins dashboard
2. Click "Continue"
3. Click "Install suggested plugins"
4. Create your first admin user

### 3. Create Jenkins Job

Once logged in:

1. Click **"New Item"** (top left)
2. Enter job name: `zyphron-deploy`
3. Select **"Pipeline"**
4. Click **"OK"**

### 4. Configure Pipeline

In the **Pipeline** section:

#### Option A: Pipeline script from SCM (Recommended)
1. Select **"Pipeline script from SCM"**
2. Choose **Git**
3. Repository URL: `https://github.com/MeghVyas3132/ZYPHRON.git`
4. Branch: `*/main`
5. Script Path: `Jenkinsfile`

#### Option B: Paste Pipeline Script Directly
1. Select **"Pipeline script"**
2. Copy and paste the content from `Jenkinsfile` in the root directory
3. Click **Save**

### 5. Install Required Plugins

Go to **Manage Jenkins** → **Manage Plugins** → **Available** and install:

- **Docker Pipeline**
- **Git**
- **GitHub Integration**
- **Pipeline: AWS Steps** (if using AWS)
- **HTTP Request Plugin**

## 🔧 How It Works

### Deployment Flow

```
1. User creates deployment via API
   ↓
2. Backend triggers Jenkins pipeline
   ↓
3. Jenkins clones repository
   ↓
4. Detects project type (Node.js, Python, Go, Ruby, etc.)
   ↓
5. Generates Dockerfile if not exists
   ↓
6. Builds Docker image
   ↓
7. Stops previous container
   ↓
8. Starts new container
   ↓
9. Health checks pass
   ↓
10. Updates deployment status in backend
```

### API Flow

**Create Deployment** (Triggers Pipeline)
```bash
curl -X POST http://localhost:8000/api/v1/deployments \
  -H "Content-Type: application/json" \
  -d '{
    "project_name": "My App",
    "subdomain": "myapp",
    "repo_url": "https://github.com/user/repo",
    "repo_branch": "main",
    "repo_type": "github"
  }'
```

**Update Deployment Status** (Called by Jenkins)
```bash
curl -X POST http://localhost:8000/api/v1/deployments/1/update-status \
  -H "Content-Type: application/json" \
  -G \
  -d "status=deployed" \
  -d "container_id=abc123" \
  -d "container_port=3000"
```

## 📊 Project Type Detection

Jenkins automatically detects:

- **Next.js** - `package.json` with `next` dependency
- **Vue** - `package.json` with `vue` dependency
- **React** - `package.json` with `react` dependency
- **Node.js** - `package.json`
- **Python** - `requirements.txt` or `setup.py`
- **Go** - `go.mod`
- **Ruby** - `Gemfile`
- **Docker** - Existing `Dockerfile`

## 🐳 Container Management

Deployed containers:
- Named: `zyphron-{subdomain}` (e.g., `zyphron-megh1`)
- Network: `zyphron_network`
- Port mapping: Random port on host mapped to 3000 in container

## 📝 Configuration

### Environment Variables

In `docker-compose.yml` backend service:

```yaml
JENKINS_URL: http://zyphron_jenkins:8080
JENKINS_TOKEN: dev-jenkins-token
```

### Security

For production, set proper:
- `JENKINS_TOKEN` - Generate in Jenkins: Manage Jenkins → Security → API Token
- `JENKINS_URL` - Use external domain if Jenkins is publicly accessible
- Configure Jenkins security and authentication

## 🔍 Troubleshooting

### Jenkins not starting
```bash
docker logs zyphron_jenkins
```

### Build failing
1. Check Jenkins console output: Jenkins Dashboard → Job → Build Number → Console Output
2. Check container logs: `docker logs zyphron-{subdomain}`

### Docker-in-Docker issues
Ensure Docker socket is properly mounted:
```bash
docker exec zyphron_jenkins ls -l /var/run/docker.sock
```

### Health check failing
- Check if app is actually running on port 3000
- Check container logs: `docker logs zyphron-{subdomain}`
- Add custom health check endpoint if needed

## 📚 Example Deployments

### Deploy MeghOS Portfolio
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

This will automatically:
1. Trigger Jenkins job
2. Clone repository
3. Detect it's a Next.js app
4. Build and deploy
5. Make it available at `megh1.zyphron.space`

## 🛠️ Advanced Configuration

### Custom Webhook Triggers

Add GitHub webhook to auto-trigger deployments on push:

1. Go to repository Settings → Webhooks
2. Payload URL: `http://your-domain/api/v1/deployments/webhook/github`
3. Content type: `application/json`
4. Events: Push events

### Slack Integration

For Jenkins to notify Slack:

1. Install Slack plugin in Jenkins
2. Configure Slack credentials
3. Add Slack notifications to Jenkinsfile

### Deployment Logs

Logs are stored in:
- Database: `Deployment.deployment_logs`
- Jenkins: Jenkins UI Console Output
- Container: `docker logs zyphron-{subdomain}`

## 🚀 Next Steps

1. Test deploying one of the registered repositories
2. Set up GitHub webhooks for auto-deployment
3. Configure Slack notifications
4. Add rollback functionality
5. Implement database backups
6. Set up monitoring and alerting

