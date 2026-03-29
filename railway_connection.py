"""
Railway Connection Code for Agent Zero
Integrates LMS, Agent Zero, and Railway deployment
"""

import os
import requests
from typing import Dict, Optional
from dataclasses import dataclass
from enum import Enum

class RailwayEnvironment(Enum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"

@dataclass
class RailwayConfig:
    """Railway configuration for Agent Zero deployment"""
    railway_token: str
    project_id: str
    service_name: str
    environment: RailwayEnvironment
    region: str = "us-west"
    
    # Agent Zero Requirements
    openrouter_api_key: Optional[str] = None
    lms_url: str = "http://south-lms:6000"
    
    # Resource limits
    memory_mb: int = 2048
    cpu_millicores: int = 1000

class RailwayConnection:
    """Connection handler for Railway API and Agent Zero deployment"""
    
    BASE_URL = "https://api.railway.app/graphql"
    
    def __init__(self, config: RailwayConfig):
        self.config = config
        self.headers = {
            "Authorization": f"Bearer {config.railway_token}",
            "Content-Type": "application/json"
        }
    
    def get_project(self) -> Dict:
        """Get Railway project details"""
        query = """
        query {
            project(id: "%s") {
                id
                name
                createdAt
                updatedAt
            }
        }
        """ % self.config.project_id
        
        return self._execute_query(query)
    
    def get_deployments(self) -> Dict:
        """Get project deployments"""
        query = """
        query {
            deployments(projectId: "%s", first: 10) {
                edges {
                    node {
                        id
                        status
                        createdAt
                        updatedAt
                    }
                }
            }
        }
        """ % self.config.project_id
        
        return self._execute_query(query)
    
    def get_services(self) -> Dict:
        """Get project services"""
        query = """
        query {
            services(projectId: "%s") {
                edges {
                    node {
                        id
                        name
                        status
                    }
                }
            }
        }
        """ % self.config.project_id
        
        return self._execute_query(query)
    
    def create_deployment(self, docker_image: str, environment_vars: Dict) -> Dict:
        """Create new Railway deployment"""
        query = """
        mutation {
            deploymentCreate(input: {
                projectId: "%s"
                serviceName: "%s"
                image: "%s"
                environmentVariables: %s
                resourceLimits: {
                    memoryMB: %d
                    cpuMillicores: %d
                }
            }) {
                deployment {
                    id
                    status
                    url
                }
                errors {
                    message
                }
            }
        }
        """ % (
            self.config.project_id,
            self.config.service_name,
            docker_image,
            str(environment_vars).replace("'", '"'),
            self.config.memory_mb,
            self.config.cpu_millicores
        )
        
        return self._execute_query(query)
    
    def get_environment_variables(self) -> Dict:
        """Get deployment environment variables"""
        query = """
        query {
            deployment(id: "%s") {
                environmentVariables {
                    name
                    value
                }
            }
        }
        """ % self.config.project_id
        
        return self._execute_query(query)
    
    def update_environment_variable(self, name: str, value: str) -> Dict:
        """Update environment variable"""
        query = """
        mutation {
            variableUpdate(input: {
                projectId: "%s"
                name: "%s"
                value: "%s"
            }) {
                variable {
                    id
                    name
                    value
                }
                errors {
                    message
                }
            }
        }
        """ % (self.config.project_id, name, value)
        
        return self._execute_query(query)
    
    def trigger_redeploy(self) -> Dict:
        """Trigger redeployment"""
        query = """
        mutation {
            deploymentRedeploy(input: {
                projectId: "%s"
            }) {
                deployment {
                    id
                    status
                }
                errors {
                    message
                }
            }
        }
        """ % self.config.project_id
        
        return self._execute_query(query)
    
    def get_logs(self, deployment_id: str, limit: int = 100) -> Dict:
        """Get deployment logs"""
        query = """
        query {
            deployment(id: "%s") {
                logs(first: %d) {
                    edges {
                        node {
                            timestamp
                            message
                            level
                        }
                    }
                }
            }
        }
        """ % (deployment_id, limit)
        
        return self._execute_query(query)
    
    def _execute_query(self, query: str) -> Dict:
        """Execute GraphQL query"""
        try:
            response = requests.post(
                self.BASE_URL,
                headers=self.headers,
                json={"query": query},
                timeout=30
            )
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def get_connection_string(self) -> str:
        """Get Railway connection string for Agent Zero"""
        return f"railway://{self.config.railway_token}@{self.config.project_id}/{self.config.service_name}"

class AgentZeroRailwayDeployer:
    """Deploy Agent Zero to Railway"""
    
    def __init__(self, railway_config: RailwayConfig):
        self.config = railway_config
        self.connection = RailwayConnection(railway_config)
    
    def get_required_env_vars(self) -> Dict[str, str]:
        """Get required environment variables for Agent Zero"""
        return {
            "LMS_URL": self.config.lms_url,
            "OPENROUTER_API_KEY": self.config.openrouter_api_key or "your-api-key-here",
            "ENVIRONMENT": self.config.environment.value,
            "RAILWAY_TOKEN": self.config.railway_token,
            "PROJECT_ID": self.config.project_id,
            "CHAT_NETWORK": "chat-network"
        }
    
    def prepare_deployment(self) -> Dict:
        """Prepare Agent Zero deployment for Railway"""
        env_vars = self.get_required_env_vars()
        
        deployment_config = {
            "service_name": self.config.service_name,
            "image": "agent0ai/agent-zero:v1.3",
            "port": 80,
            "environment_variables": env_vars,
            "memory_mb": self.config.memory_mb,
            "cpu_millicores": self.config.cpu_millicores,
            "restart_policy": "unless-stopped",
            "healthcheck": {
                "endpoint": "/",
                "interval": 30,
                "timeout": 10,
                "retries": 3
            }
        }
        
        return deployment_config
    
    def validate_configuration(self) -> bool:
        """Validate Railway configuration"""
        required_fields = [
            self.config.railway_token,
            self.config.project_id,
            self.config.service_name
        ]
        
        return all(required_fields)
    
    def deploy(self) -> Dict:
        """Deploy Agent Zero to Railway"""
        if not self.validate_configuration():
            return {"error": "Invalid configuration"}
        
        config = self.prepare_deployment()
        
        result = self.connection.create_deployment(
            config["image"],
            config["environment_variables"]
        )
        
        return result

class RailwayHealthCheck:
    """Health check for Railway-deployed Agent Zero"""
    
    def __init__(self, deployment_url: str):
        self.deployment_url = deployment_url
    
    def check_agent_zero(self) -> bool:
        """Check if Agent Zero is responding"""
        try:
            response = requests.get(
                f"{self.deployment_url}/",
                timeout=10
            )
            return response.status_code == 200
        except:
            return False
    
    def check_lms(self, lms_url: str) -> bool:
        """Check if LMS is responding"""
        try:
            response = requests.get(
                f"{lms_url}/health",
                timeout=10
            )
            return response.status_code == 200
        except:
            return False
    
    def full_health_check(self, lms_url: str) -> Dict:
        """Full health check of deployed system"""
        return {
            "agent_zero": self.check_agent_zero(),
            "lms": self.check_lms(lms_url),
            "timestamp": str(__import__('datetime').datetime.now())
        }

# Example Usage
if __name__ == "__main__":
    # Configure Railway connection
    config = RailwayConfig(
        railway_token=os.getenv("RAILWAY_TOKEN", "your-railway-token"),
        project_id=os.getenv("RAILWAY_PROJECT_ID", "your-project-id"),
        service_name="agent-zero",
        environment=RailwayEnvironment.PRODUCTION,
        openrouter_api_key=os.getenv("OPENROUTER_API_KEY", "your-api-key")
    )
    
    # Create connection
    railway = RailwayConnection(config)
    
    # Get project details
    print("Getting project details...")
    project = railway.get_project()
    print(project)
    
    # Get services
    print("\nGetting services...")
    services = railway.get_services()
    print(services)
    
    # Deploy Agent Zero
    print("\nDeploying Agent Zero...")
    deployer = AgentZeroRailwayDeployer(config)
    
    if deployer.validate_configuration():
        deployment = deployer.deploy()
        print(deployment)
        
        # Health check
        if "deployment" in deployment:
            deployment_url = deployment["deployment"].get("url", "")
            health = RailwayHealthCheck(deployment_url)
            print("\nHealth check:", health.full_health_check(config.lms_url))
    else:
        print("Configuration validation failed")
    
    # Connection string for documentation
    print(f"\nConnection String: {railway.get_connection_string()}")
