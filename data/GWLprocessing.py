import pandas as pd

def process_groundwater_data(input_csv_path, output_csv_path):
    """
    Calculates the weighted average depth to the water table from binned well data.

    Args:
        input_csv_path (str): The path to the input CSV file.
        output_csv_path (str): The path where the processed CSV will be saved.
    """
    try:
        midpoints = {
            '0-2': 1.0,
            '2-5': 3.5,
            '5-10': 7.5,
            '10-20': 15.0,
            '20-40': 30.0,
            '>40': 45.0 
        }

        # Load the dataset from the CSV file
        df = pd.read_csv(input_csv_path)

        # Initialize a new column to store the weighted sum
        df['Weighted_Sum'] = 0

        # Calculate the weighted sum for each district (row)
        for col_name, midpoint_val in midpoints.items():
            # Check if the column exists in the dataframe to avoid errors
            if col_name in df.columns:
                df['Weighted_Sum'] += df[col_name] * midpoint_val

        # Calculate the final weighted average
        # The column for total wells is named 'No. of Wells Analysed' in the image
        total_wells_col = 'No. of Wells Analysed'
        df['Weighted_Avg_Depth'] = df['Weighted_Sum'] / df[total_wells_col]

        # Create a new, clean dataframe with only the required output
        result_df = df[['District', 'Weighted_Avg_Depth']].copy()
        
        # Round the result to two decimal places for clarity
        result_df['Weighted_Avg_Depth'] = result_df['Weighted_Avg_Depth'].round(2)

        # Save the processed data to a new CSV file
        result_df.to_csv(output_csv_path, index=False)

        print("Processing complete.")
        print(f"Processed data saved to: {output_csv_path}")
        print("\nFirst 5 rows of the processed data:")
        print(result_df.head())

    except FileNotFoundError:
        print(f"Error: The file '{input_csv_path}' was not found.")
    except KeyError as e:
        print(f"Error: A required column is missing from the CSV file: {e}")
        print("Please ensure your CSV has a 'District' column, a total wells column, and columns for the depth ranges.")

# --- How to use the function ---
if __name__ == "__main__":
    # Define the input and output file paths
    input_file = 'GWlevelAugust.csv'  # The name of your data file
    output_file = 'processedGWLAugust.csv' # The name for the output file

    # Run the processing function
    process_groundwater_data(input_file, output_file)