"""
Nginx configuration management
"""

import logging
import os
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class NginxManager:
    """Manage Nginx configurations for subdomains"""
    
    def __init__(self, config_dir: str = "/etc/nginx/sites-available"):
        self.config_dir = config_dir
    
    def create_subdomain_config(
        self,
        subdomain: str,
        full_domain: str,
        service_name: str,
        service_port: int,
        ssl_cert_path: Optional[str] = None,
        ssl_cert_key_path: Optional[str] = None
    ) -> str:
        """
        Create nginx configuration for a subdomain
        Returns: configuration file path
        """
        try:
            config_file = os.path.join(self.config_dir, subdomain)
            
            # Read template
            template_path = os.path.join(os.path.dirname(__file__), "nginx.template.conf")
            with open(template_path, 'r') as f:
                template = f.read()
            
            # Generate configuration
            config = template.format(
                subdomain=subdomain,
                full_domain=full_domain,
                service_name=service_name,
                service_port=service_port,
                ssl_cert_path=ssl_cert_path or f"/etc/letsencrypt/live/{full_domain}/fullchain.pem",
                ssl_cert_key_path=ssl_cert_key_path or f"/etc/letsencrypt/live/{full_domain}/privkey.pem"
            )
            
            # Write configuration
            with open(config_file, 'w') as f:
                f.write(config)
            
            logger.info(f"Nginx configuration created: {config_file}")
            return config_file
        
        except Exception as e:
            logger.error(f"Failed to create nginx configuration: {str(e)}")
            raise
    
    def enable_config(self, subdomain: str) -> None:
        """Enable nginx configuration (create symlink to sites-enabled)"""
        try:
            import subprocess
            
            config_file = os.path.join(self.config_dir, subdomain)
            enabled_file = os.path.join(self.config_dir.replace("sites-available", "sites-enabled"), subdomain)
            
            # Create symlink
            if not os.path.exists(enabled_file):
                os.symlink(config_file, enabled_file)
            
            # Test and reload nginx
            subprocess.run(["nginx", "-t"], check=True, capture_output=True)
            subprocess.run(["systemctl", "reload", "nginx"], check=True, capture_output=True)
            
            logger.info(f"Nginx configuration enabled for {subdomain}")
        
        except Exception as e:
            logger.error(f"Failed to enable nginx configuration: {str(e)}")
            raise
    
    def disable_config(self, subdomain: str) -> None:
        """Disable nginx configuration"""
        try:
            import subprocess
            
            enabled_file = os.path.join(self.config_dir.replace("sites-available", "sites-enabled"), subdomain)
            
            if os.path.exists(enabled_file):
                os.remove(enabled_file)
            
            # Reload nginx
            subprocess.run(["systemctl", "reload", "nginx"], check=True, capture_output=True)
            
            logger.info(f"Nginx configuration disabled for {subdomain}")
        
        except Exception as e:
            logger.error(f"Failed to disable nginx configuration: {str(e)}")
            raise
