import pandas as pd
import numpy as np
import os
import random
from pathlib import Path


def create_incomplete_dataset(input_file, output_file, missing_percentage=0.25, seed=42):
    """
    Create a new dataset with a specified percentage of missing values filled with "UNKNOWN".

    Parameters:
    -----------
    input_file : str
        Path to the input file
    output_file : str
        Path to save the output file
    missing_percentage : float
        Percentage of values to remove (between 0 and 1)
    seed : int
        Random seed for reproducibility
    """
    # Set random seed for reproducibility
    np.random.seed(seed)
    random.seed(seed)

    # Read the input file
    print(f"Reading data from {input_file}...")
    df = pd.read_csv(input_file)

    # Get the columns to modify (excluding drug identifier columns)
    columns_to_preserve = ['Drug1', 'Drug2', 'Drug1 ID', 'Drug2 ID', 'Unnamed: 0']
    columns_to_modify = [col for col in df.columns if col not in columns_to_preserve]

    # If no valid columns to modify, print a warning
    if not columns_to_modify:
        print(f"Warning: No columns to modify in {input_file}. Check column names.")
        return {
            "original_rows": len(df),
            "modified_rows": len(df),
            "target_missing_percentage": missing_percentage * 100,
            "actual_missing_percentage": 0,
            "columns_modified": []
        }

    # Calculate the total number of cells to modify
    total_cells = len(df) * len(columns_to_modify)
    cells_to_modify = int(total_cells * missing_percentage)

    print(f"Total modifiable cells: {total_cells}")
    print(f"Cells to make UNKNOWN: {cells_to_modify} ({missing_percentage * 100:.1f}%)")
    print(f"Columns being modified: {columns_to_modify}")

    # Create a copy of the dataframe to modify
    modified_df = df.copy()

    # Create a list of all possible (row, column) combinations
    all_positions = [(row, col) for row in range(len(df)) for col in columns_to_modify]

    # Randomly select positions to make values UNKNOWN
    positions_to_modify = random.sample(all_positions, cells_to_modify)

    # Set the selected positions to "UNKNOWN"
    for row, col in positions_to_modify:
        modified_df.loc[row, col] = "UNKNOWN"

    # Calculate the actual percentage of UNKNOWN values
    unknown_count = sum(1 for row, col in positions_to_modify)
    actual_missing = unknown_count / total_cells
    print(f"Actual UNKNOWN percentage: {actual_missing * 100:.2f}%")

    # Save the modified dataframe
    modified_df.to_csv(output_file, index=False)
    print(f"Modified data saved to {output_file}")

    # Return statistics
    return {
        "original_rows": len(df),
        "modified_rows": len(modified_df),
        "target_missing_percentage": missing_percentage * 100,
        "actual_missing_percentage": actual_missing * 100,
        "columns_modified": columns_to_modify
    }


def main():
    # Configuration
    random_seed = 42
    missing_percentage = 0.28  # Targeting 28% missing data

    # Create output directory if it doesn't exist
    output_dir = Path("incomplete_data")
    output_dir.mkdir(exist_ok=True)

    # Process File 1
    file1_input = "all_id_interaction_chunk_1.csv"
    file1_output = output_dir / "incomplete_all_id_interaction_chunk_1.csv"

    # Process File 2
    file2_input = "data_final_v5.csv"  # Update with your actual filename
    file2_output = output_dir / "incomplete_data_final_v5_chunk_1.csv"

    # Process both files
    stats1 = create_incomplete_dataset(file1_input, file1_output, missing_percentage, random_seed)
    stats2 = create_incomplete_dataset(file2_input, file2_output, missing_percentage, random_seed)

    # Print summary
    print("\nSummary:")
    print(f"File 1: {stats1['actual_missing_percentage']:.2f}% missing data")
    print(f"File 2: {stats2['actual_missing_percentage']:.2f}% missing data")


if __name__ == "__main__":
    main()