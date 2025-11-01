"""
Docker operations and container management
Building, pushing, and running containers
"""

import docker
import logging
import json
import os
from typing import Dict, List, Optional
from pathlib import Path

logger = logging.getLogger(__name__)


class DockerManager:
    """Manage Docker operations for deployments"""
    
    def __init__(self, docker_socket: str = "unix:///var/run/docker.sock"):
        """Initialize Docker client"""
        try:
            self.client = docker.DockerClient(base_url=docker_socket)
            logger.info("Docker client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Docker client: {str(e)}")
            raise
    
    def build_image(
        self,
        dockerfile_path: str,
        image_name: str,
        image_tag: str = "latest",
        build_args: Optional[Dict] = None
    ) -> str:
        """
        Build a Docker image
        Returns: image ID
        """
        try:
            logger.info(f"Building image {image_name}:{image_tag}")
            
            image, build_logs = self.client.images.build(
                dockerfile=dockerfile_path,
                tag=f"{image_name}:{image_tag}",
                buildargs=build_args or {},
                rm=True,
                quiet=False
            )
            
            for log in build_logs:
                if 'stream' in log:
                    logger.debug(log['stream'].strip())
            
            logger.info(f"Image built successfully: {image.id}")
            return image.id
        
        except Exception as e:
            logger.error(f"Failed to build image: {str(e)}")
            raise
    
    def run_container(
        self,
        image_name: str,
        container_name: str,
        ports: Optional[Dict] = None,
        environment: Optional[Dict] = None,
        volumes: Optional[Dict] = None,
        network: Optional[str] = None,
        restart_policy: Optional[Dict] = None,
        detach: bool = True
    ) -> str:
        """
        Run a Docker container
        Returns: container ID
        """
        try:
            logger.info(f"Running container from image {image_name}")
            
            container = self.client.containers.run(
                image_name,
                name=container_name,
                ports=ports or {},
                environment=environment or {},
                volumes=volumes or {},
                network=network,
                restart_policy=restart_policy or {"Name": "unless-stopped"},
                detach=detach,
                remove=False
            )
            
            logger.info(f"Container started: {container.id}")
            return container.id
        
        except Exception as e:
            logger.error(f"Failed to run container: {str(e)}")
            raise
    
    def run_docker_compose(
        self,
        compose_file: str,
        project_name: str,
        detach: bool = True
    ) -> Dict:
        """
        Run Docker Compose
        Returns: container information
        """
        try:
            import subprocess
            
            logger.info(f"Running docker-compose for {project_name}")
            
            cmd = ["docker-compose", "-f", compose_file, "-p", project_name]
            cmd.extend(["up", "-d"] if detach else ["up"])
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                raise Exception(f"Docker Compose failed: {result.stderr}")
            
            logger.info(f"Docker Compose executed successfully")
            return {"status": "success", "output": result.stdout}
        
        except Exception as e:
            logger.error(f"Failed to run docker-compose: {str(e)}")
            raise
    
    def stop_container(self, container_id: str) -> None:
        """Stop a running container"""
        try:
            container = self.client.containers.get(container_id)
            container.stop()
            logger.info(f"Container stopped: {container_id}")
        except Exception as e:
            logger.error(f"Failed to stop container: {str(e)}")
            raise
    
    def remove_container(self, container_id: str, force: bool = False) -> None:
        """Remove a container"""
        try:
            container = self.client.containers.get(container_id)
            container.remove(force=force)
            logger.info(f"Container removed: {container_id}")
        except Exception as e:
            logger.error(f"Failed to remove container: {str(e)}")
            raise
    
    def get_container_status(self, container_id: str) -> Dict:
        """Get container status and information"""
        try:
            container = self.client.containers.get(container_id)
            stats = container.stats(stream=False)
            
            return {
                "container_id": container.id,
                "name": container.name,
                "status": container.status,
                "state": container.attrs["State"],
                "cpu_usage": stats["cpu_stats"]["cpu_usage"]["total_usage"],
                "memory_usage": stats["memory_stats"]["usage"],
                "memory_limit": stats["memory_stats"]["limit"]
            }
        except Exception as e:
            logger.error(f"Failed to get container status: {str(e)}")
            raise
    
    def get_container_logs(self, container_id: str, tail: int = 100) -> str:
        """Get container logs"""
        try:
            container = self.client.containers.get(container_id)
            logs = container.logs(tail=tail, timestamps=True).decode('utf-8')
            return logs
        except Exception as e:
            logger.error(f"Failed to get container logs: {str(e)}")
            return f"Error retrieving logs: {str(e)}"
    
    def generate_dockerfile(
        self,
        language: str,
        framework: Optional[str] = None,
        port: int = 8000
    ) -> str:
        """
        Generate a Dockerfile based on detected language and framework
        """
        dockerfiles = {
            "Python": {
                "FastAPI": self._generate_fastapi_dockerfile,
                "Django": self._generate_django_dockerfile,
                "Flask": self._generate_flask_dockerfile,
            },
            "JavaScript": {
                "Next.js": self._generate_nextjs_dockerfile,
                "React": self._generate_react_dockerfile,
                "Express": self._generate_express_dockerfile,
            },
            "TypeScript": {
                "Next.js": self._generate_nextjs_dockerfile,
                "NestJS": self._generate_nestjs_dockerfile,
            }
        }
        
        generator = dockerfiles.get(language, {}).get(framework)
        
        if generator:
            return generator(port)
        else:
            logger.warning(f"No Dockerfile template for {language}/{framework}, using generic")
            return self._generate_generic_dockerfile(language, port)
    
    @staticmethod
    def _generate_fastapi_dockerfile(port: int = 8000) -> str:
        """FastAPI Dockerfile template"""
        return f"""FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \\
    gcc && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE {port}

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "{port}"]
"""
    
    @staticmethod
    def _generate_nextjs_dockerfile(port: int = 3000) -> str:
        """Next.js Dockerfile template"""
        return f"""FROM node:18-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

FROM node:18-alpine

WORKDIR /app

COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/package*.json ./
COPY public ./public

EXPOSE {port}

CMD ["npm", "start"]
"""
    
    @staticmethod
    def _generate_react_dockerfile(port: int = 3000) -> str:
        """React Dockerfile template"""
        return f"""FROM node:18-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

FROM nginx:alpine

COPY --from=builder /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE {port}

CMD ["nginx", "-g", "daemon off;"]
"""
    
    @staticmethod
    def _generate_express_dockerfile(port: int = 3000) -> str:
        """Express Dockerfile template"""
        return f"""FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install --production

COPY . .

EXPOSE {port}

CMD ["node", "server.js"]
"""
    
    @staticmethod
    def _generate_django_dockerfile(port: int = 8000) -> str:
        """Django Dockerfile template"""
        return f"""FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \\
    gcc postgresql-client && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE {port}

CMD ["gunicorn", "--bind", "0.0.0.0:{port}", "config.wsgi:application"]
"""
    
    @staticmethod
    def _generate_flask_dockerfile(port: int = 5000) -> str:
        """Flask Dockerfile template"""
        return f"""FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \\
    gcc && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE {port}

CMD ["gunicorn", "--bind", "0.0.0.0:{port}", "app:app"]
"""
    
    @staticmethod
    def _generate_nestjs_dockerfile(port: int = 3000) -> str:
        """NestJS Dockerfile template"""
        return f"""FROM node:18-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

FROM node:18-alpine

WORKDIR /app

COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package*.json ./

EXPOSE {port}

CMD ["node", "dist/main"]
"""
    
    @staticmethod
    def _generate_generic_dockerfile(language: str, port: int = 8000) -> str:
        """Generic Dockerfile template"""
        return f"""FROM ubuntu:22.04

WORKDIR /app

COPY . .

EXPOSE {port}

CMD ["echo", "Please provide a valid Dockerfile"]
"""
