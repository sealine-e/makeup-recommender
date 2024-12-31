import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load the dataset
df = pd.read_csv("main/sephora_website_dataset.csv")

# Remove any rows where the 'category' column is missing to avoid errors
df = df.dropna(subset=['category', 'price', 'rating', 'URL'])

df['category'] = df['category'].str.lower()

# Initialize TF-IDF Vectorizer (use the 'category' column for similarity)
tfidf_vectorizer = TfidfVectorizer(stop_words='english')

# Create a TF-IDF matrix for the 'category' column (or use 'name' or 'details' if needed)
tfidf_matrix = tfidf_vectorizer.fit_transform(df['details'])

# Compute cosine similarity between products based on the 'category' column
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)


# Example: Find similar products to a specific product by category
def get_similar_products(categories, price_min, price_max, rating_min, top_n):
    # Filter products by category, price, and rating
    filtered_df = []
    for category in categories:
        filtered_df = df[
            (df['category'].str.contains(category)) &
            (df['price'] >= price_min) &
            (df['price'] <= price_max) &
            (df['rating'] >= rating_min)
            ]

    # Compute cosine similarity within the filtered dataframe
    filtered_indices = filtered_df.index
    filtered_sim_matrix = cosine_sim[filtered_indices][:, filtered_indices]

    # Find the most similar products (by averaging across the category similarity)
    mean_sim_scores = filtered_sim_matrix.mean(axis=1)
    sorted_indices = mean_sim_scores.argsort()[::-1][:top_n]

    # Get the most similar products from the filtered dataframe
    sim_products = filtered_df.iloc[sorted_indices]

    return sim_products[['name', 'brand', 'category', 'price', 'rating', 'URL']]


# Example usage: Get similar products to 'foundation' (replace with your actual product name)
categories_list = ['foundation',
                   'concealer']  # Example product name, replace with the actual product you're interested in
similar_products = get_similar_products(categories_list, 20.00, 50.00, 4.0, 5)

# Display the recommended products
if similar_products.empty:
    print("No similar products found.")
else:
    print("Recommended Products Similar to", categories_list)
    print(similar_products)
