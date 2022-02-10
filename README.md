# Artistic Style Transfer Api
Image classification API that uploads, downloads and classify images from s3 using arbitrary-image-stylization-v1-256  pretrained neural network.

### To deploy 
1. Run 'serverless deploy' to upload the lambda function to aws

### Endpoints
## /style-image
1. Artistic style transfer from one image to another taken from s3

## POST /image
1. Upload image to s3, creates unique names each time

## GET /image
1. Download image from s3 repository

## DELETE /image
1. Delete image from s3 repository