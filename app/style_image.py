import tensorflow_hub as hub
import tensorflow as tf
import PIL.Image as Image
import numpy as np
import boto3
import json
import io

s3_resource = boto3.resource("s3")
s3_client = boto3.client("s3")
model = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')

def preprocess_img(img):
  max_dim = 512
  #img = tf.image.decode_image(img, channels=3)
  img = tf.image.convert_image_dtype(img, tf.float32)

  shape = tf.cast(tf.shape(img)[:-1], tf.float32)
  long_dim = max(shape)
  scale = max_dim / long_dim

  new_shape = tf.cast(shape * scale, tf.int32)

  img = tf.image.resize(img, new_shape)
  img = img[tf.newaxis, :]
  return img

def tensor_to_image(tensor):
  tensor = tensor*255
  tensor = np.array(tensor, dtype=np.uint8)
  if np.ndim(tensor)>3:
    assert tensor.shape[0] == 1
    tensor = tensor[0]
  return Image.fromarray(tensor)

def readImageFromBucket(image_key, bucket_name):
  bucket = s3_resource.Bucket(bucket_name)
  image_object = bucket.Object(image_key)
  response = image_object.get()
  return Image.open(response["Body"])

def upload_image(bucket_name,image_key,image):
  image_buffer = io.BytesIO()
  image.save(image_buffer, "JPEG")
  image_buffer.seek(0)
  s3_client.put_object(Bucket=bucket_name, Key=image_key, Body=image_buffer)
  return {"bucket_name" : bucket_name, "image_key" : image_key}

def lambda_handler(event, context):
  bucket_name = "style-image-app"
  image_key = event["queryStringParameters"]["image_key"]
  style_image_key = event["queryStringParameters"]["style_image_key"]

  image = readImageFromBucket(image_key, bucket_name)
  image = preprocess_img(image)

  print("image found")

  style_image = readImageFromBucket(style_image_key, bucket_name)
  style_image = preprocess_img(style_image)

  print("style_image found")

  stylized_image = model(tf.constant(image), tf.constant(style_image))[0]
  stylized_image = tensor_to_image(stylized_image)

  print("stylized_image generated")

  stylized_image_key = image_key[:-4] + "_" + style_image_key

  upload_image(bucket_name,stylized_image_key,stylized_image)

  print("stylized_image_key uploaded to s3",stylized_image_key)

  stylized_image_result =  {
    "bucket_name": bucket_name,
    "image":   image_key,
    "style_image": style_image_key,
    "stylized_image": stylized_image_key
  }
  return {
    "statusCode": 200,
    "headers": {
        "Access-Control-Allow-Origin": "*"
    },
    "body": json.dumps(stylized_image_result),
}
