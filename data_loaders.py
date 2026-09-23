# data_loaders.py
from pathlib import Path

import logging
import pandas as pd
import json
import yaml


# Do not call logging.basicConfig() here.
# Use the logging configuration from Part 1.
logger = logging.getLogger(__name__)


def setup_logging(verbose=False):
    """Configure logging for the pipeline."""
    logging.basicConfig(
    level=logging.DEBUG if verbose else logging.INFO,
    format="%(asctime)s %(levelname)-8s %(message)s",
    datefmt="%H:%M:%S"
    )


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="check quality of csv file")

    parser.add_argument(
        "--input",
        "-i",
        required=True,
        help="path to input file"
    )

    parser.add_argument(
        "--output",
        "-o",
        required=True,
        help="path to output file"
    )

    parser.add_argument(
        "--format",
        default="csv",
        choices=["csv", "json"],
        help="output format (csv or json, default csv)" 
    )

    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="enable verbose logging"
    )

    args = parser.parse_args()

    return args


def validate_input(filepath):
    """Check whether the input path exists and is a file."""
    p = Path(filepath)
    if p.is_file():
        logger.info(f"Input file validated: {filepath}")
        return True
    if not p.is_file():
        logger.error(f"Input file not found: {filepath}")
        return False


def load_csv(filepath):
    """Load a CSV file into a DataFrame."""
    df = pd.read_csv(filepath)
    logger.info(f"Loaded CSV file: {filepath} ({len(df)} rows)")
    return df


def load_json(filepath):
    """Load a JSON file into a Python object (dict or list)."""
    with open(filepath, "r") as file:
        data = json.load(file)
        logger.info(f"Loaded JSON file: {filepath}")
        return data


def load_yaml(filepath):
    """Load a YAML file into a Python object."""
    with open(filepath, "r") as file:
        config = yaml.safe_load(file)
        logger.info(f"Loaded YAML file: {filepath}")



def load_data(filepath):
    """Load a file based on its extension."""
    data = Path(filepath)
    if data.suffix == ".csv":
        return load_csv(data)
    elif data.suffix == ".json":
        return load_json(data)
    elif data.suffix == ".yaml":
        return load_yaml(data)
    else:
        logger.error(f"Unsupported file format: {data.suffix}")
        raise ValueError("Unsupported file format.")


