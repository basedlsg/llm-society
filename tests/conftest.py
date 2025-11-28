"""
Pytest configuration and shared fixtures for LLM Society tests
"""

import pytest
import sys
import os

# Add the project root to the path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


@pytest.fixture
def sample_position():
    """Provide a sample Position for testing"""
    from llm_society.agents.spatial_mixin import Position
    return Position(x=50.0, y=50.0, z=0.0)


@pytest.fixture
def sample_memory():
    """Provide a sample Memory for testing"""
    from llm_society.agents.memory_mixin import Memory
    return Memory(
        content="Test memory content",
        timestamp=100.0,
        importance=0.7,
        tags=["test"],
        agent_id="test_agent"
    )


@pytest.fixture
def sample_trade_order():
    """Provide a sample TradeOrder for testing"""
    from llm_society.economics.market_system import (
        TradeOrder, ResourceType, TradeOrderType
    )
    return TradeOrder(
        order_id="test_order_1",
        agent_id="test_agent",
        resource_type=ResourceType.FOOD,
        order_type=TradeOrderType.BUY,
        quantity=10.0,
        price_per_unit=5.0,
    )
