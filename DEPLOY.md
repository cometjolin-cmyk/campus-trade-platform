# 全國大學生二手物品交換與買賣平台 - 線上部署指南 (DEPLOY.md)

本專案為標準 Python Flask + SQLite 輕量化全端架構，支援**即時公網穿透**與**主流雲端平台（PaaS / Docker）永久免費部署**。

---

## ⚡ 方式一：目前已啟動的即時線上公網網址 (免配置直接打開)

我們已透過安全反向代理通道，將您本地的 `http://127.0.0.1:5050` 映射至全球公網 HTTPS，任何手機或電腦皆可立即瀏覽：

- 🌐 **線上正式公網網址**：**[https://whqwc-220-135-111-77.run.pinggy-free.link](https://whqwc-220-135-111-77.run.pinggy-free.link)**
- 🌐 **備用公網網址**：**[https://axtyb-220-135-111-77.free.pinggy.net](https://axtyb-220-135-111-77.free.pinggy.net)**

> **說明**：此通道目前在您電腦背景運行中。若日後需要手動重啟穿透通道，只需在終端機執行：
> ```bash
> ssh -p 443 -R0:localhost:5050 -o StrictHostKeyChecking=no a.pinggy.io
> ```

---

## 🚀 方式二：永久雲端託管（推薦首選：Render.com 免費方案）

[Render.com](https://render.com/) 是目前託管 Python Flask + SQLite 最佳且完全免費的平台，具備免費自動 SSL 證書、GitHub 自動連動更新（Git Push 即自動發布）。

### 部署 4 步驟：

1. **建立 GitHub 儲存庫**：
   在專案目錄下初始化 Git 並推送至您的 GitHub：
   ```bash
   cd /Users/comet/.gemini/antigravity/scratch/campus_trade_platform
   git init
   git add .
   git commit -m "feat: Campus Trade Platform Manga Edition with 50 seed items"
   # 推送至您在 GitHub 建立的新 Repository (例如 campus-trade)
   git remote add origin https://github.com/<您的GitHub帳號>/campus-trade.git
   git push -u origin main
   ```

2. **登入 Render 並新增 Web Service**：
   - 瀏覽 [Render Dashboard](https://dashboard.render.com/)，點擊右上角 **「New +」➔「Web Service」**。
   - 選擇 **「Build and deploy from a Git repository」**，連結剛才推送的 GitHub Repo。

3. **填寫執行參數（專案內已預置 `Procfile` 與 `requirements.txt`）**：
   - **Name**: `campus-trade-platform`（或自訂）
   - **Region**: `Singapore` 或 `Oregon`
   - **Branch**: `main`
   - **Runtime**: `Python 3`
   - **Build Command**: 
     ```bash
     pip install -r requirements.txt && python seed_data.py
     ```
   - **Start Command**: 
     ```bash
     gunicorn app:app --bind 0.0.0.0:$PORT
     ```
   - **Instance Type**: 選擇 **Free**（完全免費）

4. **點擊「Create Web Service」**：
   - 等待約 2 分鐘建置完成，Render 將為您產出永久固定的專屬線上 HTTPS 網址（例如：`https://campus-trade-platform.onrender.com`）。

---

## 🛠️ 方式三：使用 Docker 容器化部署 (適用任何雲端主機)

專案根目錄下已配置完整生產級 [`Dockerfile`](file:///Users/comet/.gemini/antigravity/scratch/campus_trade_platform/Dockerfile)：

```bash
# 1. 本地或伺服器建置 Docker 映像檔
docker build -t campus-trade-platform:latest .

# 2. 啟動容器 (映射本機 5050 埠)
docker run -d -p 5050:5050 --name campus-app campus-trade-platform:latest
```

支援一鍵部署至：
- **GCP Cloud Run** (無伺服器容器，每個月有大量免費額度)
- **AWS App Runner / ECS**
- **Railway.app / Fly.io / Zeabur**
