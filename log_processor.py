"""
Author: Mina
Date: 2023-02-20
Copyright: TSMC
"""

import re  # Regular expression library used for matching file names
import os  # Operating system library used for getting file creation time
from datetime import datetime, date  # Date and time library used for date processing
from log_compressor import LogCompressor
from tool_name_parser import ToolNameParser
from date_capture import DateCapture


class LogProcessor:

  def __init__(self):
    self.tool_names = ""  # Store tool names
    self.regex = ""  # Regular expression used for matching file names
    self.log_compressor = LogCompressor()
    self.tool_name_parser = ""
    self.date_capture = DateCapture()

  def read_toolname(self, tool_names_path):
    """
    Read ToolName from the given file.

    Args:
        tool_names_path: The path of the file containing ToolName.

    Returns:
        None
    """
    # Read tool names
    with open(tool_names_path) as f:
      self.tool_names = f.read().splitlines()  # Store tool names in a list
    # Construct the regular expression used for matching file names by concatenating all tool names with '|'
    self.tool_name_parser = ToolNameParser(self.tool_names)
    # self.regex = re.compile("^(\w+)/(%s)[._]" % "|".join(self.tool_names))

  def classify_files_by_toolname(self, files):
    """
    Classify files by ToolName and creation date.

    Args:
        files: A list of file names.

    Returns:
        A dictionary containing files classified by ToolName and creation date.
        The key of the dictionary is the ToolName and the value is another dictionary.
        The key of the inner dictionary is the creation date and the value is a list of file paths created on that date.
    """

    # Initialize a dictionary to store the results using a dictionary comprehension
    results = {tool_name: [] for tool_name in self.tool_names}

    # Iterate over the list of file names and store the file name and creation date in the results list
    for filename in files:

      tool_name = self.tool_name_parser.parser_file(filename)
      if tool_name =="No Tool Name":
            continue
      
      created_time = self.date_capture.extract_date(filename).date()

        # Store the file name and creation date as a tuple in the results list
      results[tool_name].append((created_time, filename))

    results = self.__classify_files_by_date(
      results)  # Classify the results by date

    return results

  def __classify_files_by_date(self, results):
    """
    Further classify the files by creation date under each ToolName.

    Args:
        results: A dictionary containing the files classified by ToolName.

    Returns:
        A dictionary containing the files classified by ToolName and creation date.
        The key of the dictionary is ToolName, and the value is another dictionary with
        the key as creation date and the value as a list of files created on that date.
    """

    # Initialize the output dictionary with ToolName as the key
    output = {tool_name: {} for tool_name in self.tool_names}

    # Classify the results by date for each ToolName
    for tool_name in results:
      date_dict = {}
      for created_date, filename in results[tool_name]:
        if created_date not in date_dict:
          # If the date does not exist, create a new list to store the file names
          date_dict[created_date] = [filename]
        else:
          # If the date already exists, append the file name to the corresponding list
          date_dict[created_date].append(filename)
      output[tool_name] = date_dict

    return output

  def get_compress_files(self, input):
    """
    Compress the files classified by ToolName and creation date into one file.

    Args:
        input: A dictionary containing the files classified by ToolName and creation date.

    Returns:
        A dictionary containing the compressed files.
        The key of the dictionary is the compressed file path, and the value is a list of
        files that were compressed.
    """
    return self.log_compressor.compress_same_day_files(input)

  def delete_compressed_folder(self):
    """
    Delete the compressed files.

    Args:
        None

    Returns:
        None
    """
    self.log_compressor.delete_compress_folder()

  def get_no_compress_name_files(self, input, local_src_path):
    """
    Get the files that do not need to be compressed.

    Args:
        input: A dictionary containing the files classified by ToolName and creation date.
        local_src_path: The local file path.

    Returns:
        A dictionary containing the files that do not need to be compressed.
        The key of the dictionary is ToolName, and the value is a list of lists.
        Each list contains the file name and path.
    """

    no_compress_file = {}
    # Traverse through the files classified by ToolName and creation date
    for toolname, date_files in input.items():
      for files in date_files.items():
        # If there is only one file, it does not need to be compressed
        # print("dates", date_files)
        # print("files", files)
        # print("files size", len(files[1]))
        if len(files[1]) == 1:
          # print("hi")
          # Replace the local file path with an empty string in the file name
          file_name = files[1][0].replace(local_src_path, "")
          # If the ToolName already exists in no_compress_file, append the file name and path
          if toolname in no_compress_file:
            no_compress_file[toolname].append([file_name, files[1][0]])
          # If the ToolName does not exist in no_compress_file, create a new list and add the file name and path
          else:
            no_compress_file[toolname] = [[file_name, files[1][0]]]
    return no_compress_file

