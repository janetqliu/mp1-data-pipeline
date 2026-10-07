"""
Data Processing Pipeline - CLI Template

DS 3500 - MP1

"""

import argparse
import logging
import sys
from pathlib import Path
from src import (
    create_cleaning_report,
    load_data,
    process_data,
    save_data,
    setup_logging,
    validate_dataframe,
    validate_input,
)


logger = logging.getLogger(__name__)


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="data parsing pipeline")

    parser.add_argument(
        "--input",
        "-i",
        required=True,
        help="path to input file"
    )

    parser.add_argument(
        "--config",
        "-c",
        required=True,
        help="path to yaml config file"
    )

    parser.add_argument(
        "--output",
        "-o",
        required=True,
        help="path to output file"
    )

    # parser.add_argument(
    #     "--format",
    #     default="csv",
    #     choices=["csv", "json"],
    #     help="output format (csv or json, default csv)" 
    # )

    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="enable verbose logging"
    )

    args = parser.parse_args()

    return args


def main():
    """Main pipeline function."""
    args = parse_arguments()

    setup_logging(verbose=args.verbose)

    logger.debug(f"Arguments parsed: input={args.input}, config={args.config}, output={args.output}")

    if not validate_input(args.input):
        sys.exit(1)

    if not validate_input(args.config):
        sys.exit(1)

    try:
        data = load_data(args.input)
        config = load_data(args.config)
        
    except ValueError as e:
        logger.error(f"Failed to load data/config: {e}")
        sys.exit(1)

    required_columns = config["validation"]["required_columns"]
    numeric_columns = config["validation"]["numeric_columns"]

    df_before = data.copy()

    try:
        df = validate_dataframe(data, required_columns, numeric_columns)
    except ValueError as e:
        logger.error(f"Failed to validate dataframe: {e}")
        sys.exit(1)

    logger.info(f"Rows before validating: {len(df_before)} | Rows after: {len(df)}")

    df_before2 = data.copy()

    try:
        df_after = process_data(df, config)
    except ValueError as e:
        logger.error(f"Failed to process data: {e}")
        sys.exit(1)

    logger.info(f"Processing complete: {len(df_before2)} -> {len(df_after)} rows")

    outpath = save_data(df_after, args.output)
    logger.info(f"Saved data successfully to {args.output}")

    report = create_cleaning_report(df_before2, df_after)

    print(report)

if __name__ == "__main__":
    main()