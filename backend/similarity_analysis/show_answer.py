
import pandas as pd

# File paths (currently hardcoded)
similarity_analysis_output_csv = r'C:\Users\mahdi\OneDrive\Desktop\Smart_Product_Finder\backend\similarity_analysis\similarity_analysis.csv'
main_data_csv = r'C:\Users\mahdi\OneDrive\Desktop\Smart_Product_Finder\data\cats_prds_all.csv'
export_csv = r'C:\Users\mahdi\OneDrive\Desktop\Smart_Product_Finder\data\search_results.csv'

def run_show_answer(similarity_analysis_output_csv, main_data_csv, export_csv):
    """
    Retrieves the top 15 most relevant products (based on Euclidean distance)
    and exports them with full product details.

    Steps:
      1. Reads the similarity analysis CSV (contains euclidean_distance for each product).
      2. Sorts products by distance in descending order (most similar first).
      3. Picks the top 15 products.
      4. Uses row_id to match these top products with the full main dataset.
      5. Preserves the ranking order from the similarity analysis.
      6. Saves the matched full product info to a new CSV file.

    :param similarity_analysis_output_csv: Path to CSV containing 'row_id' and 'euclidean_distance'.
    :param main_data_csv: Path to the main full product data CSV.
    :param export_csv: Path to save the top-15 product details.
    :return: Path to the saved CSV file containing top-15 detailed results.
    """
    # Step 1: Read similarity analysis results
    df_output = pd.read_csv(similarity_analysis_output_csv)
    #Step 2: Pick top 15 products by highest Euclidean distance
    top15 = df_output.sort_values('euclidean_distance', ascending=False).head(15)
    # Step 3: Get row_ids of these products
    top15_ids = top15['row_id'].tolist()
    # Step 4: Read main product dataset
    df_main = pd.read_csv(main_data_csv)
    # Step 5: Filter products whose row_id matches top15_ids
    # Use loc with the original order preserved
    df_matched = df_main[df_main['row_id'].isin(top15_ids)]
    df_matched = df_matched.set_index('row_id').loc[top15_ids].reset_index()
    # Step 6: Save the results to CSV
    df_matched.to_csv(export_csv, index=False, encoding="utf-8-sig")

    print(f"✅ The file '{export_csv}' containing detailed information of the same 15 products has been created.")
    return export_csv



