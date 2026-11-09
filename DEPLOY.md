# 全國大學生二手物品交換與買賣平台 - Vercel 線上部署全指南 (DEPLOY.md)

本專案已完成 **Vercel Serverless Function** 完整適配架構（包含 `api/index.py`、`vercel.json` 及 `/tmp` SQLite 自動冷啟動同步機制）。

---

## ⚡ 核心適配架構（已為您配置完成）

1. **Vercel 路由設定 (`vercel.json`)**：
   所有頁面與 API 請求（`/(.*)`）皆自動重寫轉發至 `api/index.py` Serverless 處理器。
2. **WSGI 入口 (`api/index.py`)**：
   自動將根目錄加入模組路徑，匯出 Flask `app` 物件供 Vercel 原生 Python 執行環境呼叫。
3. **SQLite 唯讀檔案系統相容機制 (`database.py`)**：
   Vercel 雲端函式執行時，工作目錄為唯讀（Read-Only）。專案已內建智慧檢測：當於 Vercel 環境執行時，自動將預先載入 50 筆商品的資料庫複製至唯一具備讀寫權限的 `/tmp/campus_trade.db`，確保會員登入、刊登寶物與公開留言等功能 100% 正常寫入！

---

## 🚀 方式一：透過 GitHub + Vercel 網頁端部署（最推薦、零指令、1 分鐘搞定）

此方式完全不需要安裝 Node.js 或 Vercel CLI，只需將程式碼推送至 GitHub，即可享有 **自動持續整合 (CI/CD)**，未來每次更新程式碼只要 `git push`，Vercel 就會自動重新發布！

### 步驟 1：在 GitHub 建立新儲存庫並推送程式碼
專案本地已完成 Git 初始化並打好 Commit，您只需在 GitHub 建立一個新專案（例如命名為 `campus-trade-platform`），然後在終端機執行：

```bash
cd /Users/comet/.gemini/antigravity/scratch/campus_trade_platform

# 關聯您的 GitHub 儲存庫（請將 <您的GitHub帳號> 替換為您的實際帳號）
git remote add origin https://github.com/<您的GitHub帳號>/campus-trade-platform.git

# 推送至 main 分支
git push -u origin main
```

### 步驟 2：登入 Vercel 並匯入專案
1. 打開瀏覽器訪問 **[https://vercel.com](https://vercel.com)** 並登入（可直接使用 GitHub 帳號快速登入）。
2. 在 Dashboard 右上方點擊 **「Add New...」➔「Project」**。
3. 在「Import Git Repository」列表中，找到您剛才建立的 **`campus-trade-platform`**，點擊旁邊的 **「Import」**。

### 步驟 3：點擊「Deploy」完成發布
1. **Project Name**：可自訂專案名稱（將決定您的網址前綴，如 `campus-trade.vercel.app`）。
2. **Framework Preset**：保持預設的 **`Other`**（Vercel 會自動辨識根目錄的 `vercel.json` 與 `api/index.py`）。
3. **Root Directory**：保持 `./`。
4. **Environment Variables**：無須設定（已內建預設值）。
5. 直接點擊下方藍色的 **「Deploy」** 按鈕！

> 🎉 **大功告成**：等待約 1 分鐘，Vercel 即會發布完成，並提供一個專屬的正式線上網址（例如 `https://campus-trade-platform.vercel.app`），自帶免費 SSL 安全憑證！

---

## 💻 方式二：使用 Vercel CLI 在本機直接部署

如果您不想經過 GitHub，也可以使用 Vercel CLI 直接從本機發布：

1. **安裝 Vercel CLI**（需先有 Node.js 環境）：
   ```bash
   npm i -g vercel
   ```
2. **執行部署指令**：
   ```bash
   cd /Users/comet/.gemini/antigravity/scratch/campus_trade_platform
   vercel
   ```
3. 依照終端機提示：
   - `Set up and deploy?` ➔ 按 `y`
   - `Which scope?` ➔ 選擇您的帳號
   - `Link to existing project?` ➔ 按 `N`
   - `What's your project's name?` ➔ 輸入 `campus-trade-platform`
   - `In which directory is your code located?` ➔ 按 Enter (預設 `./`)
4. 發布至正式環境：
   ```bash
   vercel --prod
   ```

---

## 🔍 部署後常見問題與檢查清單

| 檢查項目 | 說明與排查 |
| :--- | :--- |
| **首頁是否正常載入** | 打開 `https://<專案名>.vercel.app`，確認熱血漫畫風首頁正常展示 |
| **50 筆商品是否正常顯示** | 首頁市集應立即載入 50 筆商品（包含微積分課本、iPad、IKEA 宿舍椅等） |
| **AI 電腦照片辨識** | 點擊「✨ 拍照秒上架」，直接從本機選擇照片，確認能正常辨識品項名稱 |
| **會員登入測試** | 使用預設帳號 `alice@ntu.edu.tw`，密碼 `password123` 測試登入與刊登 |
| **Log 日誌檢視** | 若遇到錯誤，可至 Vercel Dashboard ➔「Logs」分頁查看即時執行記錄 |
