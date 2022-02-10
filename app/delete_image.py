import base64
import boto3
import json
from datetime import datetime

s3 = boto3.client("s3")

def delete_image(bucket_name,image_key):
    s3_image = s3.delete_object(Bucket=bucket_name, Key=image_key)
    return {"bucket_name" : bucket_name, "image_key" : image_key, "status":"Deleted"}


def lambda_handler(event, context):
    #bucket_name = event["queryStringParameters"]["bucket_name"]
    bucket_name = "style-image-app"
    image_key = event["queryStringParameters"]["image_key"]
    image_params =  delete_image(bucket_name,image_key)
    return_message = {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps(image_params)
        }
    return return_message
