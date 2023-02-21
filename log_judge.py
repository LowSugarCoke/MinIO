"""
Author: Mina
Date: 2023-02-20
Copyright: TSMC
"""
# import necessary modules
import os
import datetime


# Define a LogJudge class for handling log data
class LogJudge:

  def __init__(self):
    pass

  def is_folder_size_above_5_g(self, folder_path):
    """
    Check if the size of the specified folder is above 5GB.

    Args:
        folder_path: The path of the folder.

    Returns:
        True if the folder size is greater than 5GB, False otherwise.
    """
    total_size = 0
    # Traverse all files and subdirectories under the specified folder using os.walk
    for dirpath, dirnames, filenames in os.walk(folder_path):
      # Traverse files
      for f in filenames:
        fp = os.path.join(dirpath, f)
        # Skip symbolic links and do not calculate their sizes
        if not os.path.islink(fp):
          total_size += os.path.getsize(fp)

    # Return True if the folder size is greater than 5GB, False otherwise
    if total_size > 5 * 1024 * 1024 * 1024:
      print("Folder size is greater than 5GB")
      return True
    else:
      print("Folder size is less than or equal to 5GB")
      return False

  def get_file_in_folder(self, folder_path):
    """
    Get all file paths under the specified folder.

    Args:
        folder_path: The path of the folder.

    Returns:
        A list containing all file paths under the specified folder.
    """
    output = []
    for dirpath, dirnames, filenames in os.walk(folder_path):
      for f in filenames:
        output.append(folder_path + f)
    return output

  def get_file_above_two_days(self, folder_path):
    """
    Get the names of all files under the specified folder that were created more than two days ago.

    Args:
        folder_path: The path of the folder.

    Returns:
        A list containing the names of all files that were created more than two days ago.
    """
    output = []
    for dirpath, dirnames, filenames in os.walk(folder_path):
      for f in filenames:
        if self.__is_file_above_two_days(os.path.join(folder_path, f)):
          output.append(f)
    return output

  def __is_file_above_two_days(self, file):
    """
    Check if the specified file was created more than two days ago.

    Args:
        file: The path of the file.

    Returns:
        True if the file was created more than two days ago, False otherwise.
    """

    # Get the stat info of the file
    stat_info = os.stat(file)

    # Get the creation time of the file
    created_time = datetime.datetime.fromtimestamp(stat_info.st_ctime).date()

    # Get the current time
    now = datetime.datetime.now().date()

    # Calculate the time difference between the two times
    time_difference = now - created_time

    # Return True if the time difference is more than two days, False otherwise
    if time_difference.days > 2:
      print(f"{file} was created more than 2 days ago")
      return True
    else:
      print(f"{file} was created within the last 2 days")
      return False
