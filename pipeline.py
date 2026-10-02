"""
Data Processing Pipeline

DS 3500 - MP1

Usage:
    python pipeline.py --input fixtures/sample.csv \
        --output cleaned_data.csv --config config.yaml
"""

import argparse
import logging
import sys
from pathlib import Path

from data_loaders import load_data
from data_processor import process_data, create_cleaning_report


logger = logging.getLogger(__name__)


def setup_logging(verbose=False):
    """Configure logging for the pipeline."""

    if verbose:
        level = logging.DEBUG
    else:
        level = logging.INFO

    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
        datefmt="%H:%M:%S"
    )


def parse_arguments():
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser(
        description="Data Processing Pipeline"
    )

    parser.add_argument(
        "--input",
        "-i",
        required=True,
        help="Path to the input file"
    )

    parser.add_argument(
        "--config",
        "-c",
        required=True,
        help="Path to the YAML configuration file"
    )

    parser.add_argument(
        "--output",
        "-o",
        required=True,
        help="Path to the output CSV file"
    )

    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose logging"
    )

    return parser.parse_args()


def validate_input(filepath):
    """Check whether the input path exists and is a file."""

    if Path(filepath).is_file():
        logger.info(f"Input file validated: {filepath}")
        return True

    logger.error(f"Input file not found: {filepath}")
    return False


def main():
    """Run the data-processing pipeline."""

    args = parse_arguments()
    setup_logging(args.verbose)

    logger.debug(
        f"Arguments parsed: input={args.input}, "
        f"output={args.output}, config={args.config}"
    )

    if not validate_input(args.input):
        sys.exit(1)

    if not validate_input(args.config):
        sys.exit(1)

    try:
        data = load_data(args.input)
        config = load_data(args.config)
    except ValueError as error:
        logger.error(error)
        sys.exit(1)

    data_before = data.copy()

    try:
        cleaned_data = process_data(data, config)
    except ValueError as error:
        logger.error(error)
        sys.exit(1)

    report = create_cleaning_report(
        data_before,
        cleaned_data
    )

    print(report)

    logger.info(
        f"Processing complete: "
        f"{len(data_before)} → {len(cleaned_data)} rows"
    )

    cleaned_data.to_csv(args.output, index=False)

    logger.info(f"Saved cleaned data to {args.output}")


if __name__ == "__main__":
    main()