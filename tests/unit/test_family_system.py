"""Unit tests for Family System"""

import pytest
from llm_society.social.family_system import (
    FamilyType,
    RelationshipType,
)


class TestFamilyType:
    """Tests for FamilyType enum"""

    def test_all_family_types_exist(self):
        """Test all expected family types are defined"""
        expected = ["nuclear", "extended", "single_parent", "childless", "clan"]
        actual = [ft.value for ft in FamilyType]
        assert set(expected) == set(actual)

    def test_family_type_from_string(self):
        """Test creating FamilyType from string value"""
        assert FamilyType("nuclear") == FamilyType.NUCLEAR
        assert FamilyType("extended") == FamilyType.EXTENDED

    def test_family_type_str(self):
        """Test string representation"""
        assert str(FamilyType.NUCLEAR) == "nuclear"
        assert str(FamilyType.CLAN) == "clan"


class TestRelationshipType:
    """Tests for RelationshipType enum"""

    def test_all_relationship_types_exist(self):
        """Test all expected relationship types are defined"""
        expected = [
            "parent", "child", "sibling", "spouse",
            "grandparent", "grandchild", "aunt_uncle",
            "cousin", "niece_nephew"
        ]
        actual = [rt.value for rt in RelationshipType]
        assert set(expected) == set(actual)

    def test_relationship_type_from_string(self):
        """Test creating RelationshipType from string value"""
        assert RelationshipType("spouse") == RelationshipType.SPOUSE
        assert RelationshipType("child") == RelationshipType.CHILD

    def test_relationship_type_str(self):
        """Test string representation"""
        assert str(RelationshipType.PARENT) == "parent"
        assert str(RelationshipType.SIBLING) == "sibling"

    def test_immediate_family_relationships(self):
        """Test immediate family relationship types"""
        immediate = [RelationshipType.PARENT, RelationshipType.CHILD,
                     RelationshipType.SIBLING, RelationshipType.SPOUSE]
        for rel in immediate:
            assert rel in RelationshipType

    def test_extended_family_relationships(self):
        """Test extended family relationship types"""
        extended = [RelationshipType.GRANDPARENT, RelationshipType.GRANDCHILD,
                    RelationshipType.AUNT_UNCLE, RelationshipType.COUSIN,
                    RelationshipType.NIECE_NEPHEW]
        for rel in extended:
            assert rel in RelationshipType
