import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import plotly.express as px
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import LabelEncoder

# Read csv and select desired columns
df = pd.read_csv("sephora_website_dataset.csv")
df_filtered = df[['id', 'brand', 'name', 'category', 'price', 'rating', 'number_of_reviews']]

# Preprocessing: Convert categorical columns to numeric using Label Encoding
label_encoder_brand = LabelEncoder()
label_encoder_category = LabelEncoder()

# Fit the encoders on the full dataset
df_filtered['brand_encoded'] = label_encoder_brand.fit_transform(df_filtered['brand'])
df_filtered['category_encoded'] = label_encoder_category.fit_transform(df_filtered['category'])

# Normalize price and rating (optional, but can improve model performance)
df_filtered['price_normalized'] = (df_filtered['price'] - df_filtered['price'].min()) / (df_filtered['price'].max() - df_filtered['price'].min())
df_filtered['rating_normalized'] = (df_filtered['rating'] - df_filtered['rating'].min()) / (df_filtered['rating'].max() - df_filtered['rating'].min())

# Example user preferences (this could be dynamic)
user_preferences = {
    "preferred_brands": ["NARS", "Fenty Beauty"],
    "preferred_categories": ["Foundation", "Lipstick"],
    "price_range": (20, 50),
    "min_rating": 4.0
}

# Encode user preferences using the same label encoder
user_pref_brands_encoded = label_encoder_brand.transform(user_preferences['preferred_brands'])
user_pref_categories_encoded = label_encoder_category.transform(user_preferences['preferred_categories'])

# Filter dataset based on user preferences
user_filtered = df_filtered[
    (df_filtered['brand'].isin(user_preferences['preferred_brands'])) &
    (df_filtered['category'].isin(user_preferences['preferred_categories'])) &
    (df_filtered['price'] >= user_preferences['price_range'][0]) &
    (df_filtered['price'] <= user_preferences['price_range'][1]) &
    (df_filtered['rating'] >= user_preferences['min_rating'])
]

# Create user preference vector: Weights for brands, categories, price, and rating
user_vector = []
user_vector.extend(user_pref_brands_encoded)
user_vector.extend(user_pref_categories_encoded)
user_vector.extend([ (user_preferences['price_range'][0] + user_preferences['price_range'][1]) / 2, user_preferences['min_rating']])

# Use cosine similarity to recommend products based on user's preferences
def recommend_based_on_user_preferences(user_vector, df_filtered):
    # Create a feature vector for each product (e.g., brand, category, price, rating)
    product_features = df_filtered[['brand_encoded', 'category_encoded', 'price_normalized', 'rating_normalized']]

    # Reshape user preferences and calculate cosine similarity with products
    similarity_scores = cosine_similarity([user_vector], product_features)

    # Add similarity scores to the DataFrame
    df_filtered['similarity_score'] = similarity_scores[0]

    # Sort products by similarity score and return the top recommendations
    recommended_products = df_filtered.sort_values(by='similarity_score', ascending=False)

    return recommended_products

# Get top 10 recommendations
recommended_products = recommend_based_on_user_preferences(user_vector, df_filtered)
print(recommended_products[['name', 'brand', 'category', 'price', 'rating', 'similarity_score']].head(10))

# Visualize recommendations (optional)
fig = px.bar(
    recommended_products.head(10),
    x='name',
    y='rating',
    color='price',
    hover_data=['brand', 'category'],
    title="Recommended Products"
)
fig.show()
