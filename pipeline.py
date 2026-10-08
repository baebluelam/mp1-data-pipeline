"""
Complete Data Processing Pipeline

DS 3500 - MP1

Usage:
    python pipeline.py \
        --input fixtures/sample_data.csv \
        --output output/clean.csv \
        --config config/config.yaml \
        --verbose
"""

import argparse
import logging
import sys

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


def main():
    """Run the complete data-processing pipeline."""

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

    validation_config = config["validation"]
    required_columns = validation_config["required_columns"]
    numeric_columns = validation_config["numeric_columns"]

    rows_before_validation = len(data)

    try:
        validated_data = validate_dataframe(
            data,
            required_columns,
            numeric_columns
        )
    except ValueError as error:
        logger.error(error)
        sys.exit(1)

    logger.info(
        f"Validation complete: "
        f"{rows_before_validation} -> {len(validated_data)} rows"
    )

    data_before = validated_data.copy()

    try:
        cleaned_data = process_data(
            validated_data,
            config
        )
    except ValueError as error:
        logger.error(error)
        sys.exit(1)

    report = create_cleaning_report(
        data_before,
        cleaned_data
    )

    logger.info(
        f"Processing complete: "
        f"{len(data_before)} -> {len(cleaned_data)} rows"
    )

    output_path = save_data(
        cleaned_data,
        args.output
    )

    logger.info(
        f"Saved cleaned data to {output_path}"
    )

    print("\nCleaning report:")
    print(report)


if __name__ == "__main__":
    main()