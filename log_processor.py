"""
作者: Mina
日期: 2023-02-20
版權: TSMC
"""

import re  # 正則表達式庫，用於匹配檔案名稱
import os  # 操作系統庫，用於取得檔案創建時間
from datetime import datetime, date  # 日期時間庫，用於處理日期
from log_compressor import LogCompressor


class LogProcessor:

  def __init__(self):
    self.tool_names = ""  # 存放 tool names
    self.regex = ""  # 用來匹配檔案名稱的正則表達式
    self.log_compressor = LogCompressor()

  def read_toolname(self, tool_names_path):
    """
    從給定的檔案中讀取ToolName。

    Args:
        tool_names_path: 包含ToolName的檔案路徑。

    Returns:
        None
    """
    # 讀取 tool names
    with open(tool_names_path) as f:
      self.tool_names = f.read().splitlines()  # 將 tool names 存入列表
    # 構造匹配檔案名稱的正則表達式，使用 '|' 將所有 tool names 串聯在一起
    self.regex =  re.compile("^(\w+)/(%s)[._]"  % "|".join(self.tool_names))

  
  def classify_files_by_toolname(self, files):
    """
    將檔案按照ToolName和創建日期分類。

    Args:
        files: 包含檔案名稱的列表。

    Returns:
        一個字典，包含按照ToolName和創建日期分類的檔案。
        字典的 key 是ToolName，value 是一個字典，其 key 是創建日期，value 是該日期創建的檔案列表。
    """
    
    # 初始化結果字典，使用字典推導式創建
    results = {tool_name: [] for tool_name in self.tool_names}

    # 遍歷檔案列表，將檔案名稱和創建日期存入結果列表
    for filename in files:
      match = self.regex.match(filename)  # 使用正則表達式進行匹配
      if match:  # 如果匹配成功
        tool_name = match.group(2)  # 提取 tool name
        
        created_time = datetime.fromtimestamp(
          os.path.getctime(filename)).date()  # 取得檔案創建時間，並轉換為日期
        # 將檔案名稱與創建日期以 tuple 的形式存入結果列表
        results[tool_name].append((created_time, filename))


    results = self.__classify_files_by_date(results)  # 將結果按日期進行分類

    return results

  def __classify_files_by_date(self, results):
    """
    將按照ToolName分類的檔案進一步按照創建日期進行分類。

    Args:
        results: 一個字典，包含按照ToolName分類的檔案。

    Returns:
        一個字典，包含按照ToolName和創建日期分類的檔案。
        字典的 key 是ToolName，value 是一個字典，其 key 是創建日期，value 是該日期創建的檔案列表。
    """
    
    # 初始化分類後的結果字典
    output = {tool_name: {} for tool_name in self.tool_names}

    # 對每個 tool name 的結果進行分類
    for tool_name in results:
      date_dict = {}
      for created_date, filename in results[tool_name]:
        if created_date not in date_dict:
          # 如果該日期不存在，則新建一個列表存放檔案名稱
          date_dict[created_date] = [filename]
        else:
          # 如果該日期已存在，則將檔案名稱加入對應的列表中
          date_dict[created_date].append(filename)
      output[tool_name] = date_dict

    return output

  def get_compress_files(self, input):
    """
    將按照ToolName和創建日期分類的檔案壓縮到一個文件中。

    Args:
        input: 一個字典，包含按照ToolName和創建日期分類的檔案。

    Returns:
        一個字典，包含壓縮後的檔案。
        字典的 key 是壓縮後的檔案路徑，value 是壓縮前的檔案列表。
    """
    return self.log_compressor.compress_same_day_files(input)

  def delete_compressed_folder(self):
    """
    刪除已經壓縮的檔案。

    Args:
        None

    Returns:
        None
    """
    self.log_compressor.delete_compress_folder()
  
  def get_no_compress_name_files(self, input, local_src_path ):
    """
    取得不需要進行壓縮的檔案。

    Args:
        input: 一個字典，包含按照ToolName和創建日期分類的檔案。
        local_src_path: 本地檔案路徑。

    Returns:
        一個字典，包含不需要進行壓縮的檔案。
        字典的 key 是ToolName，value 是一個列表，其元素是一個列表，包含檔案名稱和路徑。
    """

    no_compress_file = {}
    # 遍歷按照ToolName和創建日期分類的檔案
    for toolname, date_files in input.items():
      for files in date_files.items():
        # 如果只有一個檔案，則不需要進行壓縮
        if len(files) == 1:
          # 將檔案名稱中的本地檔案路徑替換為空字串
          file_name = files[0].replace(local_src_path,"")
          # 如果該ToolName已經存在於 no_compress_file 中，則將檔案名稱和路徑加入其對應的列表中
          if toolname in no_compress_file:
            no_compress_file[toolname].append([file_name,files[0]] )
          # 如果該ToolName不存在於 no_compress_file 中，則創建一個新的列表，並將檔案名稱和路徑加入其中
          else:
            no_compress_file[toolname] = [[ file_name,files[0] ]]
    return no_compress_file
