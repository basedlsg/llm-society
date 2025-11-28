# LLM Society Deployment Guide

## Prerequisites

### System Requirements

**Minimum:**
- Python 3.11+
- 8GB RAM
- 4 CPU cores

**Recommended (for 2,500 agents):**
- Python 3.11+
- 32GB RAM
- 8+ CPU cores
- NVIDIA GPU with CUDA 11.0+ (for GPU acceleration)

### API Keys Required

- **Google Generative AI API Key** (for Gemini models)
- **OpenAI API Key** (optional, for GPT-4 fallback)
- **Anthropic API Key** (optional, for Claude fallback)

## Installation

### 1. Clone Repository

```bash
git clone <repository-url>
cd llm-society
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate  # Windows
```

### 3. Install Dependencies

**Basic installation:**
```bash
pip install -e .
```

**With development tools:**
```bash
pip install -e ".[dev]"
```

**With LLM providers:**
```bash
pip install -e ".[llm]"
```

**With GPU support:**
```bash
pip install -e ".[gpu]"
```

**Full installation:**
```bash
pip install -e ".[all]"
```

### 4. Configure Environment

Create a `.env` file:

```bash
# Required
GOOGLE_API_KEY=your_google_api_key

# Optional - Fallback LLM providers
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key

# Simulation settings
NUM_AGENTS=100
SIMULATION_STEPS=1000
DEFAULT_LLM_MODEL=gemini-pro

# GPU settings (if using)
FLAMEGPU_ENABLED=false

# Monitoring (optional)
WANDB_PROJECT=llm-society
```

## Running the Simulation

### Basic Run

```bash
python -m llm_society.main run --agents 50 --steps 100
```

### With Custom Configuration

```bash
python -m llm_society.main run \
    --agents 100 \
    --steps 500 \
    --model gemini-pro \
    --config config.yaml \
    --output ./results
```

### Demo Mode

```bash
python -m llm_society.main demo --scenario basic
```

### Benchmark Mode

```bash
python -m llm_society.main benchmark --agents 500 --duration 60
```

## Configuration

### Create `config.yaml`

```yaml
llm:
  model_name: "gemini-pro"
  max_tokens: 150
  temperature: 0.7
  max_cache_size: 5000
  rate_limit_per_second: 10
  batch_size: 10

agents:
  count: 100
  movement_speed: 1.0
  social_radius: 10.0
  memory_size: 20

simulation:
  max_steps: 1000
  world_size: [100, 100]
  tick_rate: 0.1
  autosave_enabled: true
  autosave_interval_steps: 100

output:
  directory: "./results"
  database_url: "sqlite:///./llm_society.db"
  db_pool_size: 5

monitoring:
  enable_metrics: true
  metrics_interval: 10

performance:
  enable_gpu_acceleration: false
  parallel_llm_requests: 5
  async_database_writes: true
```

## GPU Acceleration Setup

### 1. Install CUDA Toolkit

Ensure CUDA 11.0+ is installed:
```bash
nvidia-smi  # Check CUDA version
```

### 2. Install FLAME GPU 2

```bash
pip install pyflamegpu
```

### 3. Enable GPU in Configuration

```yaml
performance:
  enable_gpu_acceleration: true
  gpu_device_id: 0
```

Or via environment:
```bash
FLAMEGPU_ENABLED=true
```

## Production Deployment

### Docker Deployment

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY pyproject.toml .
COPY llm_society/ ./llm_society/
RUN pip install -e ".[all]"

# Copy configuration
COPY config.yaml .

# Run simulation
CMD ["python", "-m", "llm_society.main", "run", "--config", "config.yaml"]
```

Build and run:
```bash
docker build -t llm-society .
docker run -v $(pwd)/results:/app/results --env-file .env llm-society
```

### Docker Compose with GPU

```yaml
version: '3.8'
services:
  simulation:
    build: .
    volumes:
      - ./results:/app/results
    env_file:
      - .env
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: llm-society
spec:
  replicas: 1
  selector:
    matchLabels:
      app: llm-society
  template:
    metadata:
      labels:
        app: llm-society
    spec:
      containers:
      - name: simulation
        image: llm-society:latest
        resources:
          limits:
            memory: "8Gi"
            cpu: "4"
            nvidia.com/gpu: 1
        env:
        - name: GOOGLE_API_KEY
          valueFrom:
            secretKeyRef:
              name: llm-secrets
              key: google-api-key
        volumeMounts:
        - name: results
          mountPath: /app/results
      volumes:
      - name: results
        persistentVolumeClaim:
          claimName: simulation-results
```

## Monitoring

### Enable Structured Logging

```python
from llm_society.monitoring import setup_logging

setup_logging(
    level="INFO",
    structured=True,
    log_file="simulation.log"
)
```

### Prometheus Metrics (Optional)

Export metrics for Prometheus scraping:

```python
from llm_society.monitoring import metrics

# Get metrics summary
summary = metrics.get_summary()

# Expose via HTTP (add prometheus_client dependency)
from prometheus_client import start_http_server, Counter, Gauge

start_http_server(8000)
```

### Weights & Biases Integration

```bash
pip install wandb
wandb login
```

Enable in config:
```yaml
monitoring:
  enable_wandb: true
  wandb_project: "llm-society"
```

## Troubleshooting

### Common Issues

**1. LLM API Rate Limits**
```
Error: Rate limit exceeded
```
Solution: Reduce `rate_limit_per_second` in config or increase cache size.

**2. Out of Memory**
```
Error: MemoryError
```
Solution: Reduce agent count or enable GPU acceleration.

**3. GPU Not Found**
```
Error: CUDA device not available
```
Solution: Verify CUDA installation with `nvidia-smi` and reinstall pyflamegpu.

**4. Database Lock**
```
Error: database is locked
```
Solution: Enable `async_database_writes` or increase `db_pool_size`.

### Debug Mode

Run with debug logging:
```bash
python -m llm_society.main run --debug --agents 10 --steps 10
```

### Validation

Run installation validation:
```bash
python -m llm_society.main validate
```

## Scaling Guidelines

| Agent Count | RAM Required | Recommended Setup |
|------------|--------------|-------------------|
| 50-100     | 4GB          | CPU only |
| 100-500    | 8GB          | CPU with SSD |
| 500-1000   | 16GB         | GPU recommended |
| 1000-2500  | 32GB         | GPU required |

### Performance Tuning

1. **Increase LLM cache size** for repetitive scenarios
2. **Enable request deduplication** to avoid duplicate API calls
3. **Use GPU acceleration** for >500 agents
4. **Enable async database writes** for better throughput
5. **Tune batch sizes** based on available memory
