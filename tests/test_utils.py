# filepath: /c:/repositorios/cuidar/cuidar_plus_api/tests/test_utils.py
import pytest
from routes.utils import validate_cpf, sanitize_input

def test_validate_cpf_valid():
    assert validate_cpf("12345678909")

def test_validate_cpf_invalid():
    assert not validate_cpf("12345678900")
    assert not validate_cpf("11111111111")
    assert not validate_cpf("")

def test_sanitize_input():
    assert sanitize_input("<script>alert('xss')</script>") == "&lt;script&gt;alert('xss')&lt;/script&gt;"
    assert sanitize_input("   valid input   ") == "valid input"
    with pytest.raises(ValueError):
        sanitize_input("a" * 101)

def test_functional_validate_cpf():
    valid_cpfs = ["12345678909", "98765432100"]
    invalid_cpfs = ["12345678900", "11111111111", ""]
    for cpf in valid_cpfs:
        assert validate_cpf(cpf)
    for cpf in invalid_cpfs:
        assert not validate_cpf(cpf)

def test_functional_sanitize_input():
    inputs = {
        "<script>alert('xss')</script>": "&lt;script&gt;alert('xss')&lt;/script&gt;",
        "   valid input   ": "valid input",
        "a" * 101: ValueError
    }
    for input_str, expected_output in inputs.items():
        if expected_output is ValueError:
            with pytest.raises(ValueError):
                sanitize_input(input_str)
        else:
            assert sanitize_input(input_str) == expected_output
