# AI-product-search
AI-based engine for finding the best matching products from a dataset using vector embeddings.

## Features
- Processes and tokenizes user input using an AI API and a selected language model.
- Accepts user search queries via HTML input form.
- Embeds the primary dataset to enable faster and more accurate semantic searches.
- Compares user queries against the original dataset for precise matching.
- Selects the most relevant result using Euclidean distance–based ranking.
- Works seamlessly with any product dataset in CSV or Excel format.
- Easily configurable and extendable for different e-commerce use cases.

## Usage
1. In the backend folder:
   - Inside the `ai_clients` and `api` directories, place your API credentials or configuration files.
2. Place your dataset file in the `data` folder.
3. Load the dataset and use the embedding script inside the `backend` folder to generate vector embeddings.
4. Verify that all required files exist and update the file paths in the code to match your system’s directory structure.
5. Run the application:
```bash
python app.py
