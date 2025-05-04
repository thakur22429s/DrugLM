import pandas as pd
import os
import sys
from pathlib import Path


def split_csv_by_size(input_file, output_dir, max_chunk_size_mb=25):
    """
    Split a CSV file into smaller chunks based on size

    Args:
        input_file (str): Path to the input CSV file
        output_dir (str): Directory to save the output chunks
        max_chunk_size_mb (int): Maximum size of each chunk in MB
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Get file basename
    base_name = Path(input_file).stem

    # Read the CSV file
    print(f"Reading {input_file}...")
    df = pd.read_csv(input_file)

    # Calculate approximate row size
    total_file_size = os.path.getsize(input_file)
    row_count = len(df)
    approx_row_size_bytes = total_file_size / row_count if row_count > 0 else 0

    # Calculate rows per chunk based on max size
    max_size_bytes = max_chunk_size_mb * 1024 * 1024  # Convert MB to bytes
    rows_per_chunk = int(max_size_bytes / approx_row_size_bytes) if approx_row_size_bytes > 0 else 5000

    # Ensure we have at least some rows per chunk
    rows_per_chunk = max(1000, rows_per_chunk)

    # Calculate number of chunks
    num_chunks = (row_count + rows_per_chunk - 1) // rows_per_chunk

    print(f"Splitting {input_file} into approximately {num_chunks} chunks...")
    print(f"Total rows: {row_count}, Rows per chunk: {rows_per_chunk}")

    # Split the dataframe and save chunks
    for i in range(0, row_count, rows_per_chunk):
        chunk_df = df.iloc[i:i + rows_per_chunk]
        chunk_num = i // rows_per_chunk + 1
        output_file = os.path.join(output_dir, f"{base_name}_chunk_{chunk_num}.csv")

        # Save the chunk
        chunk_df.to_csv(output_file, index=False)

        # Verify chunk size
        chunk_size_mb = os.path.getsize(output_file) / (1024 * 1024)
        print(f"Created {output_file}: {chunk_df.shape[0]} rows, {chunk_size_mb:.2f} MB")


def main():
    if len(sys.argv) < 3:
        print("Usage: python split_csv.py <input_file> <output_directory> [max_chunk_size_mb]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_dir = sys.argv[2]
    max_chunk_size_mb = 25  # Default

    if len(sys.argv) >= 4:
        try:
            max_chunk_size_mb = int(sys.argv[3])
        except ValueError:
            print("Error: max_chunk_size_mb must be an integer")
            sys.exit(1)

    split_csv_by_size(input_file, output_dir, max_chunk_size_mb)


if __name__ == "__main__":
    main()