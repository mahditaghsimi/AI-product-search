import pandas as pd
from sentence_transformers import SentenceTransformer
import numpy as np
from data.process import df
import os

model = SentenceTransformer('all-MiniLM-L6-v2')
columns = ['name', 'company_name', 'categories', 'brand', 'description','price']

save_dir = os.path.join('Smart_Product_Finder', 'data', 'embedding_files')
os.makedirs(save_dir, exist_ok=True)

for col in columns:
    # Get unique values and clean up
    unique_items = df[col].drop_duplicates().fillna('').astype(str).tolist()
    print(f"{col}: Unic num: {len(unique_items)}")

    # Generate embeddings
    embeddings = model.encode(unique_items, show_progress_bar=True, batch_size=64, normalize_embeddings=True)
    print(f'Embeddings shape for {col}:', embeddings.shape)

    # Save outputs (names + embeddings)
    np.save(os.path.join(save_dir, f"{col}_embeddings.npy"), embeddings)
    pd.Series(unique_items).to_csv(os.path.join(save_dir, f"{col}_list.csv"), index=False)
