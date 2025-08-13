import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
import os


def run_feature_similarity(feat_queries):
    """
    Calculate similarity scores for each product in the dataset
    based on the provided feature-specific search queries.

    :param feat_queries: dict containing search strings for each feature
                         keys = ["name", "brand", "company_name", "categories", "description", "price"]
                         example: {"name": "gaming laptop", "brand": "Asus", "description": "lightweight"}
    :return: Path to the generated CSV file containing similarity scores.
    """
    # Paths & Settings
    BASE_DIR  = r'C:\Users\mahdi\OneDrive\Desktop\Smart_Product_Finder'
    input_csv = os.path.join(BASE_DIR, 'data', 'cats_prds_all.csv')# main product database
    save_dir = os.path.join(BASE_DIR, 'data', 'embedding_files')  # folder containing precomputed embeddings
    columns = ['name', 'brand', 'company_name', 'categories', 'description','price'] # features to compare
    model = SentenceTransformer('all-MiniLM-L6-v2')# embedding model for text similarity

    # Step 1: Load main product dataframe, replace NaN with empty strings
    df = pd.read_csv(input_csv).fillna("")
    # Step 2: Prepare result dataframe
    res_df = pd.DataFrame()
    res_df['row_id'] = df['row_id'] # keep original product row ID
    res_df['name'] = df['name']# product name is always kept (for reference)
    # Step 3: Iterate through each feature column and compute similarity scores
    for col in columns:
        query = feat_queries.get(col, "")# get the query for this feature
        if not query.strip():
            # If no query is provided for this feature → similarity = 0 for all rows
            res_df[f"{col}_sim"] = 0
            continue
        # Step 3.1: Load saved embeddings and unique value lists for this feature
        emb_file = f"{save_dir}/{col}_embeddings.npy"
        unique_file = f"{save_dir}/{col}_list.csv"
        unique_items = pd.read_csv(unique_file).iloc[:,0].astype(str).tolist()# unique feature values
        embeddings = np.load(emb_file)  # precomputed embeddings for unique values
        # Map each unique feature value to an index
        val2idx = {v: i for i, v in enumerate(unique_items)}
        # Map each product's feature value to its index in the unique list
        idxs = df[col].astype(str).map(val2idx).fillna(-1).astype(int)
        # Initialize similarity column with zeros
        sim_col = np.zeros(len(df))
        # Only compute similarity for products whose feature value exists in the unique list
        has_val = idxs >= 0
        query_vec = model.encode([query], normalize_embeddings=True)# encode query
        sim_col[has_val] = np.dot(embeddings[idxs[has_val]], query_vec.T).reshape(-1)
        # Assign this feature's similarity scores to the results dataframe
        res_df[f"{col}_sim"] = sim_col
     # Step 4: Save similarity results to CSV
    output_csv = r'C:\Users\mahdi\OneDrive\Desktop\Smart_Product_Finder\backend\features\feature_similarity\feature_similarity.csv'
    output_dir = os.path.dirname(output_csv)
    os.makedirs(output_dir, exist_ok=True)
    res_df.to_csv(output_csv, index=False, encoding='utf-8-sig')
    print(f'✅ Similarity table based on each feature query created: {output_csv}')
    return output_csv