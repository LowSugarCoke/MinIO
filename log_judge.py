"""
作者: Mina
日期: 2023-02-20
版權: TSMC
"""
# import相關的模組
import os
import datetime


# 定義一個LogJudge類別，用於處理log資料
class LogJudge:

  def __init__(self):
    pass

  def is_folder_size_above_5_g(self, folder_path):
    """
        判斷指定資料夾的大小是否超過5G，如果是，則回傳True，否則回傳False

        Args:
        - folder_path: 資料夾的路徑

        Returns:
        - boolean: True代表資料夾大小超過5G，False代表資料夾大小小於或等於5G
        """
    total_size = 0
    # 使用os.walk遍歷指定資料夾下的所有檔案和子目錄
    for dirpath, dirnames, filenames in os.walk(folder_path):
      # 遍歷檔案
      for f in filenames:
        fp = os.path.join(dirpath, f)
        # 如果是符號連結則跳過，不計算大小
        if not os.path.islink(fp):
          total_size += os.path.getsize(fp)

    # 判斷資料夾大小是否超過5G，如果是，則回傳True，否則回傳False
    if total_size > 5 * 1024 * 1024 * 1024:
      print("Folder size is greater than 5G")
      return True
    else:
      print("Folder size is less than or equal to 5G")
      return False

  def get_file_in_folder(self, folder_path):
    """
        獲取指定資料夾下的所有檔案路徑

        Args:
        - folder_path: 資料夾的路徑

        Returns:
        - list: 包含指定資料夾下所有檔案路徑的列表
        """
    output = []
    for dirpath, dirnames, filenames in os.walk(folder_path):
      for f in filenames:
        output.append(folder_path + f)
    return output

  def get_file_above_two_days(self, folder_path):
    """
        獲取指定資料夾下創建時間超過兩天的所有檔案名稱

        Args:
        - folder_path: 資料夾的路徑

        Returns:
        - list: 包含指定資料夾下所有創建時間超過兩天的檔案名稱的列表
        """
    output = []
    for dirpath, dirnames, filenames in os.walk(folder_path):
      for f in filenames:
        if self.__is_file_above_two_days(os.path.join(folder_path, f)):
          output.append(f)
    return output

  def __is_file_above_two_days(self, file):
    """
        判斷指定檔案的創建時間是否超過兩天

        Args:
        - file: 檔案的路徑

        Returns:
        - boolean: True代表檔案創建時間超過兩天，False代表檔案創建
        """

    # 取得文件的stat資訊
    stat_info = os.stat(file)

    # 取得文件的創建時間
    created_time = datetime.datetime.fromtimestamp(stat_info.st_ctime).date()

    # 取得現在時間
    now = datetime.datetime.now().date()

    # 計算兩個時間之間的差距
    time_difference = now - created_time

    # 如果差距超過兩天，則認為文件的創建時間大於兩天，否則則表示文件是在兩天內創建的
    if time_difference.days > 2:
      print(f"{file} was created more than 2 days ago")
      return True
    else:
      print(f"{file} was created within the last 2 days")
      return False
