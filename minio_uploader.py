"""
Author: Mina
Date: 2023-02-20
Copyright: TSMC
"""

import boto3
from botocore.exceptions import EndpointConnectionError


class MinioUploader:
  """
    This class defines a MinioUploader object that provides the functionality to upload files to an S3 bucket.
    """

  def __init__(self, access_key, secret_key, endpoint_url, bucket_name):
    """
        Initializes the MinioUploader object's connection and sets the S3 endpoint URL, AWS access key, and bucket name.

        Args:
            access_key (str): AWS access key
            secret_key (str): AWS secret access key
            endpoint_url (str): S3 endpoint URL
            bucket_name (str): S3 bucket name

        Raises:
            EndpointConnectionError: raised when connecting to the Minio endpoint fails
        """
    try:
      self.s3 = boto3.resource('s3',
                               endpoint_url=endpoint_url,
                               aws_access_key_id=access_key,
                               aws_secret_access_key=secret_key)
      self.bucket = self.s3.Bucket(bucket_name)
    except EndpointConnectionError as e:
      print(f"Connection to Minio endpoint {endpoint_url} failed: {e}")
      self.s3 = None

  def upload_files(self, minio_folder, update_files):
    """
        Uploads files to the specified path in the S3 bucket.

        Args:
            minio_folder (str): the path to upload to
            update_files (dict): a dictionary of file names and paths to update
        """
    # Use a for loop to iterate over the dictionary
    for toolname, files in update_files.items():
      for file in files:
        file_name = file[0]
        file_path = file[1]
        try:
          self.s3.Object(self.bucket.name, minio_folder + '/' + toolname+'/' + file_name).upload_file(file_path)
          print(f"{file_name} update to MinIO succesffully")
        except:
          print(f"{file_path} update to MinIO failed")
