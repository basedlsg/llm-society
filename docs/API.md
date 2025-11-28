# LLM Society API Documentation

## Overview

LLM Society is a 2,500-agent LLM-driven society simulation. This document describes the core APIs for running simulations, configuring agents, and extending the system.

## Quick Start

```python
from llm_society.simulation.society_simulator import SocietySimulator
from llm_society.utils.config import Config

# Load configuration
config = Config.default()
config.agents.count = 100
config.simulation.max_steps = 500

# Create and run simulation
simulator = SocietySimulator(config)
await simulator.run()
```

## Core Classes

### `SocietySimulator`

Main simulation orchestrator extending Mesa's `Model` class.

```python
class SocietySimulator(mesa.Model):
    def __init__(self, config: Config)
    async def run() -> None
    async def step() -> None
    def save_state(filepath: str) -> None
    @classmethod
    def load_from_file(filepath: str) -> SocietySimulator
```

**Methods:**
- `run()`: Execute the full simulation loop
- `step()`: Execute a single simulation step
- `save_state(path)`: Serialize simulation to JSON
- `load_from_file(path)`: Restore simulation from JSON

### `LLMAgent`

LLM-powered agent inheriting from Mesa's `Agent`.

```python
class LLMAgent(Agent):
    def __init__(
        self,
        model: SocietySimulator,
        unique_id: str,
        llm_coordinator: LLMCoordinator,
        config: Config,
        position: Optional[Position] = None,
        persona: Optional[str] = None,
    )
    async def step() -> None
    def get_status() -> Dict[str, Any]
    def to_dict() -> Dict[str, Any]
    @classmethod
    def from_dict(data, model, llm_coordinator, config) -> LLMAgent
```

**Agent States:**
- `IDLE` - No current activity
- `MOVING` - Moving to target position
- `SOCIALIZING` - Interacting with other agents
- `WORKING` - Performing work actions
- `CREATING` - Creating objects
- `THINKING` - Processing LLM decisions

**Agent Actions:**
- `move_to <x> <y>` - Move to coordinates
- `talk_to <agent_id>` - Social interaction
- `create_object <description>` - Create 3D asset
- `gather_resources` - Collect resources
- `rest` - Recover energy
- `market_trade <buy/sell> <resource> <qty> <price>` - Trade
- `banking_action <type> <params>` - Banking operations

### `LLMCoordinator`

Manages all LLM API interactions with batching and caching.

```python
class LLMCoordinator:
    def __init__(self, config: LLMConfig)
    async def start() -> None
    async def stop() -> None
    async def get_response(
        agent_id: str,
        prompt: str,
        max_tokens: int = 150,
        temperature: float = 0.7,
    ) -> str
```

**Features:**
- Request batching (configurable batch size)
- LRU response cache (default 5000 items)
- Rate limiting (default 10 req/sec)
- Automatic retry with exponential backoff
- Fallback to mock responses on API failure

## Economic System

### `MarketSystem`

Manages resource trading between agents.

```python
class MarketSystem:
    def submit_order(
        agent_id: str,
        resource_type: ResourceType,
        order_type: TradeOrderType,
        quantity: float,
        price_per_unit: float,
    ) -> Optional[str]
    def get_resource_market_summary(resource: ResourceType) -> str
    def get_general_market_overview() -> str
```

**Resource Types:**
- `FOOD`, `MATERIALS`, `ENERGY`, `LUXURY`
- `TOOLS`, `KNOWLEDGE`, `SERVICES`, `CURRENCY`

### `BankingSystem`

Manages agent accounts, loans, and transactions.

```python
class BankingSystem:
    async def create_account(
        agent_id: str,
        account_type: AccountType,
        initial_deposit: float,
        current_step: int,
    ) -> Optional[BankAccount]
    async def process_transaction(
        account_id: str,
        transaction_type: TransactionType,
        amount: float,
        description: str,
        current_step: int,
    ) -> bool
    async def apply_for_loan(
        agent_id: str,
        loan_type: LoanType,
        amount: float,
        purpose: str,
        term_months: int,
        current_step: int,
    ) -> Optional[Loan]
```

