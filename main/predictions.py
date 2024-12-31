import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Read CSV and select desired columns
df = pd.read_csv("main/sephora_website_dataset.csv")
df_filtered = df[['id', 'brand', 'name', 'category', 'price', 'rating', 'number_of_reviews']]

# Safely modify df_filtered using .loc[]
df_filtered.loc[:, 'collaborative_rating'] = np.random.uniform(3.5, 5.0, size=len(df_filtered))

print(df_filtered.head())

# Connect to SQLite database
conn = sqlite3.connect("sephora.db")
cursor = conn.cursor()

# Write the DataFrame to an SQLite table
df_filtered.to_sql('makeup_products', conn, if_exists='replace', index=False)

# Example usage with user preferences
user_preferences = {
    "preferred_brands": ["NARS", "Fenty Beauty", "Charlotte Tilbury"],
    "preferred_categories": ["Foundation", "Lipstick"],
    "price_range": (20, 50),
    "min_rating": 4.0
}

# Filter based on user preferences
recommended_products = df_filtered[
    (df_filtered['brand'].isin(user_preferences['preferred_brands'])) &
    (df_filtered['category'].isin(user_preferences['preferred_categories'])) &
    (df_filtered['price'] >= user_preferences['price_range'][0]) &
    (df_filtered['price'] <= user_preferences['price_range'][1]) &
    (df_filtered['rating'] >= user_preferences['min_rating'])
    ]

# Sort by rating, number of reviews, or price for better recommendations
recommended_products = recommended_products.sort_values(
    by=['rating', 'number_of_reviews'], ascending=[False, False]
)


# Content-based filtering
def recommend_products(preferences, data):
    recommended = data[
        (data['brand'].isin(preferences['preferred_brands'])) &
        (data['category'].isin(preferences['preferred_categories'])) &
        (data['price'] >= preferences['price_range'][0]) &
        (data['price'] <= preferences['price_range'][1]) &
        (data['rating'] >= preferences['min_rating'])
        ]
    return recommended.sort_values(by=['rating', 'number_of_reviews'], ascending=[False, False])


recommendations = recommend_products(user_preferences, df_filtered)
print(recommendations[['name', 'brand', 'category', 'price', 'rating']].head(10))


# Generate synthetic ratings
def generate_synthetic_ratings(dataframe, user_pref, top_n=10):
    rec_products = dataframe[
        (dataframe['brand'].isin(user_pref['preferred_brands'])) &
        (dataframe['category'].isin(user_pref['preferred_categories'])) &
        (dataframe['price'] >= user_pref['price_range'][0]) &
        (dataframe['price'] <= user_pref['price_range'][1]) &
        (dataframe['rating'] >= user_pref['min_rating'])
        ]

    # Safely modify DataFrame to avoid SettingWithCopyWarning
    rec_products.loc[:, 'synthetic_rating'] = np.random.uniform(3.5, 5.0, size=len(rec_products))

    # Simulate higher ratings for preferred brands/categories
    rec_products.loc[
        rec_products['brand'].isin(user_pref['preferred_brands']), 'synthetic_rating'] += 0.5
    rec_products.loc[
        rec_products['category'].isin(user_pref['preferred_categories']), 'synthetic_rating'] += 0.5

    return rec_products.sort_values(by='synthetic_rating', ascending=False).head(top_n)


# Generate recommendations
synthetic_recommendations = generate_synthetic_ratings(df_filtered, user_preferences, top_n=10)
print(synthetic_recommendations[['name', 'brand', 'category', 'price', 'rating', 'synthetic_rating']])


# Simulate collaborative filtering ratings
def generate_collaborative_ratings(dataframe, user_pref, top_n=10):
    # If user preferences are provided, filter data accordingly
    if user_pref:
        dataframe = dataframe[
            (dataframe['brand'].isin(user_pref['preferred_brands'])) &
            (dataframe['category'].isin(user_pref['preferred_categories'])) &
            (dataframe['price'] >= user_pref['price_range'][0]) &
            (dataframe['price'] <= user_pref['price_range'][1]) &
            (dataframe['rating'] >= user_pref['min_rating'])
            ]

    # Safely modify the DataFrame with .loc
    dataframe.loc[:, 'collaborative_rating'] = np.random.uniform(3.5, 5.0, size=len(dataframe))

    # Sort by the generated collaborative rating
    return dataframe.sort_values(by='collaborative_rating', ascending=False).head(top_n)


# Combine content-based and collaborative ratings
def combine_ratings(dataframe, user_pref, content_weight=0.6, collaborative_weight=0.4):
    content_based = generate_synthetic_ratings(dataframe, user_pref)
    collaborative = generate_collaborative_ratings(dataframe, user_pref)

    print("Content-based recommendations:")
    print(content_based[['name', 'synthetic_rating']])

    print("Collaborative-based recommendations:")
    print(collaborative[['name', 'collaborative_rating']])

    # Merge the data on product name, including 'brand' and 'price' columns
    merged_df = pd.merge(content_based[['name', 'brand', 'price', 'rating', 'synthetic_rating']],
                         collaborative[['name', 'brand', 'price', 'rating', 'collaborative_rating']],
                         on=['name', 'brand', 'price', 'rating'],
                         how='inner')
    print(merged_df.columns)
    # Combine ratings (weighted average)
    merged_df['combined_rating'] = (content_weight * merged_df['synthetic_rating'] +
                                    collaborative_weight * merged_df['collaborative_rating'])

    # Sort by combined rating
    merged_df = merged_df.sort_values(by=['price', 'rating'], ascending=True)

    return merged_df[['name', 'brand', 'price', 'rating']]


# Generate the final combined recommendations
combined_recommendations = combine_ratings(df_filtered, user_preferences)
print(combined_recommendations.head(10))
