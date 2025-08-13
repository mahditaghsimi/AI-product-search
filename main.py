from backend.ai_clints.open_ai_clint import run_open_ai_clints
from backend.features.extract_features import run_extract_features
from backend.features.feature_similarity.feature_similarity import run_feature_similarity
from backend.similarity_analysis.calculate_euclidean_distance import run_calculate_distance
from backend.similarity_analysis.show_answer import run_show_answer
import pandas as pd

# Paths to the main dataset CSV and the output CSV for search results
main_data_csv = r"C:\Users\mahdi\OneDrive\Desktop\Smart_Product_Finder\data\cats_prds_all.csv"
export_csv_path = r"C:\Users\mahdi\OneDrive\Desktop\Smart_Product_Finder\data\search_results.csv"

def run_pipeline(raw_content: str):
    """
    Executes the full search pipeline:
    1. Sends the raw user query to the AI client for processing.
    2. Extracts structured product features from the AI output.
    3. Calculates feature similarity against the dataset.
    4. Calculates Euclidean distance from the similarity scores.
    5. Retrieves the top matching products and outputs them as a list of dictionaries.

    :param raw_content: Raw text from the user, which may contain product requirements in Persian/English.
    :return: List of dictionaries containing product details (image, link, name, price, description).
    """
    # Step 1: Process the raw user query using the AI client
    ai_clints = run_open_ai_clints(raw_content)
    # Step 2: Extract product features from the AI's output
    features_dict = run_extract_features(ai_clints)  # Returns dict
    # Step 3: Calculate similarity for each product feature
    similarity_csv_path = run_feature_similarity(features_dict)  # Returns path to CSV
    # Step 4: Calculate Euclidean distance for ranking products
    distance_csv_path = run_calculate_distance(similarity_csv_path)  # Returns path to CSV
    # Step 5: Get the final matching products with details
    export_path = run_show_answer(distance_csv_path, main_data_csv, export_csv_path)

    # Read the exported search results
    df = pd.read_csv(export_path)
    # Prepare list for storing final product dictionaries
    products = []
    for _, row in df.iterrows():
        # Get first image from the product_images field
        image_url = ""
        if pd.notna(row.get("product_images")):
            images = str(row["product_images"]).split(",")
            image_url = images[0].strip()

        # Get product link
        link_url = ""
        if pd.notna(row.get("url")):
            link_url = str(row["url"]).strip()

        # Get product name
        name = ""
        if pd.notna(row.get("name")):
            name = str(row["name"]).strip()

        # Get product price
        price = ""
        if pd.notna(row.get("price")):
            price = str(row["price"]).strip()

        # Get product description
        description = ""
        if pd.notna(row.get("description")):
            description = str(row["description"]).strip()

        # Append product details to the list
        products.append({
            "image": image_url,
            "link": link_url,
            "name": name,
            "price": price,
            "description": description,
        })

    return products


if __name__ == "__main__":
    # Direct script test with a sample query
    raw_content = "exm"
    products = run_pipeline(raw_content)

    # import json
    # # Print the results with proper formatting and UTF-8 characters
    # print(json.dumps(products, ensure_ascii=False, indent=2))