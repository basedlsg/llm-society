"""Unit tests for Memory class"""

import pytest
from llm_society.agents.memory_mixin import Memory


class TestMemory:
    """Tests for Memory dataclass"""

    def test_memory_creation(self):
        """Test basic memory creation"""
        mem = Memory(
            content="Test memory",
            timestamp=100.0,
            importance=0.8,
            tags=["test", "unit"],
            agent_id="agent_1",
        )
        assert mem.content == "Test memory"
        assert mem.timestamp == 100.0
        assert mem.importance == 0.8
        assert mem.tags == ["test", "unit"]
        assert mem.agent_id == "agent_1"

    def test_memory_defaults(self):
        """Test memory with default values"""
        mem = Memory(content="Test", timestamp=0.0)
        assert mem.importance == 0.5
        assert mem.tags == []
        assert mem.agent_id is None

    def test_to_dict(self):
        """Test serialization to dict"""
        mem = Memory(
            content="Test memory",
            timestamp=100.0,
            importance=0.8,
            tags=["test"],
            agent_id="agent_1",
        )
        data = mem.to_dict()
        assert data["content"] == "Test memory"
        assert data["timestamp"] == 100.0
        assert data["importance"] == 0.8
        assert data["tags"] == ["test"]
        assert data["agent_id"] == "agent_1"

    def test_from_dict(self):
        """Test deserialization from dict"""
        data = {
            "content": "Loaded memory",
            "timestamp": 50.0,
            "importance": 0.6,
            "tags": ["loaded"],
            "agent_id": "agent_2",
        }
        mem = Memory.from_dict(data)
        assert mem.content == "Loaded memory"
        assert mem.timestamp == 50.0
        assert mem.importance == 0.6
        assert mem.tags == ["loaded"]
        assert mem.agent_id == "agent_2"

    def test_from_dict_ensures_tags_list(self):
        """Test that from_dict converts tags to list"""
        data = {
            "content": "Test",
            "timestamp": 0.0,
            "tags": None,  # Should become empty list
        }
        mem = Memory.from_dict(data)
        assert mem.tags == []

    def test_roundtrip_serialization(self):
        """Test that to_dict/from_dict preserves data"""
        original = Memory(
            content="Important event",
            timestamp=999.0,
            importance=0.95,
            tags=["event", "important"],
            agent_id="agent_test",
        )
        data = original.to_dict()
        restored = Memory.from_dict(data)

        assert restored.content == original.content
        assert restored.timestamp == original.timestamp
        assert restored.importance == original.importance
        assert restored.tags == original.tags
        assert restored.agent_id == original.agent_id
