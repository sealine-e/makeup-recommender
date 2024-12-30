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

# Verify that the data was inserted correctly
cursor.execute("SELECT * FROM makeup_products LIMIT 5")

################## PRACTICING SQL QUERIES #############################
# average ratings per brand
query1 = """
SELECT brand, AVG(rating) AS avg_rating
FROM makeup_products
GROUP BY brand
"""
avg_rating_by_brand = pd.read_sql_query(query1, conn)
print(avg_rating_by_brand)

# Top brands and num of products
query3 = """
SELECT brand, AVG(rating) AS avg_rating, COUNT(*) AS product_count, AVG(price) AS avg_price
FROM makeup_products
GROUP BY brand
ORDER BY avg_rating DESC
"""
top_5_brands = pd.read_sql_query(query3, conn)
print(top_5_brands)

# Create an interactive bar plot with Plotly
fig = px.scatter(top_5_brands,
                 x='avg_rating',
                 y='product_count',
                 hover_data={'brand': True, 'avg_rating': True},
                 color='avg_price',
                 labels={'avg_price': 'Average Price',
                         'avg_rating': 'Average Rating',
                         'product_count': 'Number of Products'},
                 title='Average Rating by Brand')

# Customize hover info
fig.update_traces(marker=dict(colorscale='Viridis'))
fig.update_traces(hovertemplate='<b>Brand:</b> %{customdata[0]}<br>'
                                '<b>Average Rating:</b> %{x:.1f}<br>'
                                '<b>Average Price:</b> $%{y:.2f}<br>'
                                '<b>Product Count:</b> %{marker.color:.2f}')
# hovertemplate='<b>Brand:</b> %{brand}<br><b>Avg Rating:</b> %{y}'
# Show the plot
# fig.show()
