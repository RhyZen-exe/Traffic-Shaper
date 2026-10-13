import pytest
from unittest.mock import patch

from system.executor import ExecResult
from core.blocker import (
    is_valid_ip,
    classify_ip,
    is_in_network,
    normalize_ip,
    block_ip,
    unblock_ip,
)

def test_is_valid_ip_correct():
    assert is_valid_ip("192.168.1.5") is True
    assert is_valid_ip("8.8.8.8") is True
    assert is_valid_ip("2001:db8::1") is True

def test_is_valid_ip_invalid():
    assert is_valid_ip("abc") is False
    assert is_valid_ip("") is False
    assert is_valid_ip("999.999.999.999") is False

def test_classify_ip_valid():
    result = classify_ip("192.168.1.5")
    assert result["valid"] is True
    assert result["version"] == 4
    assert result["private"] is True
    
def test_classify_ip_invalid():
    result = classify_ip("abc")
    assert result == {"valid": False}

def test_is_in_network():
    assert is_in_network("192.168.1.5", "192.168.1.0/24") is True
    assert is_in_network("192.168.2.5", "192.168.1.0/24") is False
    assert is_in_network("abc", "192.168.1.0/24") is False    

def test_normalize_ip_raises():
    with pytest.raises(ValueError):
        normalize_ip("abc")

def test_normalize_ip_ok():
    assert normalize_ip("192.168.1.5") == "192.168.1.5"
    assert normalize_ip("2001:0db8::0001") == "2001:db8::1"


@patch("core.blocker.run")
def test_block_ip_success(mock_run):
    mock_run.return_value = ExecResult(True, 0, "", "")
    result = block_ip("192.168.1.5")
    assert result["success"] is True
    assert result["ip"] == "192.168.1.5"
    assert "-A" in result["command"]
    mock_run.assert_called_once()
    

def test_block_ip_invalid():
    result = block_ip("abc") 
    assert result["success"] is False
    assert "Невалидный" in result["error"]

@patch("core.blocker.run")
def test_unblock_ip_success(mock_run):
    mock_run.return_value = ExecResult(True, 0, "", "")
    result = unblock_ip("192.168.1.5")
    assert result["success"] is True
    assert result["ip"] == "192.168.1.5"
    assert "-D" in result["command"]
    mock_run.assert_called_once()