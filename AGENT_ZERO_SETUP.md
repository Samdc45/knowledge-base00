# Agent Zero Configuration Guide

## What is Being Configured

Agent Zero is being configured with:
1. **Local LLM** (Ollama + Mistral) - FREE, no API keys
2. **Background Knowledge** - Connected to LMS
3. **5 Subagents** - For task distribution
4. **Health Monitoring** - Automatic health checks
5. **Caching** - Performance optimization

## Quick Start (One Command)

```bash
docker-compose up -d
```

This starts:
- Ollama (local LLM model)
- Agent Zero (autonomous router)
- LMS (knowledge base)
- Chat network (inter-service communication)

## Configuration Options

### Option 1: Local Model (Recommended - FREE)
```yaml
- LLM_PROVIDER=ollama
- OLLAMA_MODEL=mistral
- OLLAMA_BASE_URL=http://ollama:11434
```
✅ No API key needed
✅ Completely free
✅ Runs locally
❌ Slower responses (but works)

### Option 2: OpenRouter (Requires API Key)
```yaml
- LLM_PROVIDER=openrouter
- OPENROUTER_API_KEY=sk-or-v1-...
```
✅ Better responses
❌ Costs money
❌ Requires API key

### Option 3: OpenAI (Requires API Key)
```yaml
- LLM_PROVIDER=openai
- OPENAI_API_KEY=sk-...
```
✅ Excellent quality
❌ Expensive
❌ Requires API key

## Services Running

```
┌─────────────────────────────────────────┐
│  Agent Zero (Port 55015)               │
│  • Autonomous router                  │
│  • Task orchestration                 │
│  • Subagent dispatcher                │
└──────────────────┬──────────────────────┘
                   │
        ┌──────────┼──────────┐
        │          │          │
   ┌────▼────┐ ┌──▼───┐ ┌───▼────┐
   │ Ollama   │ │ LMS  │ │Network │
   │ (Mistral)│ │(Knowl│ │(Chat)  │
   └────┬────┘ │Base) │ └───┬────┘
        │      └──┬───┘     │
        │         │         │
    Model    Knowledge   5 Subagents
    Access    Base
```

## Starting Agent Zero

### Method 1: Docker Compose (Recommended)
```bash
# Start all services
docker-compose up -d

# Check status
docker ps

# View logs
docker logs agent-zero
docker logs ollama
docker logs south-lms
```

### Method 2: Manual Start
```bash
# Start Ollama first
docker run -d --name ollama -p 11434:11434 ollama/ollama:latest

# Pull Mistral model
docker exec ollama ollama pull mistral

# Start Agent Zero
docker run -d \
  --name agent-zero \
  -p 55015:80 \
  -e LLM_PROVIDER=ollama \
  -e OLLAMA_BASE_URL=http://ollama:11434 \
  -e LMS_URL=http://south-lms:6000 \
  --network chat-network \
  agent0ai/agent-zero:v1.3

# Start LMS
docker run -d \
  --name south-lms \
  -p 6000:6000 \
  -e PORT=6000 \
  --network chat-network \
  mass161/south-lms:latest
```

## Accessing Agent Zero

- **UI**: http://localhost:55015
- **API**: http://localhost:55015/api
- **Health**: curl http://localhost:55015/

## LMS (Knowledge Base)

- **Health**: http://localhost:6000/health
- **Courses**: http://localhost:6000/api/courses
- **Modules**: http://localhost:6000/api/courses/{id}/modules

## First Run Tasks

### 1. Download Mistral Model
First time setup downloads ~7GB model (takes ~10-15 minutes):

```bash
# Check Ollama status
docker logs ollama

# Pull model manually if needed
docker exec ollama ollama pull mistral
```

### 2. Verify Connectivity

```bash
# Check Agent Zero
curl http://localhost:55015/

# Check Ollama
curl http://localhost:11434/api/tags

# Check LMS
curl http://localhost:6000/api/courses
```

### 3. Test Agent Zero

Open browser: http://localhost:55015

Or via API:
```bash
curl -X POST http://localhost:55015/api/task \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Get training courses"}'
```

## Environment Variables

All configuration is via environment variables:

```
# LMS Connection
LMS_URL=http://south-lms:6000
LMS_HEALTH_CHECK=http://south-lms:6000/health
LMS_COURSES_ENDPOINT=http://south-lms:6000/api/courses

# LLM Provider (choose one)
LLM_PROVIDER=ollama
OLLAMA_MODEL=mistral
OLLAMA_BASE_URL=http://ollama:11434

# Memory & Knowledge
MEMORY_ENABLED=true
BACKGROUND_KNOWLEDGE=true
KNOWLEDGE_SOURCE=LMS_SERVICE

# Performance
MAX_WORKERS=4
REQUEST_TIMEOUT=30
CACHE_ENABLED=true
CACHE_TTL=3600

# Subagents
SUBAGENT_1_LMS=http://south-lms:6000
SUBAGENT_2_API_GATEWAY=http://161:80
SUBAGENT_3_DATA_PROCESSOR=http://unruffled_buck:80
SUBAGENT_4_ANALYSIS=http://ecstatic_mirzakhani:80
SUBAGENT_5_ML_AI=http://magical_chaplygin:80
```

## Troubleshooting

### Agent Zero won't start
```
Error: Connection refused
Solution: Check if Ollama is running
$ docker ps | grep ollama

# If not running:
$ docker-compose up ollama -d
```

### Ollama downloading slowly
```
This is normal for first run.
Model size: ~7GB
Expected time: 10-15 minutes
```

### LMS not found
```
Error: LMS_URL connection refused
Solution: Start LMS service
$ docker-compose up south-lms -d
```

### High memory usage
```
Ollama model uses ~8GB RAM
Agent Zero uses ~2GB
Total: ~10GB needed
```

## Stopping Services

```bash
# Stop all services
docker-compose down

# Stop specific service
docker stop agent-zero
docker stop ollama
docker stop south-lms

# Remove volumes (careful!)
docker-compose down -v
```

## Monitoring

### View Logs
```bash
# Agent Zero
docker logs -f agent-zero

# Ollama
docker logs -f ollama

# LMS
docker logs -f south-lms
```

### Check Health
```bash
# All containers
docker ps

# Specific health
curl http://localhost:55015/
curl http://localhost:11434/api/tags
curl http://localhost:6000/health
```

### Performance Stats
```bash
# Memory/CPU usage
docker stats agent-zero ollama south-lms
```

## Production Deployment

### On Railway
1. Push `docker-compose.yml` to GitHub
2. Connect Railway to repository
3. Set environment variables in Railway
4. Deploy

### On Kubernetes
1. Convert docker-compose to Helm charts
2. Configure persistent volumes for Ollama
3. Set resource limits
4. Deploy

## Next Steps

1. **Start services**
   ```bash
   docker-compose up -d
   ```

2. **Wait for Mistral to download** (first run only)

3. **Access Agent Zero**
   ```
   http://localhost:55015
   ```

4. **Test with a task**
   ```
   "Get NZCI training courses"
   ```

5. **Monitor performance**
   ```bash
   docker stats
   ```

---

**Configuration Complete!**
Agent Zero is ready with:
✅ Local LLM (no API keys needed)
✅ Background knowledge from LMS
✅ 5 operational subagents
✅ Full health monitoring
✅ Performance optimization
