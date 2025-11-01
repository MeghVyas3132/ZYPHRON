"""
Language and framework detection service
Analyzes repository to detect programming languages, frameworks, and dependencies
"""

import os
import json
import re
from typing import Dict, List, Tuple, Optional
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class LanguageDetector:
    """Detect programming languages and frameworks in a repository"""
    
    # File patterns for language detection
    LANGUAGE_PATTERNS = {
        "Python": [r"\.py$", r"requirements\.txt$", r"setup\.py$", r"Pipfile$", r"pyproject\.toml$"],
        "JavaScript": [r"\.js$", r"\.jsx$", r"package\.json$"],
        "TypeScript": [r"\.ts$", r"\.tsx$", r"tsconfig\.json$"],
        "Java": [r"\.java$", r"pom\.xml$", r"build\.gradle$"],
        "Go": [r"\.go$", r"go\.mod$", r"go\.sum$"],
        "Rust": [r"\.rs$", r"Cargo\.toml$", r"Cargo\.lock$"],
        "Ruby": [r"\.rb$", r"Gemfile$", r"Rakefile$"],
        "PHP": [r"\.php$", r"composer\.json$"],
        "C#": [r"\.cs$", r"\.csproj$", r"\.sln$"],
        "C++": [r"\.cpp$", r"\.cc$", r"\.cxx$", r"CMakeLists\.txt$"],
        "Dockerfile": [r"Dockerfile$", r"docker-compose\.yml$"],
    }
    
    # Framework detection patterns
    FRAMEWORK_PATTERNS = {
        "Frontend": {
            "React": [r"react", r"\.jsx?$", r"components/"],
            "Vue": [r"vue", r"\.vue$"],
            "Angular": [r"@angular"],
            "Next.js": [r"next", r"pages/"],
            "Nuxt": [r"nuxt"],
            "Svelte": [r"svelte"],
        },
        "Backend": {
            "FastAPI": [r"fastapi", r"from fastapi"],
            "Django": [r"django", r"manage\.py"],
            "Flask": [r"flask"],
            "Express": [r"express"],
            "NestJS": [r"@nestjs"],
            "Spring": [r"spring"],
            "Laravel": [r"laravel"],
            "Rails": [r"rails"],
        },
        "Database": {
            "PostgreSQL": [r"psycopg", r"postgres", r"pg"],
            "MySQL": [r"mysql", r"mariadb"],
            "MongoDB": [r"mongodb", r"mongoose"],
            "Redis": [r"redis"],
            "SQLite": [r"sqlite"],
        }
    }
    
    @staticmethod
    def detect_languages(repo_path: str) -> Dict[str, List[str]]:
        """
        Detect all languages in a repository
        Returns: {"Python": ["requirements.txt", "setup.py"], ...}
        """
        detected = {}
        
        try:
            for root, dirs, files in os.walk(repo_path):
                # Skip hidden and common non-essential directories
                dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', 'venv']]
                
                for file in files:
                    for language, patterns in LanguageDetector.LANGUAGE_PATTERNS.items():
                        for pattern in patterns:
                            if re.search(pattern, file, re.IGNORECASE):
                                if language not in detected:
                                    detected[language] = []
                                detected[language].append(os.path.join(root, file))
        except Exception as e:
            logger.error(f"Error detecting languages: {str(e)}")
        
        return detected
    
    @staticmethod
    def detect_frameworks(repo_path: str, detected_languages: Dict) -> Dict[str, List[str]]:
        """
        Detect frameworks based on detected languages and dependencies
        """
        frameworks = {
            "Frontend": [],
            "Backend": [],
            "Database": []
        }
        
        try:
            # Check package.json for JavaScript/TypeScript
            package_json_path = os.path.join(repo_path, "package.json")
            if os.path.exists(package_json_path):
                with open(package_json_path, 'r') as f:
                    package_data = json.load(f)
                    deps = {**package_data.get("dependencies", {}), **package_data.get("devDependencies", {})}
                    
                    for category, fw_patterns in LanguageDetector.FRAMEWORK_PATTERNS.items():
                        for framework, patterns in fw_patterns.items():
                            for pattern in patterns:
                                if any(re.search(pattern, dep, re.IGNORECASE) for dep in deps.keys()):
                                    if framework not in frameworks[category]:
                                        frameworks[category].append(framework)
            
            # Check requirements.txt for Python
            requirements_path = os.path.join(repo_path, "requirements.txt")
            if os.path.exists(requirements_path):
                with open(requirements_path, 'r') as f:
                    requirements = f.read()
                    
                    for category, fw_patterns in LanguageDetector.FRAMEWORK_PATTERNS.items():
                        for framework, patterns in fw_patterns.items():
                            for pattern in patterns:
                                if re.search(pattern, requirements, re.IGNORECASE):
                                    if framework not in frameworks[category]:
                                        frameworks[category].append(framework)
            
            # Check Gemfile for Ruby
            gemfile_path = os.path.join(repo_path, "Gemfile")
            if os.path.exists(gemfile_path):
                with open(gemfile_path, 'r') as f:
                    gemfile = f.read()
                    
                    if "rails" in gemfile.lower():
                        if "Rails" not in frameworks["Backend"]:
                            frameworks["Backend"].append("Rails")
        
        except Exception as e:
            logger.error(f"Error detecting frameworks: {str(e)}")
        
        return frameworks
    
    @staticmethod
    def detect_env_variables(repo_path: str) -> List[str]:
        """
        Detect required environment variables by scanning config files
        """
        env_vars = set()
        env_patterns = [
            r"process\.env\.([A-Z_]+)",  # Node.js
            r"os\.getenv\(['\"]([A-Z_]+)['\"]",  # Python
            r"\$ENV\{([A-Z_]+)\}",  # General
            r"ENV\[([A-Z_]+)\]",  # Ruby
        ]
        
        try:
            for root, dirs, files in os.walk(repo_path):
                dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__']]
                
                for file in files:
                    if file.endswith(('.js', '.py', '.rb', '.go', '.rs', '.tsx', '.ts')):
                        try:
                            with open(os.path.join(root, file), 'r', encoding='utf-8', errors='ignore') as f:
                                content = f.read()
                                for pattern in env_patterns:
                                    matches = re.findall(pattern, content)
                                    env_vars.update(matches)
                        except Exception as e:
                            logger.debug(f"Error reading file {file}: {str(e)}")
        
        except Exception as e:
            logger.error(f"Error detecting environment variables: {str(e)}")
        
        return sorted(list(env_vars))


# Example usage
if __name__ == "__main__":
    repo_path = "/path/to/repo"
    detector = LanguageDetector()
    
    languages = detector.detect_languages(repo_path)
    frameworks = detector.detect_frameworks(repo_path, languages)
    env_vars = detector.detect_env_variables(repo_path)
    
    print(f"Languages: {languages}")
    print(f"Frameworks: {frameworks}")
    print(f"Environment Variables: {env_vars}")
