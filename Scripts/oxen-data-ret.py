import requests
import json
import csv

BASE_URL = "https://sephora14.p.rapidapi.com"
SEARCH_BY_CATEGORY_SUB_URL = "/searchByCategory"
SEARCH_BY_CATEGORY_URL = BASE_URL + SEARCH_BY_CATEGORY_SUB_URL
CATEGORIES_SUB_URL = "/categories"
CATEGORIES_URL = BASE_URL + CATEGORIES_SUB_URL
PRODUCT_REVIEWS_SUB_URL = "/productReviews"
PRODUCT_REVIEWS_URL = BASE_URL + PRODUCT_REVIEWS_SUB_URL

# Connect to MongoDB (commented out)
# import pymongo
# client = pymongo.MongoClient("mongodb://localhost:27017/")
# db = client["sephora"]
# categories_collection = db["categories"]
# products_collection = db["products"]
# reviews_collection = db["reviews"]

# Initialize AWS Bedrock client (commented out)
# import boto3
# bedrock_client = boto3.client("bedrock-runtime")

# List of categories
global category_ids
category_ids = ["facial-treatments"]

def fetch_sephora_categories(api_key):
    # Define the headers for RapidAPI
    headers = {
        'x-rapidapi-key': api_key,
        'x-rapidapi-host': "sephora14.p.rapidapi.com"
    }

    # Print the category list
    print("Categories:")
    for category_id in category_ids:
        print(f"- {category_id}")
    
    # Fetch and print products for the categories
    for category_id in category_ids:
        fetch_products_in_category(category_id, headers)

def fetch_products_in_category(category_id, headers):
    # Define the URL with query parameters for fetching products in a category
    url = f"{SEARCH_BY_CATEGORY_URL}?categoryID={category_id}&sortBy=BEST_SELLING"

    products_list = []
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
            
            # Append product data to the list
            products_list.append({
                "productId": product_id,
                "productName": product_name,
                "brandName": brand_name,
                "price": price,
                "productUrl": product_url,
                "categoryID": category_id
            })
            
            # Fetch and store reviews for the product
            fetch_product_reviews(product_id, headers)
        
        # Write products to CSV
        write_products_to_csv(products_list)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching products for category {category_id}: {e}")

def fetch_product_reviews(product_id, headers):
    # Define the URL with query parameters for fetching product reviews
    url = f"{PRODUCT_REVIEWS_URL}?productID={product_id}"

    reviews_list = []
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
            
            # Append review data to the list
            reviews_list.append({
                "productID": product_id,
                "reviewText": review_text,
                "rating": rating,
                "reviewerName": reviewer_name,
                "reviewDate": review_date,
                "sentimentScore": sentiment_score
            })
        
        # Write reviews to CSV
        write_reviews_to_csv(reviews_list)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching reviews for product {product_id}: {e}")

def get_sentiment_score(review_text):
    # Use AWS Bedrock to get the sentiment score (commented out)
    # response = bedrock_client.invoke_model(
    #     modelId='sentiment-analysis',
    #     body=json.dumps({
    #         "inputText": review_text,
    #         "prompt": "generate and return one number 0 to 1 as the sentiment score of this review"
    #     }),
    #     contentType="application/json"
    # )
    # result = json.loads(response['body'])
    # return float(result.get("sentimentScore", 0))
    return 0.5  # Placeholder sentiment score

def write_products_to_csv(products):
    with open('products.csv', mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["productId", "productName", "brandName", "price", "productUrl", "categoryID"])
        writer.writeheader()
        for product in products:
            writer.writerow(product)

def write_reviews_to_csv(reviews):
    with open('reviews.csv', mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["productID", "reviewText", "rating", "reviewerName", "reviewDate", "sentimentScore"])
        writer.writeheader()
        for review in reviews:
            writer.writerow(review)

def display_data():
    # Display categories, products, and reviews from MongoDB in JSON format (commented out)
    # print("\nCategories from MongoDB:")
    # for category in categories_collection.find():
    #     print(json.dumps(category, indent=4, default=str))

    # print("\nProducts from MongoDB:")
    # for product in products_collection.find():
    #     print(json.dumps(product, indent=4, default=str))

    # print("\nReviews from MongoDB:")
    # for review in reviews_collection.find():
    #     print(json.dumps(review, indent=4, default=str))
    pass

# Example usage
API_KEY = "<API_KEY>"
fetch_sephora_categories(API_KEY)
display_data()