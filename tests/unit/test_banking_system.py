"""Unit tests for Banking System"""

import pytest
from llm_society.economics.banking_system import (
    AccountType,
    LoanType,
    LoanStatus,
    TransactionType,
)


class TestAccountType:
    """Tests for AccountType enum"""

    def test_all_account_types_exist(self):
        """Test all expected account types are defined"""
        expected = ["checking", "savings", "business", "investment"]
        actual = [at.value for at in AccountType]
        assert set(expected) == set(actual)

    def test_account_type_from_string(self):
        """Test creating AccountType from string value"""
        assert AccountType("checking") == AccountType.CHECKING
        assert AccountType("savings") == AccountType.SAVINGS


class TestLoanType:
    """Tests for LoanType enum"""

    def test_all_loan_types_exist(self):
        """Test all expected loan types are defined"""
        expected = ["personal", "business", "mortgage", "education", "emergency"]
        actual = [lt.value for lt in LoanType]
        assert set(expected) == set(actual)


class TestLoanStatus:
    """Tests for LoanStatus enum"""

    def test_all_loan_statuses_exist(self):
        """Test all loan statuses are defined"""
        expected = ["pending", "approved", "active", "paid_of", "defaulted", "rejected"]
        actual = [ls.value for ls in LoanStatus]
        assert set(expected) == set(actual)

    def test_loan_status_active(self):
        """Test active loan status"""
        assert LoanStatus.ACTIVE.value == "active"


class TestTransactionType:
    """Tests for TransactionType enum"""

    def test_deposit_exists(self):
        """Test deposit transaction type exists"""
        assert hasattr(TransactionType, "DEPOSIT")

    def test_withdrawal_exists(self):
        """Test withdrawal transaction type exists"""
        assert hasattr(TransactionType, "WITHDRAWAL")
