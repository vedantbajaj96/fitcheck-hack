import requests
import boto3
import pymongo
import json
import numpy as np

BASE_URL = "https://sephora14.p.rapidapi.com"
SEARCH_BY_CATEGORY_SUB_URL = "/searchByCategory"
SEARCH_BY_CATEGORY_URL = BASE_URL + SEARCH_BY_CATEGORY_SUB_URL
CATEGORIES_SUB_URL = "/categories"
CATEGORIES_URL = BASE_URL + CATEGORIES_SUB_URL
PRODUCT_REVIEWS_SUB_URL = "/productReviews"
PRODUCT_REVIEWS_URL = BASE_URL + PRODUCT_REVIEWS_SUB_URL

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["sephora"]
categories_collection = db["categories"]
products_collection = db["products"]
reviews_collection = db["reviews"]

# Initialize AWS Bedrock client
# bedrock_client = boto3.client("bedrock-runtime")

def fetch_sephora_categories(api_key):
    # Define the headers for RapidAPI
    headers = {
        'x-rapidapi-key': api_key,
        'x-rapidapi-host': "sephora14.p.rapidapi.com"
    }

    try:
        # Make the request to fetch the category list
        response = requests.get(CATEGORIES_URL, headers=headers)
        
        # Raise an exception for HTTP errors
        response.raise_for_status()
        
        # Parse the response JSON
        categories = response.json()
        
        # Store categories in MongoDB
        categories_collection.insert_many(categories)
        
        # Get the first two category IDs
        category_ids = [category['categoryID'] for category in categories][:2]
        
        # Print the category list
        print("Categories:")
        for category_id in category_ids:
            print(f"- {category_id}")
        
        # Fetch and print products for the first two categories
        for category_id in category_ids:
            fetch_products_in_category(category_id, headers)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

def fetch_products_in_category(category_id, headers):
    # Define the URL with query parameters for fetching products in a category
    url = f"{SEARCH_BY_CATEGORY_URL}?categoryID={category_id}&sortBy=BEST_SELLING"

    try:
        # Make the request to fetch the products in the category
        response = requests.get(url, headers=headers)
        
        # Raise an exception for HTTP errors
        response.raise_for_status()
        
        # Parse the response JSON
        products = response.json()
        
        # Print the first 10 products for the category with details
        print(f"Products in category {category_id}:")
        for product in products.get("products", [])[:10]:
            product_name = product.get("displayName", "N/A")
            brand_name = product.get("brandName", "N/A")
            price = product.get("currentSku", {}).get("listPrice", "N/A")
            product_url = product.get("targetUrl", "N/A")
            product_id = product.get("productId", "N/A")
            print(f"- {product_name} by {brand_name}, Price: {price}, URL: {product_url}")
            
            # Store product in MongoDB
            product_data = {
                "productId": str(product_id),
                "productName": product_name,
                "brandName": brand_name,
                "price": price,
                "productUrl": product_url,
                "categoryID": category_id
            }
            # products_collection.insert_one(product_data)
            
            # Fetch and print reviews for the product
            fetch_product_reviews(product_id, headers)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching products for category {category_id}: {e}")

def fetch_product_reviews(product_id, headers):
    # Define the URL with query parameters for fetching product reviews
    url = f"{PRODUCT_REVIEWS_URL}?productID={product_id}"

    try:
        # Make the request to fetch the product reviews
        response = requests.get(url, headers=headers)
        
        # Raise an exception for HTTP errors
        response.raise_for_status()
        
        # Parse the response JSON
        reviews = response.json()
        
        # Print the first 10 reviews for the product
        print(f"Reviews for product {product_id}:")
        for review in reviews[:2]:
            review_text = review.get("ReviewText", "No review text available")
            rating = int(review.get("Rating", 0))  # Convert to int
            reviewer_name = review.get("UserNickname", "Anonymous")
            review_date = review.get("SubmissionTime", "Unknown date")
            sentiment_score = get_sentiment_score(review_text)
            print(f"  - Rating: {rating}, Review by {reviewer_name} on {review_date}: {review_text} (Sentiment Score: {sentiment_score})")
            
            # Store review in MongoDB
            review_data = {
                "productID": str(product_id),
                "reviewText": review_text,
                "rating": rating,
                "reviewerName": reviewer_name,
                "reviewDate": review_date,
                "sentimentScore": sentiment_score
            }
            # reviews_collection.insert_one(review_data)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching reviews for product {product_id}: {e}")

# def get_sentiment_score(review_text):
#     # Use AWS Bedrock to get the sentiment score
#     response = bedrock_client.invoke_model(
#         modelId='sentiment-analysis',
#         body=json.dumps({
#             "inputText": review_text,
#             "prompt": "generate and return one number 0 to 1 as the sentiment score of this review"
#         }),
#         contentType="application/json"
#     )
#     result = json.loads(response['body'])
#     return float(result.get("sentimentScore", 0))

def display_data():
    # Display categories, products, and reviews from MongoDB in JSON format
    print("\nCategories from MongoDB:")
    for category in categories_collection.find():
        print(json.dumps(category, indent=4, default=str))

    print("\nProducts from MongoDB:")
    for product in products_collection.find():
        print(json.dumps(product, indent=4, default=str))

    print("\nReviews from MongoDB:")
    for review in reviews_collection.find():
        print(json.dumps(review, indent=4, default=str))

# Example usage
API_KEY = "0ece9ddcd9msh98c62a92f7408b5p1e3135jsn75a3781ddf69"
fetch_sephora_categories(API_KEY)
display_data()