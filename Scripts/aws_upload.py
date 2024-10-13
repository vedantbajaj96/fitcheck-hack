import csv
import json
import boto3

# get products from csv
products = []
reader = csv.DictReader(open("products.csv"))
for row in reader:
    products.append(row)

# get reviews from csv
reviews = []
reader = csv.DictReader(open("reviews.csv"))
for row in reader:
    reviews.append(row)

# print(json.dumps(reviews,indent=4))


d = boto3.resource("dynamodb")

# write to sephora products table
table = d.Table("SephoraProducts")
with table.batch_writer() as writer:
    for p in products:
        writer.put_item(Item=p)

# write to product review table
table = d.Table("ProductReviews")
with table.batch_writer() as writer:
    for r in reviews:
        writer.put_item(Item=r)