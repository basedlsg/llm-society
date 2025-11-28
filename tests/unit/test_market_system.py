"""Unit tests for Market System"""

import pytest
from llm_society.economics.market_system import (
    ResourceType,
    TradeOrderType,
    OrderStatus,
    TradeOrder,
)


class TestResourceType:
    """Tests for ResourceType enum"""

    def test_all_resource_types_exist(self):
        """Test all expected resource types are defined"""
        expected = ["food", "materials", "energy", "luxury", "tools", "knowledge", "services", "currency"]
        actual = [rt.value for rt in ResourceType]
        assert set(expected) == set(actual)

    def test_resource_type_from_string(self):
        """Test creating ResourceType from string value"""
        assert ResourceType("food") == ResourceType.FOOD
        assert ResourceType("tools") == ResourceType.TOOLS


class TestTradeOrderType:
    """Tests for TradeOrderType enum"""

    def test_order_types(self):
        """Test buy and sell order types exist"""
        assert TradeOrderType.BUY.value == "buy"
        assert TradeOrderType.SELL.value == "sell"


class TestOrderStatus:
    """Tests for OrderStatus enum"""

    def test_all_statuses_exist(self):
        """Test all order statuses are defined"""
        expected = ["pending", "partial", "completed", "cancelled"]
        actual = [os.value for os in OrderStatus]
        assert set(expected) == set(actual)


class TestTradeOrder:
    """Tests for TradeOrder dataclass"""

    def test_trade_order_creation(self):
        """Test basic trade order creation"""
        order = TradeOrder(
            order_id="order_1",
            agent_id="agent_1",
            resource_type=ResourceType.FOOD,
            order_type=TradeOrderType.BUY,
            quantity=10.0,
            price_per_unit=5.0,
        )
        assert order.order_id == "order_1"
        assert order.agent_id == "agent_1"
        assert order.resource_type == ResourceType.FOOD
        assert order.order_type == TradeOrderType.BUY
        assert order.quantity == 10.0
        assert order.price_per_unit == 5.0

    def test_trade_order_defaults(self):
        """Test trade order default values"""
        order = TradeOrder(
            order_id="order_1",
            agent_id="agent_1",
            resource_type=ResourceType.FOOD,
            order_type=TradeOrderType.BUY,
            quantity=10.0,
            price_per_unit=5.0,
        )
        assert order.quantity_filled == 0.0
        assert order.status == OrderStatus.PENDING
        assert order.max_price is None
        assert order.min_price is None
        assert order.priority == 1.0

    def test_to_dict(self):
        """Test serialization to dict"""
        order = TradeOrder(
            order_id="order_1",
            agent_id="agent_1",
            resource_type=ResourceType.TOOLS,
            order_type=TradeOrderType.SELL,
            quantity=5.0,
            price_per_unit=10.0,
            status=OrderStatus.PARTIAL,
        )
        data = order.to_dict()
        assert data["order_id"] == "order_1"
        assert data["resource_type"] == "tools"
        assert data["order_type"] == "sell"
        assert data["status"] == "partial"

    def test_from_dict(self):
        """Test deserialization from dict"""
        data = {
            "order_id": "order_2",
            "agent_id": "agent_2",
            "resource_type": "materials",
            "order_type": "buy",
            "quantity": 20.0,
            "price_per_unit": 3.0,
            "max_price": None,
            "min_price": None,
            "quantity_filled": 5.0,
            "status": "partial",
            "created_time": 1000.0,
            "expiry_time": None,
            "priority": 1.0,
        }
        order = TradeOrder.from_dict(data)
        assert order.order_id == "order_2"
        assert order.resource_type == ResourceType.MATERIALS
        assert order.order_type == TradeOrderType.BUY
        assert order.quantity_filled == 5.0
        assert order.status == OrderStatus.PARTIAL

    def test_roundtrip_serialization(self):
        """Test that to_dict/from_dict preserves data"""
        original = TradeOrder(
            order_id="order_test",
            agent_id="agent_test",
            resource_type=ResourceType.ENERGY,
            order_type=TradeOrderType.SELL,
            quantity=100.0,
            price_per_unit=15.0,
            min_price=12.0,
            quantity_filled=25.0,
            status=OrderStatus.PARTIAL,
            priority=2.0,
        )
        data = original.to_dict()
        restored = TradeOrder.from_dict(data)

        assert restored.order_id == original.order_id
        assert restored.agent_id == original.agent_id
        assert restored.resource_type == original.resource_type
        assert restored.order_type == original.order_type
        assert restored.quantity == original.quantity
        assert restored.price_per_unit == original.price_per_unit
        assert restored.quantity_filled == original.quantity_filled
        assert restored.status == original.status
