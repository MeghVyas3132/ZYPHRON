pipeline {
    agent any
    
    options {
        timestamps()
        timeout(time: 1, unit: 'HOURS')
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }
    
    parameters {
        string(name: 'DEPLOYMENT_ID', description: 'Deployment ID from Zyphron')
        string(name: 'REPO_URL', description: 'Repository URL')
        string(name: 'REPO_BRANCH', description: 'Repository Branch', defaultValue: 'main')
        string(name: 'PROJECT_NAME', description: 'Project Name')
        string(name: 'SUBDOMAIN', description: 'Subdomain for deployment')
        string(name: 'REPO_TYPE', description: 'Repository Type (github, gitlab, etc)', defaultValue: 'github')
    }
    
    environment {
        REGISTRY = 'localhost:5000'
        IMAGE_NAME = "${REGISTRY}/zyphron/${params.PROJECT_NAME.toLowerCase().replaceAll(' ', '-')}"
        IMAGE_TAG = "${params.SUBDOMAIN}-${BUILD_NUMBER}"
        CONTAINER_NAME = "zyphron-${params.SUBDOMAIN}"
        DOCKER_SOCKET = '/var/run/docker.sock'
    }
    
    stages {
        stage('Checkout') {
            steps {
                script {
                    echo "🔄 Cloning repository: ${params.REPO_URL}"
                    checkout scm: [
                        $class: 'GitSCM',
                        branches: [[name: "*/${params.REPO_BRANCH}"]],
                        userRemoteConfigs: [[url: "${params.REPO_URL}"]]
                    ], poll: false
                }
            }
        }
        
        stage('Detect Project Type') {
            steps {
                script {
                    echo "🔍 Detecting project type..."
                    
                    def projectType = 'unknown'
                    if (fileExists('package.json')) {
                        def packageJson = readJSON file: 'package.json'
                        if (packageJson.devDependencies?.next || packageJson.dependencies?.next) {
                            projectType = 'next-js'
                        } else if (packageJson.devDependencies?.vue || packageJson.dependencies?.vue) {
                            projectType = 'vue'
                        } else if (packageJson.devDependencies?.react || packageJson.dependencies?.react) {
                            projectType = 'react'
                        } else {
                            projectType = 'node'
                        }
                    } else if (fileExists('requirements.txt') || fileExists('setup.py')) {
                        projectType = 'python'
                    } else if (fileExists('go.mod')) {
                        projectType = 'golang'
                    } else if (fileExists('Gemfile')) {
                        projectType = 'ruby'
                    } else if (fileExists('Dockerfile')) {
                        projectType = 'dockerfile'
                    }
                    
                    env.PROJECT_TYPE = projectType
                    echo "✅ Detected project type: ${projectType}"
                }
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    echo "🐳 Building Docker image: ${IMAGE_NAME}:${IMAGE_TAG}"
                    
                    // Create Dockerfile if it doesn't exist
                    if (!fileExists('Dockerfile')) {
                        sh 'cat > Dockerfile << EOF\n' + generateDockerfile() + '\nEOF'
                    }
                    
                    sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} -t ${IMAGE_NAME}:latest ."
                }
            }
        }
        
        stage('Stop Previous Container') {
            steps {
                script {
                    echo "🛑 Stopping previous container (if exists)..."
                    sh """
                        if docker ps -a --format '{{.Names}}' | grep -q '^${CONTAINER_NAME}$'; then
                            docker stop ${CONTAINER_NAME} || true
                            docker rm ${CONTAINER_NAME} || true
                        fi
                    """
                }
            }
        }
        
        stage('Run Container') {
            steps {
                script {
                    echo "🚀 Starting container: ${CONTAINER_NAME}"
                    
                    sh """
                        docker run -d \
                            --name ${CONTAINER_NAME} \
                            --network zyphron_network \
                            -e DEPLOYMENT_ID=${params.DEPLOYMENT_ID} \
                            -e SUBDOMAIN=${params.SUBDOMAIN} \
                            -p 0:3000 \
                            ${IMAGE_NAME}:${IMAGE_TAG}
                    """
                    
                    // Get the port mapping
                    sleep(time: 3, unit: 'SECONDS')
                    def portMapping = sh(
                        script: "docker port ${CONTAINER_NAME} 3000/tcp | cut -d: -f2",
                        returnStdout: true
                    ).trim()
                    
                    env.CONTAINER_PORT = portMapping
                    echo "✅ Container running on port: ${portMapping}"
                }
            }
        }
        
        stage('Health Check') {
            steps {
                script {
                    echo "💚 Running health checks..."
                    retry(5) {
                        sleep(time: 2, unit: 'SECONDS')
                        sh """
                            curl -f http://localhost:${CONTAINER_PORT}/ || exit 1
                        """
                    }
                    echo "✅ Health checks passed!"
                }
            }
        }
        
        stage('Update Deployment Status') {
            steps {
                script {
                    echo "📝 Updating deployment status in Zyphron backend..."
                    sh """
                        curl -X POST http://zyphron_backend:8000/api/v1/deployments/${params.DEPLOYMENT_ID}/update-status \
                            -H "Content-Type: application/json" \
                            -d '{
                                "status": "deployed",
                                "container_id": "'$(docker inspect -f '{{.ID}}' ${CONTAINER_NAME})'",
                                "container_port": '${CONTAINER_PORT}',
                                "deployed_at": "'$(date -u +%Y-%m-%dT%H:%M:%S)'",
                                "deployment_logs": "Deployed successfully"
                            }' || true
                    """
                }
            }
        }
    }
    
    post {
        always {
            cleanWs()
            echo "🧹 Workspace cleaned"
        }
        success {
            script {
                echo "✅ Deployment successful: ${params.SUBDOMAIN}.zyphron.space"
            }
        }
        failure {
            script {
                echo "❌ Deployment failed for ${params.SUBDOMAIN}"
                sh """
                    curl -X POST http://zyphron_backend:8000/api/v1/deployments/${params.DEPLOYMENT_ID}/update-status \
                        -H "Content-Type: application/json" \
                        -d '{
                            "status": "failed",
                            "error_logs": "Build or deployment failed"
                        }' || true
                """
            }
        }
    }
}

def generateDockerfile() {
    def dockerfile = ''
    
    if (env.PROJECT_TYPE == 'node' || env.PROJECT_TYPE == 'next-js' || env.PROJECT_TYPE == 'react' || env.PROJECT_TYPE == 'vue') {
        dockerfile = '''FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build || true
EXPOSE 3000
CMD ["npm", "start"]'''
    } else if (env.PROJECT_TYPE == 'python') {
        dockerfile = '''FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]'''
    } else if (env.PROJECT_TYPE == 'golang') {
        dockerfile = '''FROM golang:1.21-alpine as builder
WORKDIR /app
COPY . .
RUN go build -o app .

FROM alpine:latest
WORKDIR /app
COPY --from=builder /app/app .
EXPOSE 8080
CMD ["./app"]'''
    } else {
        dockerfile = '''FROM alpine:latest
WORKDIR /app
COPY . .
EXPOSE 3000
CMD ["/bin/sh"]'''
    }
    
    return dockerfile
}
