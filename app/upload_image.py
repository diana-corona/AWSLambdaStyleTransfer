import base64
import boto3
import json
from datetime import datetime

s3 = boto3.client("s3")
lambda_client = boto3.client("lambda", region_name="us-east-1",)

def upload_image(event,bucket_name):
    data = json.loads(event["body"])
    image_key = data["name"].replace(" ", "")
    time_now = str(datetime.utcnow()).replace(" ", "")
    time_now = time_now.replace(".", "")
    time_now = time_now.replace("-", "")
    time_now = time_now.replace(":", "")
    image_key = time_now[:-4] + "_" + image_key
    image = data["file"]
    image = image[image.find(",")+1:]
    image_decoded = base64.b64decode(image + "===")
    s3.put_object(Bucket=bucket_name, Key=image_key, Body=image_decoded)

    return {"bucket_name" : bucket_name, "image_key" : image_key}
 

def lambda_handler(event, context):
    bucket_name = "style-image-app"
    if event["httpMethod"] == "POST" :
        image_params =  upload_image(event,bucket_name)
        return_message = {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps(image_params)
        }
        return return_message



        