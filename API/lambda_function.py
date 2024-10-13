import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
from collections import defaultdict
import requests
d = boto3.resource("dynamodb")

API_KEY = "<API_KEY>"
MODEL_NAME = "azure/gpt-4o"
kindo_url = "https://llm.kindo.ai/v1/chat/completions"
def lambda_handler(event, context):
    try:
        params = json.loads(event.get('body'))
        user_Specifications = params.get('users')[0].get('preferences').get('specifications')
        user_Skin_Type = user_Specifications.get('skin_type')
        user_Skin_Concerns = 'Acne'#user_Specifications.get('skin_concern')
        user_Budget = 50 #user_Specifications.get('budget')
        
        reviews= get_product_reviews(skinType = user_Skin_Type, skinConcern = user_Skin_Concerns)
        product_details, recommended_product_review = get_product_recommendation(reviews, user_Budget)
        
        product_name = product_details.get('productName')
        brand = product_details.get('brandDisplayName')
        key_ingredients = product_details.get('ingredientDesc')
        
        reviews = recommended_product_review

        desc = kindo_call(product_name, brand, key_ingredients, user_Skin_Type, user_Skin_Concerns, user_Budget, reviews)
        body = {'recommendations': {'user1': {'products': [{'brand': brand, 'product_id': product_details.get('productId'), 'rank': 1, 'name': product_name, 'image_url': 'https://www.sephora.com/productimages/sku/s2210581-main-zoom.jpg?imwidth=1224', 'price': ('$'+ str(product_details.get('listPrice'))), 'affiliate_url': product_details.get('fullSiteProductUrl'), 'tags': ['hydrating', 'organic', 'skincare'], 'description': desc, 'reviews': [{'id': 1, 'name': 'John Doe', 'review': 'This moisturizer works wonders for dry skin.'}]}]}}}
        # Your main logic here
        response = {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',  # Or specify allowed domain
                'Access-Control-Allow-Methods': 'OPTIONS,GET,POST',
                'Access-Control-Allow-Headers': 'Content-Type,Authorization'
            },
            'body': json.dumps(body)
        }
        return response
    
    except Exception as e:
        # Print the exception for logging/debugging
        print(f"Error occurred: {str(e)}")
        
        # Return a generic error response with CORS headers
        error_response = {
            'statusCode': 500,  # Internal server error
            'headers': {
                'Access-Control-Allow-Origin': '*',  # Or specify allowed domain
                'Access-Control-Allow-Methods': 'OPTIONS,GET,POST',
                'Access-Control-Allow-Headers': 'Content-Type,Authorization'
            },
            'body': 'An error occurred. Please try again later.'
        }
        return error_response
    
def kindo_call(product_name, brand, key_ingredients, user_Skin_Type, user_Skin_Concerns, user_Budget, reviews):
    prompt_template = f"""
Using the user’s skin type, skin concerns, budget, and skincare preferences, craft a personalized and engaging explanation for why we recommended a product to them. Since specific product metadata is not provided, remain agnostic to the details and use general terms. The explanation should:

	1.	Address the User’s Needs:
	•	Begin by acknowledging the user’s skin type and skin concerns.
	•	Explain how the product is specifically formulated to suit their skin type and address their concerns.
	2.	Highlight Product Value:
	•	Emphasize the benefits of the product’s key ingredients in a general way.
	•	Mention any special features that make the product stand out.
	3.	Align with Preferences:
	•	Point out how the product meets the user’s skincare preferences.
	•	Highlight any features that align with these preferences.
	4.	Consider Budget:
	•	Acknowledge the user’s budget and explain how the product offers excellent value.
	•	Mention any cost-saving benefits in general terms.
	5.	Include Social Proof:
	•	Incorporate positive sentiments from users like them.
	•	Reference the brand’s reputable status without specific details.
	6.	Use an Appropriate Tone:
	•	Maintain a friendly, professional, and reassuring tone.
	•	Keep the explanation concise and focused on the user’s needs.

User Input Fields:

	•	Skin Type: {user_Skin_Type}
	•	Skin Concern(s): {user_Skin_Concerns}
	•	Budget: {user_Budget}

Product Metadata:

	•	Be agnostic to the metadata. The User input fields are correct.

Additionally, write a summary for the “What Users Like You Are Saying” section by emphasizing key sentiments from reviews (listed at the bottom of this prompt), focusing on “users like you.” Since specific review data is not provided, use general positive feedback and common themes. The summary should:

	1.	Highlight Positive Feedback:
	•	Emphasize frequently praised features in a general sense.
	•	Use representative phrases that users might say.
	2.	Emphasize Relevance to the Reader:
	•	Reference similar users with the same skin type and concerns.
	•	Personalize the summary to make the reader feel connected.
	3.	Reflect Overall Sentiment:
	•	Provide an overall positive impression.
	•	Mention that the consensus among users like them is highly favorable.
	4.	Maintain an Engaging and Informative Tone:
	•	Write in a friendly and conversational tone.
	•	Avoid technical jargon.

Output Format:

	•	Length: Keep the explanation concise.
	•	Structure: Start by addressing the user’s needs, followed by highlighting product value and details.
	•	Limit the “What Users Like You Are Saying” to three short bullet points.
reviews:
{reviews}
"""
    
    # Define the data payload
    data = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": prompt_template}]
    }
    headers = {
    "api-key": API_KEY,
    "content-type": "application/json"
    }
    # Send the request
    response = requests.post(kindo_url, headers=headers, json=data)
    # print(json.dumps(response.json(), indent=4))
    
    regular_text = response.json().get('choices')[0].get('message').get('content')
    return regular_text


