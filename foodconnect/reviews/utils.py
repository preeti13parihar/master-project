import boto3
from django.conf import settings

s3_client = boto3.client("s3",
   aws_access_key_id= settings.AWS_ACCESS_KEY,
   aws_secret_access_key= settings.AWS_SECRET_KEY)

def upload_image(file, folder):
    try:
        s3_client.upload_fileobj(
            file.file,
            settings.S3_BUCKET,
            folder + "/" + str(file),
            ExtraArgs={
                "ACL": "public-read",
                "ContentType": file.content_type
            }
        )
        
        url = settings.S3_FILE_URL + folder + "/" + str(file)
        return url

    except Exception as e:
        raise e