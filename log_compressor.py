"""
作者: Mina
日期: 2023-02-20
版權: TSMC
"""
import subprocess  # 匯入 subprocess 模組，以便執行 shell 命令
import shutil  # 匯入 shutil 模組，以便進行目錄操作
import os  # 匯入 os 模組，以便進行目錄操作

compress_folder = 'compressed_logs'  # 壓縮後的檔案儲存資料夾名稱


class LogCompressor:
  """
  日誌檔案壓縮器，將同一天同一工具的日誌檔案壓縮成 tar.gz 格式。
  """

  def __init__(self):
    """
    初始化方法，不執行任何操作。
    """
    return

  def delete_compress_folder(self):
    """
    刪除壓縮後檔案的資料夾，如果存在的話。
    """
    if os.path.isdir(compress_folder):
      shutil.rmtree(compress_folder)

  def compress_same_day_files(self, result_files):
    """
    壓縮同一天同一工具的日誌檔案。
    :param result_files: 以字典形式儲存的日誌檔案路徑，格式為 {工具名稱: {日期: [檔案路徑1, 檔案路徑2, ...]}}。
    :return: 以字典形式儲存的壓縮後的檔案名稱，格式為 {工具名稱: [[檔案1名稱, 檔案1路徑], [檔案2名稱, 檔案2路徑], ...]}
    """
    self.delete_compress_folder()  # 刪除已存在的壓縮檔案資料夾
    os.makedirs(compress_folder)  # 建立新的壓縮檔案資料夾
    compressed_files = {}  # 儲存壓縮檔案的名稱

    # 迭代每個工具的每個日期下的檔案，如果有多個檔案就壓縮成一個檔案
    for toolname, date_files in result_files.items():
      for date, files in date_files.items():
        if len(files) > 1:  # 如果有多個檔案
          archive_filename = f'{compress_folder}/{toolname}_{date}.log.tar.gz'  # 壓縮檔案的名稱
          command = f"tar -cf {archive_filename} {' '.join(files)}"  # 執行壓縮命令
          subprocess.call(command, shell=True)  # 執行 shell 命令
          if toolname in compressed_files:
            compressed_files[toolname].append(
              [f'{toolname}_{date}.log.tar.gz', archive_filename])
          else:
            compressed_files[toolname] = [[
              f'{toolname}_{date}.log.tar.gz', archive_filename
            ]]

    return compressed_files
