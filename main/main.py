import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import plotly.express as px

# read csv and select desired columns
df = pd.read_csv("sephora_website_dataset.csv")
df_filtered = df[['id', 'brand', 'name', 'category', 'price', 'rating', 'number_of_reviews']]
print((df_filtered.head()))

# connect to database
conn = sqlite3.connect("sephora.db")
cursor = conn.cursor()

# Write the DataFrame to an SQLite table
df_filtered.to_sql('makeup_products', conn, if_exists='replace', index=False)

# example user preference
user_preferences = {
    "preferred_brands": ["NARS", "Fenty Beauty"],  # Example brands
    "preferred_categories": ["Foundation", "Lipstick"],  # Example categories
    "price_range": (20, 50),  # Min and max price
    "min_rating": 4.0  # Minimum acceptable rating
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

fig = px.bar(
    recommended_products.head(10),
    x='name',
    y='rating',
    color='price',
    hover_data=['brand', 'category'],
    title="Recommended Products"
)
fig.show()


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
