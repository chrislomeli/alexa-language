import logging
import os

import boto3
from botocore.exceptions import ClientError

from source.model import StorageManager, FlashCard


class S3Storage(StorageManager):
    s3_client = boto3.client('s3')

    def __init__(self, bucket_name):
        super().__init__()
        self.s3_bucket = bucket_name
        if not self.bucket_exists(self.s3_bucket):
            self.create_bucket()

    def check_exists(self):
        try:
            meta = self.s3_client.head_object(
                Bucket=self.s3_bucket,
                Key=self.flash_card.url
            )
            for key, value in self.flash_card.meta_data.items():
                if key not in meta:
                    return False
                if meta[key] != value:
                    return False
            return True
        except ClientError as e:
            return False

    def write_audio(self, data: bytes) -> str:
        try:
            flash_card = self.flash_card
            response = self.s3_client.put_object(
                Bucket=self.s3_bucket,
                Key=flash_card.url,
                Body=data,
                ACL='public-read',
                Metadata=flash_card.meta_data
            )

            presigned: str = self.s3_client.generate_presigned_url('get_object',
                                                        Params={'Bucket': self.s3_bucket,
                                                                'Key': flash_card.url},
                                                        ExpiresIn=3600)
            if presigned and len(presigned) > 0:
                if "?" in presigned:
                    url = presigned.split("?")[0]
                    return url.strip()

            return ""

        except ClientError as e:
            # AllAccessDisabled error == bucket not found
            # NoSuchKey or InvalidRequest error == (dest bucket/obj == src bucket/obj)
            logging.error(e)
            return False

    def read_audio(self) -> (dict, bool):
        try:
            object_data = self.s3_client.get_object(
                Bucket=self.s3_bucket,
                Key=self.flash_card.url
            )
            return object_data, True
        except ClientError as e:
            # AllAccessDisabled error == bucket not found
            # NoSuchKey or InvalidRequest error == (dest bucket/obj == src bucket/obj)
            logging.error(e)
            return None, False

    def bucket_exists(self, bucket):
        response = self.s3_client.list_buckets()
        return bucket in response['Buckets']

    def create_bucket(self, region=None):
        try:
            if region is None:
                s3_client = boto3.client('s3')
                s3_client.create_bucket(Bucket=self.s3_bucket)
            else:
                s3_client = boto3.client('s3', region_name=region)
                location = {'LocationConstraint': region}
                s3_client.create_bucket(Bucket=self.s3_bucket,
                                        CreateBucketConfiguration=location)
        except ClientError as e:
            logging.error(e)
            return False
        return True
