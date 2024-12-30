import streamlit as st
import pandas as pd

# Load data
df = pd.read_csv("main/sephora_website_dataset.csv")
df_filtered = df[['id', 'brand', 'name', 'category', 'price', 'rating', 'number_of_reviews']]

# Sidebar inputs
st.sidebar.title("User Preferences")
preferred_brands = st.sidebar.multiselect("Preferred Brands", options=df['brand'].unique())
preferred_categories = st.sidebar.multiselect("Preferred Categories", options=df['category'].unique())
price_range = st.sidebar.slider("Price Range", min_value=0, max_value=200, value=(20, 50))
min_rating = st.sidebar.slider("Minimum Rating", min_value=0.0, max_value=5.0, value=4.0)

# Filter products
filtered_products = df_filtered[
    (df_filtered['brand'].isin(preferred_brands)) &
    (df_filtered['category'].isin(preferred_categories)) &
    (df_filtered['price'] >= price_range[0]) &
    (df_filtered['price'] <= price_range[1]) &
    (df_filtered['rating'] >= min_rating)
].sort_values(by=['rating', 'number_of_reviews'], ascending=[False, False])

# Display results
st.title("Recommended Products")
st.write(filtered_products[['id', 'name', 'brand', 'category', 'price', 'rating']])
