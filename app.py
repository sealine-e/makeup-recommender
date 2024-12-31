
import streamlit as st

from main.predictor import get_similar_products, df

# Streamlit app UI components
st.title("Sephora Product Recommender")

# User input fields
category_input = st.multiselect("Select your preferred categories", df['category'].unique())
price_range_input = st.slider("Select your price range", min_value=float(df['price'].min()),
                              max_value=float(df['price'].max()), value=(20.00, 50.00))
rating_min_input = st.slider("Select minimum rating", min_value=1.0, max_value=5.0, value=4.0)
num_products_input = st.number_input("How many items would you like to be recommended?", min_value=0, max_value=100)

# Button to trigger the recommendation
if st.button("Get Recommendations"):
    if category_input:
        min_price, max_price = price_range_input
        similar_products = get_similar_products(
            category_input,
            min_price, max_price,
            rating_min_input,
            num_products_input
        )

        # Display the recommended products with product names as clickable links
        if not similar_products.empty:
            st.markdown(f"**Recommended Products:**"
                        )
            for _, row in similar_products.iterrows():
                st.page_link(row['URL'], label=f"**Product Name**: {row['name']}")
                # Create a clickable product name
                st.markdown(
                    f"**Brand:** {row['brand']}  \n"
                    f"**Category:** {row['category']}  \n"
                    f"**Price:** ${row['price']}0 USD  \n"
                    f"**Rating:** {row['rating']}⭐",
                    unsafe_allow_html=True
                )
            st.write(f"*Note: Products shown are not guaranteed to be in stock.*")