## Social System

### `FamilySystem`

Manages family relationships and inheritance.

```python
class FamilySystem:
    def create_family(family_type: FamilyType) -> Family
    def add_member(family_id: str, agent_id: str) -> None
    def get_family_members(family_id: str) -> List[str]
    def process_interaction_with_spouse(...) -> None
    def process_interaction_with_child(...) -> None
```

**Relationship Types:**
- `PARENT`, `CHILD`, `SIBLING`, `SPOUSE`
- `GRANDPARENT`, `GRANDCHILD`
- `AUNT_UNCLE`, `COUSIN`, `NIECE_NEPHEW`

## Configuration

### Config Dataclasses

```python
@dataclass
class Config:
    llm: LLMConfig
    agents: AgentConfig
    simulation: SimulationConfig
    output: OutputConfig
    monitoring: MonitoringConfig
    assets: AssetsConfig
    performance: PerformanceConfig
```

### Loading Configuration

```python
# From file
config = Config.load("config.yaml")

# Default with overrides
config = Config.default()
config.agents.count = 500
config.llm.model_name = "gemini-1.5-pro"
```

### Example YAML Configuration

```yaml
llm:
  model_name: "gemini-pro"
  max_tokens: 150
  temperature: 0.7
  max_cache_size: 5000
  rate_limit_per_second: 10

agents:
  count: 100
  movement_speed: 1.0
  social_radius: 10.0
  memory_size: 20

simulation:
  max_steps: 1000
  world_size: [100, 100]
  autosave_interval_steps: 100

performance:
  enable_gpu_acceleration: false
  parallel_llm_requests: 5
  async_database_writes: true
```

## GPU Acceleration

### FLAME GPU Integration

For large-scale simulations (>500 agents), enable GPU acceleration:

```python
config.performance.enable_gpu_acceleration = True
config.performance.gpu_device_id = 0
```

GPU kernels handle:
- Agent movement and spatial queries
- Social interaction processing
- Economic trading
- Cultural influence propagation
- Family interactions

## Monitoring

### Structured Logging

```python
from llm_society.monitoring import setup_logging, get_logger, metrics

# Setup structured JSON logging
setup_logging(level="INFO", structured=True, log_file="simulation.log")

# Get a logger
logger = get_logger("my_component")
logger.info("Event occurred", extra={"agent_id": "agent_1", "action": "move"})
```

### Metrics Collection

```python
from llm_society.monitoring import metrics

# Record metrics
metrics.increment("agent_actions", labels={"type": "move"})
metrics.gauge("active_agents", 150)
metrics.histogram("llm_latency_seconds", 0.5)

# Get summary
summary = metrics.get_summary()
```

## CLI Interface

```bash
# Run simulation
python -m llm_society.main run --agents 100 --steps 500 --model gemini-pro

# Run demo scenario
python -m llm_society.main demo --scenario basic

# Run benchmark
python -m llm_society.main benchmark --agents 500 --duration 60

# Validate installation
python -m llm_society.main validate
```

## Error Handling

All async operations should be wrapped in try/except:

```python
try:
    response = await llm_coordinator.get_response(...)
except Exception as e:
    logger.error(f"LLM request failed: {e}")
    # Use fallback decision
    action = agent._fallback_decision()
```

## Extending the System

### Adding New Agent Actions

1. Add action parsing in `_parse_llm_response()`
2. Implement `_execute_<action>()` method
3. Update the decision prompt with new action option
4. Add tests for the new action

### Adding New Kernels (GPU)

1. Define the kernel function with `@pyflamegpu.agent_function`
2. Register the function in `FlameGPUSimulation._define_model_layers_and_functions()`
3. Add message types if needed for inter-agent communication
