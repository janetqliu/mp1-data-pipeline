# tests/test_data_validator.py

import pytest

from src import validate_dataframe


def test_validate_dataframe_removes_invalid_ratings(sample_df):
    required_columns = ["record_id","name","rating","category","status"]
    numeric_columns = ["rating"]
    df = validate_dataframe(sample_df, required_columns, numeric_columns)
    assert df.shape == (98, 5)


def test_validate_dataframe_with_missing_column(sample_df):
    required_columns = ["record_id","name","rating","category","status","hello"]
    numeric_columns = ["rating"]
    
    with pytest.raises(ValueError):
        validate_dataframe(sample_df, required_columns, numeric_columns)
