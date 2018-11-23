import pytest

from DittoWebApi.src.utils.parse_strings import str2list


@pytest.mark.parametrize("string", ["a,1,foobar", "a, 1, foobar", "a,   1, foobar", ])
def test_str2list_splits_any_padded_string_with_default_settings(string):
    result = str2list(string)
    assert result == ["a", "1", "foobar"]

