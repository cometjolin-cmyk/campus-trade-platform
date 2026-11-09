import os
import sys

# 將專案根目錄加入模組搜尋路徑
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(CURRENT_DIR)
if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)

# 顯式匯入確保 Vercel Serverless 打包所有依賴模組
import database
import seed_data
from app import app

