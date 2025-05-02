import pandas as pd
import random
from flask import Flask, jsonify, request

app = Flask(__name__)

# Load the dataset (adjust path if needed)
quotes_df = pd.read_csv("quotes_trimmed.csv")  # Ensure the file is in the same directory

@app.route('/quote', methods=['GET'])
# It give only , random and category quote.No author
def get_random_quote():
    # Get the 'category' from URL query (e.g., /quote?category=life)
    category = request.args.get('category', default=None, type=str)
    
    if category:
        # Filter quotes containing the category (case-insensitive)
        filtered_quotes = quotes_df[
            quotes_df['category'].str.contains(category, case=False, na=False)
        ]
    else:
        # If no category given, return any random quote
        filtered_quotes = quotes_df
    
    if len(filtered_quotes) == 0:
        return jsonify({"error": "No quotes found for this category"}), 404
    
    # Pick a random quote
    random_quote = filtered_quotes.sample(1).iloc[0]
    
    return jsonify({
        "quote": random_quote['quote'],
        "author": random_quote['author'],
        "categories": random_quote['category']
    })

if __name__ == '__main__':
    app.run(debug=True)  # Run locally for testing