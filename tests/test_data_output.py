#tests/test_data_output.py

import pandas as pd

from src import save_data


def test_save_data_creates_csv(sample_df, tmp_path):
    output_path = tmp_path / "clean.csv"
    outpath = save_data(sample_df, output_path)
    assert outpath == output_path

    df = pd.read_csv(outpath)
    assert df.shape == sample_df.shape