def get_product_reviews(skinType, skinConcern):
    table = d.Table("ProductReviews")

    response = table.scan(
        FilterExpression=Attr("skinType").eq(skinType) &
        Attr("PredictedSkinConcern").contains(skinConcern))
        #Attr("listPrice").lt(budget)
    reviews = response.get("Items")
    return reviews

def get_product_details(product_id):
    table = d.Table("SephoraProducts")

    response = table.query(
        KeyConditionExpression=Key("productId").eq(product_id)
    )
    if not response.get("Items"):
        
        response = table.scan(
            FilterExpression=Attr("skuId").eq(product_id))    
    
    return response["Items"][0]

def get_all_products():
    table = d.Table("SephoraProducts")

    response = table.scan()
    return response["Items"]



def get_product_recommendation(reviews, budget):
    reviews = sorted(reviews, key=lambda k: k.get('productId'))

    product_score = {}

    product_reviews = defaultdict(list)

    for rev in reviews:
    # for r in rev:
    #     for k in r.keys():
    #         if k != "productId" or k != "reviewText" or k != sentiment
        product_reviews[rev["productId"]].append(rev)

    for k, rs in product_reviews.items():
        score_sum = 0.0
        for r in rs:
            score_sum += float(r["SentimentScore"])
            avg = score_sum / len(rs)
            product_score[k] = avg
    
    # map productId to details
    product_details_list = get_all_products()

    productId_to_details = {item["productId"]: item for item in product_details_list if "productId" in item}

    # sort products based on score
    sorted_prod_to_score = dict(sorted(product_score.items(), key=lambda item: item[1])) # prodId to score
    
    prod_rec_id = ""

    # look up details from map from sorted prod score and compare budget
    for pId, _ in sorted_prod_to_score.items():
        price = productId_to_details[pId].get("listPrice")
        if float(price) <= budget:
            prod_rec_id = pId
            break


    #prod_rec_id = ""
    # prod_score = 0.0

    # for k, score in product_score.items():
    #     if score > prod_score:
    #         prod_score = score
    #         prod_rec_id = k

    reviews = product_reviews[prod_rec_id] # list of dictionaries (ie reviews)
    final_rev = []
    for r in reviews:
        final_rev.append(r.get("review_text"))
        final_rev.append('\n')

    details = get_product_details(prod_rec_id)
    return details, final_rev

event = {'resource': '/recommender', 'path': '/recommender', 'httpMethod': 'POST', 'headers': {'accept': '*/*', 'accept-encoding': 'gzip, deflate, br, zstd', 'accept-language': 'en-US,en;q=0.9', 'content-type': 'text/plain;charset=UTF-8', 'Host': 'm10r1es0r9.execute-api.us-west-2.amazonaws.com', 'origin': 'http://localhost:3000', 'priority': 'u=1, i', 'referer': 'http://localhost:3000/', 'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"macOS"', 'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'cross-site', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36', 'X-Amzn-Trace-Id': 'Root=1-670b844e-27e638d5429e57ab2b4c5851', 'X-Forwarded-For': '69.75.199.226', 'X-Forwarded-Port': '443', 'X-Forwarded-Proto': 'https'}, 'multiValueHeaders': {'accept': ['*/*'], 'accept-encoding': ['gzip, deflate, br, zstd'], 'accept-language': ['en-US,en;q=0.9'], 'content-type': ['text/plain;charset=UTF-8'], 'Host': ['m10r1es0r9.execute-api.us-west-2.amazonaws.com'], 'origin': ['http://localhost:3000'], 'priority': ['u=1, i'], 'referer': ['http://localhost:3000/'], 'sec-ch-ua': ['"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"'], 'sec-ch-ua-mobile': ['?0'], 'sec-ch-ua-platform': ['"macOS"'], 'sec-fetch-dest': ['empty'], 'sec-fetch-mode': ['cors'], 'sec-fetch-site': ['cross-site'], 'User-Agent': ['Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'], 'X-Amzn-Trace-Id': ['Root=1-670b844e-27e638d5429e57ab2b4c5851'], 'X-Forwarded-For': ['69.75.199.226'], 'X-Forwarded-Port': ['443'], 'X-Forwarded-Proto': ['https']}, 'queryStringParameters': None, 'multiValueQueryStringParameters': None, 'pathParameters': None, 'stageVariables': None, 'requestContext': {'resourceId': 'n5v66a', 'resourcePath': '/recommender', 'httpMethod': 'POST', 'extendedRequestId': 'flGcPFl-PHcEfeA=', 'requestTime': '13/Oct/2024:08:26:54 +0000', 'path': '/ailahack/recommender', 'accountId': '051826734432', 'protocol': 'HTTP/1.1', 'stage': 'ailahack', 'domainPrefix': 'm10r1es0r9', 'requestTimeEpoch': 1728808014066, 'requestId': '21ba7582-fe95-4e10-afc4-c88cfa838089', 'identity': {'cognitoIdentityPoolId': None, 'accountId': None, 'cognitoIdentityId': None, 'caller': None, 'sourceIp': '69.75.199.226', 'principalOrgId': None, 'accessKey': None, 'cognitoAuthenticationType': None, 'cognitoAuthenticationProvider': None, 'userArn': None, 'userAgent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36', 'user': None}, 'domainName': 'm10r1es0r9.execute-api.us-west-2.amazonaws.com', 'deploymentId': 'pz4zxw', 'apiId': 'm10r1es0r9'}, 'body': '{"users":[{"id":"user1","preferences":{"product":{"type":"skincare","category":"moisturizer"},"specifications":{"skin_type":"Combination","skin_concern":"Hyperpigmentation","organic":true,"budget":"3","specific_preference":""}}}]}', 'isBase64Encoded': False}
context = None
res = lambda_handler(event,context)
print(res)