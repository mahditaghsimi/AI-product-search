from flask import Flask, render_template, request, jsonify
from main import run_pipeline

app = Flask(
    __name__,
    template_folder="chat_bot/templates", # Path to HTML template files
    static_folder="chat_bot/static"       # Path to static files (CSS, JS, images)
)
# Temporary in-memory cache to store last search results
products_cache = []

@app.route("/")
def index():
    """Renders the home page with the search form/UI."""
    return render_template("index.html")

@app.route("/api/search", methods=["POST"])
def search_products():
    """
    API endpoint for product search.
    - Receives JSON with a 'message' key from the frontend.
    - Passes the message to run_pipeline() from main.py to get search results.
    - Stores results in products_cache for later use on the detail page.
    - Returns the products as JSON.
    """
    global products_cache
    data = request.get_json()
    raw_content = data.get("message", "").strip()
    # Check if the search message is empty
    if not raw_content:
        return jsonify({"error": "Please enter a message"}), 400
    try:
        # Call the pipeline to get a list of products ready for display
        products = run_pipeline(raw_content)
        # Save products temporarily in memory for detail page access
        products_cache = products
        # Return the products as JSON
        return jsonify(products)
    except Exception as e:
        print("❌ Error:", e)
        return jsonify({"error": str(e)}), 500


@app.route("/product/<int:pid>")
def product_details(pid):
    """
       Renders the product details page for a specific product.
       - pid: product index from search results.
       - Looks up the product in products_cache.
       - Renders details.html with the selected product information.
       """
    if pid < 0 or pid >= len(products_cache):
        return "Product not found", 404
    product = products_cache[pid]
    return render_template("details.html", product=product)


if __name__ == "__main__":
    # Run the Flask app in debug mode for development
    app.run(debug=True)
