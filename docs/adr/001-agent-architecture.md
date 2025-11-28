# ADR 001: Agent Architecture Design

## Status
Accepted

## Context
The LLM Society simulation requires an architecture that can support up to 2,500 agents, each powered by Large Language Models for intelligent decision-making. The system needs to balance:
- Real-time decision making with LLM latency
- Memory efficiency for large agent populations
- GPU acceleration for parallel agent processing
- Persistence of agent state and memories

## Decision

### Agent Class Structure
We adopted a mixin-based architecture for the `LLMAgent` class:

```
LLMAgent (Mesa Agent)
├── SpatialMixin - Movement and positioning
├── MemoryMixin - Memory management and LLM reasoning
├── SocialMixin - Social interactions and relationships
└── EconomicMixin - Trading, banking, and resources
```

### Key Design Choices

1. **Async-First Architecture**: All agent operations are async to handle LLM latency without blocking the simulation loop.

2. **LLM Coordinator Pattern**: A centralized `LLMCoordinator` handles all LLM requests with:
   - Request batching for efficiency
   - Response caching (LRU with 5000 item limit)
   - Rate limiting to prevent API throttling
   - Fallback to mock responses when APIs fail

3. **GPU Acceleration via FLAME GPU 2**: For simulations >500 agents, we use FLAME GPU 2 with:
   - Python agent functions for GPU kernels
   - Brute-force message passing for agent communication
   - Separate layers for different interaction types

4. **Memory System**: Each agent maintains a weighted memory buffer:
   - Maximum 20 memories per agent (configurable)
   - Importance-based retention during cleanup
   - Async persistence to SQLite database

## Consequences

### Positive
- Scales to 2,500 agents with GPU acceleration
- LLM cache achieves 98% hit rate for repeated scenarios
- Mixin architecture allows easy extension of agent capabilities
- State persistence enables simulation resume

### Negative
- GPU acceleration requires CUDA-capable hardware
- LLM costs scale with agent count (mitigated by caching)
- Complex state synchronization between Mesa and FLAME GPU

### Neutral
- Requires careful tuning of batch sizes and cache limits
- Trade-off between simulation speed and LLM response quality

## References
- Mesa Agent-Based Modeling Framework
- FLAME GPU 2 Documentation
- Google Gemini Pro API Documentation
