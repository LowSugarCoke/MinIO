"""
作者: Mina
日期: 2023-02-20
版權: TSMC
"""
# 導入相關套件
from minio_uploader import MinioUploader  # 導入 Minio 上傳套件
from log_processor import LogProcessor  # 導入日誌處理套件
from log_judge import LogJudge  # 導入日誌處理器
import getpass  # 導入密碼輸入套件
import time  # 導入時間套件

# 設定相關參數
endpoint_url = ""  # 設定 Minio 終端節點位址
bucket_name = ""  # 設定 Bucket 名稱
minio_folder = ""  # 設定 Minio 上傳路徑
local_src_path = "logs/"  # 設定日誌檔案的本機資料夾路徑
tool_names_file = "tool_name.txt"  # 設定工具名稱檔案路徑


def main():
  # 輸入 Minio access key
  access_key = getpass.getpass(prompt='Please enter your access key: ')
  # 輸入 Minio secret key
  secret_key = getpass.getpass(prompt='Please enter your secret key: ')

  # 初始化 Minio 上傳客戶端
  minio_client = MinioUploader(access_key, secret_key, endpoint_url,
                               bucket_name)

  # 初始化日誌處理器
  log_judge = LogJudge()
  log_processor = LogProcessor()

  while True:
    # 檢查日誌資料夾大小是否超過 5 GB
    is_above_5_g = log_judge.is_folder_size_above_5_g(local_src_path)
    if is_above_5_g == False:
      # 取得超過兩天未更新的日誌檔案
      need_to_update_files = log_judge.get_file_above_two_days(local_src_path)
    else:
      # 取得日誌檔案資料夾內所有檔案
      need_to_update_files = log_judge.get_file_in_folder(local_src_path)

    # 讀取工具名稱檔案
    log_processor.read_toolname(tool_names_file)
    # 根據工具名稱將檔案分類
    classify_files = log_processor.classify_files_by_toolname(
      need_to_update_files)
    # 取得需要壓縮的檔案
    compress_files = log_processor.get_compress_files(classify_files)
    # 取得不需要壓縮的檔案
    no_compress_files = log_processor.get_no_compress_name_files(
      classify_files, local_src_path)
    # 將檔案加入上傳清單
    to_update_files = {**compress_files, **no_compress_files}

    # 上傳檔案至 Minio
    minio_client.upload_files(minio_folder, to_update_files)

    # 等待 60 秒
    time.sleep(60)


if __name__ == '__main__':
  main()
