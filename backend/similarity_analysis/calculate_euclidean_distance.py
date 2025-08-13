import pandas as pd
import numpy as np
import os

def run_calculate_distance(output_csv):
    """
    Calculate the Euclidean distance for each product based on similarity scores.

    This function:
      1. Reads the feature similarity CSV (contains *_sim columns from previous step).
      2. Identifies all columns ending with '_sim' (feature similarity scores).
      3. Computes the Euclidean distance for each row as a combined similarity measure.
      4. Keeps only product ID, name, and distance.
      5. Sorts the results by the highest distance first.
      6. Saves the sorted results to a CSV file.

    :param output_csv: (str) Path to the feature similarity CSV file (currently unused directly; uses fixed path).
    :return: Path to the saved similarity analysis CSV file.
    """
    # Path to the similarity file (currently hardcoded)
    input_csv = r'C:\Users\mahdi\OneDrive\Desktop\Smart_Product_Finder\backend\features\feature_similarity\feature_similarity.csv'
    # Path to save the Euclidean distance analysis result
    similarity_analysis_output_csv = r'C:\Users\mahdi\OneDrive\Desktop\Smart_Product_Finder\backend\similarity_analysis\similarity_analysis.csv'
    # Ensure output directory exists
    output_dir = os.path.dirname(similarity_analysis_output_csv)
    os.makedirs(output_dir, exist_ok=True)

    # Step 1: Read the feature similarity CSV
    df = pd.read_csv(input_csv)
    # Step 2: Identify all similarity columns (ending with "_sim")
    sim_cols = [col for col in df.columns if col.endswith('_sim')]
    # Step 3: Compute Euclidean distance for each product
    # Replace NaN values with 0 to avoid calculation errors
    df['euclidean_distance'] = np.linalg.norm(df[sim_cols].fillna(0).values, axis=1)
    # Step 4: Keep only row_id, name, and Euclidean distance columns
    result = df[['row_id','name', 'euclidean_distance']].copy()
    # Step 5: Sort products by distance (highest first)
    result_sorted = result.sort_values('euclidean_distance', ascending=False)
    # Step 6: Save the sorted results to CSV
    result_sorted.to_csv(similarity_analysis_output_csv, index=False, encoding='utf-8-sig')
    print(f"✅ File created: {similarity_analysis_output_csv}")

    return similarity_analysis_output_csv