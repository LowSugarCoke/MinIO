"""
Author: Mina
Date: 2023-02-20
Copyright: TSMC
"""
# Import necessary packages
from minio_uploader import MinioUploader  # Import Minio uploader package
from log_processor import LogProcessor  # Import log processing package
from log_judge import LogJudge  # Import log judge package
import getpass  # Import password input package
import time  # Import time package

# Set up related parameters
endpoint_url = ""  # Set the endpoint address of Minio
bucket_name = ""  # Set the bucket name
minio_folder = ""  # Set the upload path on Minio
local_src_path = "logs/"  # Set the local directory path of log files
tool_names_file = "tool_name.txt"  # Set the tool name file path


def main():
  # Enter Minio access key
  access_key = getpass.getpass(prompt='Please enter your access key: ')
  # Enter Minio secret key
  secret_key = getpass.getpass(prompt='Please enter your secret key: ')

  # Initialize Minio upload client
  minio_client = MinioUploader(access_key, secret_key, endpoint_url,
                               bucket_name)

  # Initialize log processor
  log_judge = LogJudge()
  log_processor = LogProcessor()

  while True:
    # Check if the size of the log folder exceeds 5 GB
    is_above_5_g = log_judge.is_folder_size_above_5_g(local_src_path)
    if is_above_5_g == False:
      # Get the log files that have not been updated for more than two days
      need_to_update_files = log_judge.get_file_above_two_days(local_src_path)
    else:
      # Get all files in the log file folder
      need_to_update_files = log_judge.get_file_in_folder(local_src_path)

    # Read the tool name file
    log_processor.read_toolname(tool_names_file)
    # Classify files based on tool name
    classify_files = log_processor.classify_files_by_toolname(
      need_to_update_files)
    # Get the files that need to be compressed
    compress_files = log_processor.get_compress_files(classify_files)
    # Get the files that do not need to be compressed
    no_compress_files = log_processor.get_no_compress_name_files(
      classify_files, local_src_path)
    # Add files to the upload list
    to_update_files = {**compress_files, **no_compress_files}

    # Upload files to Minio
    minio_client.upload_files(minio_folder, to_update_files)

    # Wait for 60 seconds
    time.sleep(60)


if __name__ == '__main__':
  main()
