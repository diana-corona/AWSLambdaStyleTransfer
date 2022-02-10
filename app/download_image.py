import base64
import boto3
import json
from datetime import datetime

s3 = boto3.client("s3")
lambda_client = boto3.client("lambda", region_name="us-east-1",)

class JsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return str(obj, encoding="utf-8");
        return json.JSONEncoder.default(self, obj)

def download_image(bucket_name,image_key):
    s3_image = s3.get_object(Bucket=bucket_name, Key=image_key)
    file_content = s3_image["Body"].read()
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/jpg",
            "Content-Disposition": "attachment; filename={}".format(image_key)
        },
        "body": base64.b64encode(file_content),
        "isBase64Encoded": True
    }


def lambda_handler(event, context):
    #bucket_name = event["queryStringParameters"]["bucket_name"]
    bucket_name = "style-image-app"
    image_key = event["queryStringParameters"]["image_key"]

    return download_image(bucket_name,image_key)
