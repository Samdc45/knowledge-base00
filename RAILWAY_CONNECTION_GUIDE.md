# Railway Connection Code - Agent Zero Deployment Guide

## Overview

This code enables you to programmatically connect to Railway and deploy Agent Zero with all required configurations.

## Setup

### 1. Get Railway Token

1. Go to https://railway.app/
2. Sign in to your account
3. Go to **Account Settings** → **API Tokens**
4. Create new token
5. Copy token (you'll use this for `RAILWAY_TOKEN`)

### 2. Get Project ID

1. Go to your Railway project
2. In project settings, find **Project ID**
3. Copy it (you'll use this for `RAILWAY_PROJECT_ID`)

### 3. Set Environment Variables

```bash
export RAILWAY_TOKEN="your-railway-token-here"
export RAILWAY_PROJECT_ID="your-project-id-here"
export OPENROUTER_API_KEY="your-openrouter-api-key-or-skip"
```

## Usage

### Basic Connection

```python
from railway_connection import RailwayConfig, RailwayConnection, RailwayEnvironment

# Create config
config = RailwayConfig(
    railway_token="your-token",
    project_id="your-project-id",
    service_name="agent-zero",
    environment=RailwayEnvironment.PRODUCTION
)

# Create connection
railway = RailwayConnection(config)

# Get project info
project = railway.get_project()
print(project)
```

### Deploy Agent Zero

```python
from railway_connection import AgentZeroRailwayDeployer

# Create deployer
deployer = AgentZeroRailwayDeployer(config)

# Prepare deployment
deployment_config = deployer.prepare_deployment()
print("Deployment config:", deployment_config)

# Deploy
result = deployer.deploy()
print("Deployment result:", result)
```

### Health Check

```python
from railway_connection import RailwayHealthCheck

health_check = RailwayHealthCheck("https://your-deployment.railway.app")
status = health_check.full_health_check("http://lms:6000")
print("Health status:", status)
```

### Get Environment Variables

```python
# Get all env vars
env_vars = railway.get_environment_variables()
print("Environment variables:", env_vars)

# Update single env var
railway.update_environment_variable("OPENROUTER_API_KEY", "new-key")
```

### View Logs

```python
# Get deployment logs
logs = railway.get_logs("deployment-id", limit=100)
print("Logs:", logs)
```

## Agent Zero Requirements

When deploying to Railway, the following environment variables are required:

```
LMS_URL=http://south-lms:6000
OPENROUTER_API_KEY=your-api-key
ENVIRONMENT=production
RAILWAY_TOKEN=your-railway-token
PROJECT_ID=your-project-id
CHAT_NETWORK=chat-network
```

## Resource Configuration

Default settings:
- **Memory**: 2048 MB
- **CPU**: 1000 millicores
- **Region**: us-west
- **Restart Policy**: unless-stopped

Adjust in `RailwayConfig`:

```python
config = RailwayConfig(
    railway_token="token",
    project_id="id",
    service_name="agent-zero",
    environment=RailwayEnvironment.PRODUCTION,
    memory_mb=4096,  # Increase for larger workloads
    cpu_millicores=2000
)
```

## Complete Example

```python
import os
from railway_connection import (
    RailwayConfig,
    RailwayConnection,
    AgentZeroRailwayDeployer,
    RailwayHealthCheck,
    RailwayEnvironment
)

# 1. Configure
config = RailwayConfig(
    railway_token=os.getenv("RAILWAY_TOKEN"),
    project_id=os.getenv("RAILWAY_PROJECT_ID"),
    service_name="agent-zero",
    environment=RailwayEnvironment.PRODUCTION,
    openrouter_api_key=os.getenv("OPENROUTER_API_KEY")
)

# 2. Create connection
railway = RailwayConnection(config)

# 3. Check project
print("Project:", railway.get_project())
print("Services:", railway.get_services())
print("Deployments:", railway.get_deployments())

# 4. Deploy Agent Zero
deployer = AgentZeroRailwayDeployer(config)
deployment = deployer.deploy()
print("Deployment:", deployment)

# 5. Health check
deployment_url = "https://your-deployment.railway.app"
health = RailwayHealthCheck(deployment_url)
print("Health:", health.full_health_check(config.lms_url))

# 6. Connection string
print("Connection:", railway.get_connection_string())
```

## API Methods

### Connection Methods

- `get_project()` - Get project details
- `get_services()` - List project services
- `get_deployments()` - List deployments
- `create_deployment()` - Create new deployment
- `get_environment_variables()` - Get env vars
- `update_environment_variable()` - Update single env var
- `trigger_redeploy()` - Trigger redeployment
- `get_logs()` - Get deployment logs
- `get_connection_string()` - Get connection string

### Deployer Methods

- `get_required_env_vars()` - Get Agent Zero env vars
- `prepare_deployment()` - Prepare deployment config
- `validate_configuration()` - Validate config
- `deploy()` - Deploy Agent Zero

### Health Check Methods

- `check_agent_zero()` - Check Agent Zero status
- `check_lms()` - Check LMS status
- `full_health_check()` - Full system health check

## Troubleshooting

### Authentication Error
```
Error: Unauthorized
Solution: Check RAILWAY_TOKEN is correct and valid
```

### Project Not Found
```
Error: Project not found
Solution: Verify RAILWAY_PROJECT_ID matches your project
```

### Deployment Failed
```
Error: Deployment creation failed
Solution: Check environment variables and resource limits
```

### Connection Timeout
```
Error: Request timeout
Solution: Increase timeout or check Railway API status
```

## Integration with Docker Compose

To use this with your local setup:

```python
# Update local docker-compose.yml with Railway connection
deployment = deployer.deploy()
deployment_url = deployment["deployment"]["url"]

# Update your local config to point to Railway
config.lms_url = deployment_url
```

## Security Notes

1. **Never commit tokens** to git
2. **Use environment variables** for sensitive data
3. **Rotate tokens regularly** in Railway dashboard
4. **Use different tokens** for different environments (dev, staging, prod)
5. **Restrict token permissions** to minimum required

## Next Steps

1. Get Railway token from https://railway.app/account/tokens
2. Get Project ID from Railway dashboard
3. Set environment variables
4. Run `python railway_connection.py`
5. Monitor deployment in Railway dashboard

---

**Version**: 1.0.0
**Last Updated**: March 28, 2026
**Status**: Production Ready ✅

