"""
Author: Mina
Date: 2023-02-20
Copyright: TSMC
"""

import subprocess
import shutil
import os

compress_folder = 'compressed_logs'


class LogCompressor:
  """
  Log file compressor that compresses log files of the same tool and day into tar.gz format.
  """

  def __init__(self):
    """
    Initialization method that does not perform any operations.
    """
    return

  def delete_compress_folder(self):
    """
    Delete the folder for compressed files, if it exists.
    """
    if os.path.isdir(compress_folder):
      shutil.rmtree(compress_folder)

  def compress_same_day_files(self, result_files):
    """
    Compress log files of the same tool and day.
    :param result_files: A dictionary that stores log file paths in the format of {tool name: {date: [file path 1, file path 2, ...]}}.
    :return: A dictionary that stores the compressed file names in the format of {tool name: [[file 1 name, file 1 path], [file 2 name, file 2 path], ...]}
    """
    self.delete_compress_folder()
    os.makedirs(compress_folder)
    compressed_files = {}

    for toolname, date_files in result_files.items():
      for date, files in date_files.items():
        if len(files) > 1:
          archive_filename = f'{compress_folder}/{toolname}_{date}.log.tar.gz'
          command = f"tar -cf {archive_filename} {' '.join(files)}"
          subprocess.call(command, shell=True)
          if toolname in compressed_files:
            compressed_files[toolname].append(
              [f'{toolname}_{date}.log.tar.gz', archive_filename])
          else:
            compressed_files[toolname] = [[
              f'{toolname}_{date}.log.tar.gz', archive_filename
            ]]

    return compressed_files
