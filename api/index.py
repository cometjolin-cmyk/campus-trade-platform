import os
import sys

# 將專案根目錄加入模組搜尋路徑
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(CURRENT_DIR)
if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)

from app import app

# Vercel Serverless Function WSGI 入口點
# 當 Vercel 呼叫時，會自動尋找名為 app 的 WSGI 物件
if __name__ == "__main__":
    app.run()
