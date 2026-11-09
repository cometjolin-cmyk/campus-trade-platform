# 使用輕量級 Python 3.11 基礎映像檔
FROM python:3.11-slim

# 設定工作目錄
WORKDIR /app

# 設定環境變數
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=5050

# 安裝系統依賴
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# 複製依賴檔案並安裝
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 複製專案原始碼與資料庫
COPY . .

# 初始化資料庫與 50 筆種子資料
RUN python3 seed_data.py

# 對外暴露埠號
EXPOSE 5050

# 以生產級 Gunicorn WSGI 伺服器啟動
CMD ["gunicorn", "--bind", "0.0.0.0:5050", "--workers", "2", "--threads", "4", "app:app"]
