"""
作者: Mina
日期: 2023-02-20
版權: TSMC
"""

import boto3
from botocore.exceptions import EndpointConnectionError


class MinioUploader:
  """
    這個類定義了一個 MinioUploader 對象，它提供了上傳文件到 S3 存儲桶的功能。
    """

  def __init__(self, access_key, secret_key, endpoint_url, bucket_name):
    """
        初始化 MinioUploader 對象的連線，並設定 S3 端點網址、AWS 存取金鑰和 bucket 名稱。

        Args:
            access_key (str): AWS 存取金鑰
            secret_key (str): AWS 秘密存取金鑰
            endpoint_url (str): S3 端點網址
            bucket_name (str): S3 存儲桶名稱

        Raises:
            EndpointConnectionError: 連接 Minio endpoint 失敗時引發
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
        上傳文件到 S3 存儲桶中的指定路徑下。

        Args:
            minio_folder (str): 要上傳的路徑
            update_files (dict): 要更新的文件名和路徑的字典

        """
    # 使用 for 迴圈來走訪字典
    for toolname, files in update_files.items():
      for file in files:
        file_name = file[0]
        file_path = file[1]
        self.s3.Object(self.bucket,
                       minio_folder + '/' + file_name).upload_file(file_path)
