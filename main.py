

import requests
from bs4 import BeautifulSoup
import csv

# Amazon India URL to scrape
url = 'https://www.amazon.in/s?rh=n%3A6612025031&fs=true&ref=lp_6612025031_sar'

# Send a GET request to the URL and get the response
for i in range(100):
    response = requests.get(url)
    if response:
        break

# Parse the response using Beautiful Soup
soup = BeautifulSoup(response.content, 'html.parser')

# Find all product items on the page
product_items = soup.find_all('div', {'class': 'sg-col-4-of-24 sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col s-widget-spacing-small sg-col-4-of-20'})

# Create a CSV file to store the product details
with open('amazon_products.csv', mode='w', newline='', encoding='utf-8') as csv_file:
    # Create a CSV writer object
    writer = csv.writer(csv_file)

    # Write the header row
    writer.writerow(['Product Name', 'Price', 'Rating', 'Seller Name'])

    # Loop through each product item and extract the details
    for item in product_items:
        # Get the product name
        product_name = item.find('span', {'class': "a-size-base-plus a-color-base a-text-normal"}).text.strip()
        # print(product_name)

        # Get the product price
        product_price = item.find('span', {'class': 'a-offscreen'})
        if product_price:
            product_price = product_price.text.strip()
            # print("price",product_price)
        else:
            continue

        # Get the product rating
        product_rating = item.find('span', {'class': 'a-icon-alt'})
        if product_rating:
            product_rating = product_rating.text.strip()
        else:
            product_rating = 'No rating'
        # Get the product seller name from the following link generated from within this page.
        name_find= item.find('a',{'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})
        link = "https://www.amazon.in"+name_find['href']
        ress = requests.get(link)
        soup1 = BeautifulSoup(ress.content, 'html.parser')
        in_stock = soup1.find('div',{'id':'availability'})
        seller_name = ""
        if in_stock:
            if in_stock.text.strip()=="In stock":
                seller_name = soup1.find('div',{'id':'merchant-info'}).text.strip()
            else:
                seller_name = "not available"

        # Write the product details to the CSV file
        writer.writerow([product_name, product_price, product_rating, seller_name])
