import streamlit as st
import pandas as pd
import numpy as np


import streamlit as st
import pandas as pd
import numpy as np

from main.predictions import generate_collaborative_ratings, generate_synthetic_ratings, combine_ratings



# Streamlit App
st.title("Sephora Product Recommendation System")

# Load dataset
df = pd.read_csv("main/sephora_website_dataset.csv")
df_filtered = df[['id', 'brand', 'name', 'category', 'price', 'rating', 'number_of_reviews']]

# User input for preferences
preferred_brands = st.multiselect("Select your preferred brands", df_filtered['brand'].unique())
preferred_categories = st.multiselect("Select your preferred categories", df_filtered['category'].unique())
price_range = st.slider("Select your price range", min_value=int(df_filtered['price'].min()),
                        max_value=int(df_filtered['price'].max()), value=(20, 50))
min_rating = st.slider("Select minimum rating", min_value=1.0, max_value=5.0, value=4.0)

# Apply filters based on user preferences
user_preferences = {
    "preferred_brands": preferred_brands,
    "preferred_categories": preferred_categories,
    "price_range": price_range,
    "min_rating": min_rating
}

# Generate recommendations if brands and categories are selected
if len(preferred_brands) > 0 and len(preferred_categories) > 0:
    combined_recommendations = combine_ratings(df_filtered, user_preferences)

    # Ensure the data is not empty before displaying
    if not combined_recommendations.empty:
        # Debug: Check the data before plotting
        st.write(combined_recommendations.head(10))

        st.write("All recommendations have been displayed based on selected preferences.")
    else:
        st.warning("No recommendations found for the selected preferences.")
else:
    st.warning("Please select at least one brand and one category to get recommendations.")

