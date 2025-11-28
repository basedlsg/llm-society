"""Unit tests for Position class"""

import pytest
import math
from llm_society.agents.spatial_mixin import Position


class TestPosition:
    """Tests for Position dataclass"""

    def test_position_creation(self):
        """Test basic position creation"""
        pos = Position(x=10.0, y=20.0, z=5.0)
        assert pos.x == 10.0
        assert pos.y == 20.0
        assert pos.z == 5.0

    def test_position_default_z(self):
        """Test position with default z value"""
        pos = Position(x=10.0, y=20.0)
        assert pos.z == 0.0

    def test_distance_to_same_position(self):
        """Test distance to same position is zero"""
        pos1 = Position(x=5.0, y=5.0, z=5.0)
        pos2 = Position(x=5.0, y=5.0, z=5.0)
        assert pos1.distance_to(pos2) == 0.0

    def test_distance_to_horizontal(self):
        """Test horizontal distance calculation"""
        pos1 = Position(x=0.0, y=0.0)
        pos2 = Position(x=3.0, y=4.0)
        assert pos1.distance_to(pos2) == 5.0  # 3-4-5 triangle

    def test_distance_to_3d(self):
        """Test 3D distance calculation"""
        pos1 = Position(x=0.0, y=0.0, z=0.0)
        pos2 = Position(x=1.0, y=2.0, z=2.0)
        expected = math.sqrt(1 + 4 + 4)  # sqrt(9) = 3
        assert abs(pos1.distance_to(pos2) - expected) < 0.0001

    def test_move_towards_reaches_target(self):
        """Test move_towards when speed exceeds distance"""
        pos = Position(x=0.0, y=0.0)
        target = Position(x=1.0, y=1.0)
        new_pos = pos.move_towards(target, speed=10.0)
        assert new_pos.x == target.x
        assert new_pos.y == target.y

    def test_move_towards_partial(self):
        """Test move_towards with partial movement"""
        pos = Position(x=0.0, y=0.0)
        target = Position(x=10.0, y=0.0)
        new_pos = pos.move_towards(target, speed=3.0)
        assert abs(new_pos.x - 3.0) < 0.0001
        assert abs(new_pos.y - 0.0) < 0.0001

    def test_to_dict(self):
        """Test serialization to dict"""
        pos = Position(x=1.0, y=2.0, z=3.0)
        data = pos.to_dict()
        assert data == {"x": 1.0, "y": 2.0, "z": 3.0}

    def test_from_dict(self):
        """Test deserialization from dict"""
        data = {"x": 5.0, "y": 10.0, "z": 15.0}
        pos = Position.from_dict(data)
        assert pos.x == 5.0
        assert pos.y == 10.0
        assert pos.z == 15.0

    def test_from_dict_with_defaults(self):
        """Test deserialization with missing keys"""
        data = {"x": 5.0}
        pos = Position.from_dict(data)
        assert pos.x == 5.0
        assert pos.y == 0.0
        assert pos.z == 0.0
