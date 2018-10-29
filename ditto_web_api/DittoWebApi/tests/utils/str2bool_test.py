import pytest

from DittoWebApi.src.utils.parse_strings import str2bool


def test_str2bool_parses_lower_case_true():
    # Arrange
    string = "true"
    # Act
    result = str2bool(string)
    # Assert
    assert result is True


def test_str2bool_parses_lower_case_false():
    # Arrange
    string = "false"
    # Act
    result = str2bool(string)
    # Assert
    assert result is False


def test_str2bool_parses_upper_case_true():
    # Arrange
    string = "TRUE"
    # Act
    result = str2bool(string)
    # Assert
    assert result is True


def test_str2bool_parses_upper_case_false():
    # Arrange
    string = "FALSE"
    # Act
    result = str2bool(string)
    # Assert
    assert result is False


def test_str2bool_raises_value_error():
    with pytest.raises(ValueError) as exception_info:
        string = "maybe"
        str2bool(string)
    assert str(exception_info.value) == "'maybe' not recognised as a Boolean. Use 'True' or 'False' (case insensitive)."
