import argparse
import duckdb
import os
from loguru import logger


def create_tpch_tables(scaling_factor=1):
    """
    Create TPC-H tables in DuckDB with the specified scaling factor.

    Args:
        scaling_factor (float): The scaling factor for TPC-H dataset generation.

    Returns:
        DuckDB connection with TPC-H tables loaded.
    """
    logger.info(f"Starting TPC-H table creation with scaling factor {scaling_factor}")

    conn = duckdb.connect(database=":memory:")

    # Generate TPC-H data using DuckDB's built-in TPC-H generator
    conn.execute(f"CALL dbgen(sf={scaling_factor});")

    logger.success(f"TPC-H tables created with scaling factor {scaling_factor}")

    return conn


def create_tpch_dataset(conn, format, output_folder_path):
    """
    Write all TPC-H tables to individual files in the specified format.

    Args:
        conn: DuckDB connection with TPC-H tables.
        format (str): Output file format ('csv', 'parquet', or 'json').
        output_folder_path (str): Directory where files will be saved.
    """
    logger.info(
        f"Starting export of TPC-H tables to {format} format in {output_folder_path}"
    )

    # Ensure the output directory exists
    os.makedirs(output_folder_path, exist_ok=True)

    # Get all TPC-H table names
    tables = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
    ).fetchall()
    table_names = [table[0] for table in tables]

    logger.info(f"Found {len(table_names)} tables to export")

    # Write each table to a file
    for table in table_names:
        output_path = os.path.join(output_folder_path, f"{table}.{format}")
        logger.info(f"Exporting {table} to {output_path}")

        if format.lower() == "csv":
            conn.execute(f"COPY {table} TO '{output_path}' (HEADER, DELIMITER ',');")
        elif format.lower() == "parquet":
            conn.execute(f"COPY {table} TO '{output_path}';")
        elif format.lower() == "json":
            conn.execute(f"COPY {table} TO '{output_path}' (FORMAT JSON);")
        else:
            raise ValueError(f"Unsupported format: {format}")

        logger.success(f"Exported {table} to {output_path}")

    logger.success(f"All tables exported successfully to {format} format")


def run(scaling_factor, format, output_folder_path):
    """
    Run the full pipeline to create TPC-H tables and export them.

    Args:
        scaling_factor (float): The scaling factor for TPC-H dataset generation.
        format (str): Output file format ('csv', 'parquet', or 'json').
        output_folder_path (str): Directory where files will be saved.
    """
    logger.info("Starting TPC-H dataset generation pipeline")

    conn = create_tpch_tables(scaling_factor)
    create_tpch_dataset(conn, format, output_folder_path)

    logger.success(
        f"TPC-H dataset with scaling factor {scaling_factor} has been generated in {output_folder_path}"
    )


if __name__ == "__main__":
    # Configure logger
    logger.remove()

    logger.add(
        sink=lambda msg: print(msg),
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>",
    )
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Generate TPC-H dataset using DuckDB")
    parser.add_argument(
        "--sf",
        "--scaling-factor",
        dest="scaling_factor",
        type=float,
        default=0.5,
        help="Scaling factor for TPC-H dataset (default: 0.5)",
    )
    parser.add_argument(
        "--format",
        type=str,
        choices=["csv", "parquet", "json"],
        default="csv",
        help="Output file format (default: csv)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="./data",
        help="Output folder path (default: current directory)",
    )

    args = parser.parse_args()

    logger.info("Parsed command line arguments")

    # Run the pipeline
    run(args.scaling_factor, args.format, args.output)
