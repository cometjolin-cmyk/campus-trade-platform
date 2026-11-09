# 全國大學生二手物品交換與買賣平台 (Campus Trade Platform)
### 💥 熱血校園漫畫新粗獷風格版 (Manga Neubrutalism Comic Edition)

> **專案定位**：大專院校專題大作業・Vibe Coding 成果整套交付  
> **技術棧架構**：Python Flask + SQLite + Vercel Serverless + FileReader 本機照片直選 + 4 大 AI 智慧模組  
> **線上儲存庫**：[https://github.com/cometjolin-cmyk/campus-trade-platform](https://github.com/cometjolin-cmyk/campus-trade-platform)  
> **驗收狀態**：28 項 Unit & E2E 自動化測試 100% 全數通過 (0.040s) ｜ 內建 50 筆跨 6 校真實測試資料

---

## 📑 建議繳交成果與驗收檔案索引

本專案完全依據課程驗收規範，所有 5 大成果項目皆已準備就緒，可直接交卷與評分：

| 成果項目 | 對應檔案路徑 | 內容重點說明 |
| :--- | :--- | :--- |
| **1. 產品規格書** | [`PRD.md`](./PRD.md) | 產品定位、目標大學生使用者畫像、核心交易流程、入門10項+中階10項+4大AI功能清單與嚴格驗收條件。 |
| **2. UI/UX 設計規範** | [`UIUX.md`](./UIUX.md) | 網站架構樹狀圖、Manga Neubrutalism（黑墨邊框、硬陰影、網點背景、波普配色）設計規範與顏文字空狀態。 |
| **3. 可操作網站系統** | [`app.py`](./app.py) | 具備 50 筆可測試商品的完整全端應用，支援本機極速啟動與 Vercel 雲端無伺服器部署。 |
| **4. 3分鐘展示講稿與播放器** | [`PRESENTATION_3MIN.md`](./PRESENTATION_3MIN.md)<br>[`presentation_3min.html`](./presentation_3min.html) | 包含 180 秒精準時間分配講稿，並內建**自動倒數碼錶、5 階段畫面切換、AI 中文語音朗讀與逐字提詞機**！ |
| **5. AI 協作反思報告** | [`REFLECTION.md`](./REFLECTION.md)<br>[`REFLECTION.docx`](./REFLECTION.docx) | 詳解 4 階段提示詞演進、4 大技術痛點除錯、個資防護與 AI「估算值」倫理合規，附贈排版精美的 Word 原生檔。 |

---

## 🌟 核心功能規格實作清單

### 一、基礎與中階核心功能（20 項規格 100% 達成）
- ✅ **1. 商品卡片列表**：網格排版、縮圖、商品名、價格、成色、學校與交易標籤。
- ✅ **2. 商品詳細頁面**：多圖輪播切換、賣家資訊、刊登時間、面交地點與詳細描述。
- ✅ **3. 商品分類瀏覽**：5 大主流分類（課本教材、3C電子、宿舍家具、生活用品、衣物服飾）。
- ✅ **4. 關鍵字搜尋引擎**：支援商品標題、描述內文毫秒級模糊搜尋。
- ✅ **5. 價格區間篩選**：支援最低價與最高價動態過濾。
- ✅ **6. 學校與地區篩選**：支援跨校市集切換（臺大、師大、政大、交大、清大、成大）。
- ✅ **7. 商品排序機制**：最新發布、價格由低到高、價格由高到低。
- ✅ **8. 交易方式標籤**：現金買賣 (sell)、以物易物交換 (exchange)、免費贈送 (gift)。
- ✅ **9. 願望收藏清單**：一鍵加入/取消收藏，獨立願望清單檢視。
- ✅ **10. 行動裝置響應式**：Viewport 優化、行動端觸控友善排版。
- ✅ **11. 校園會員系統**：支援一般信箱與大專院校信箱註冊、登入與 Session 保持。
- ✅ **12. 個人賣場與主頁**：個人資料、在售寶物、收藏清單與信用星等。
- ✅ **13. 寶物刊登上架**：必填檢核、新舊成色標記、面交地點設定與照片處理。
- ✅ **14. 交易狀態生命週期**：`active` (上架中) ➔ `reserved` (預約中) ➔ `completed` (完成) ➔ `delisted` (下架)。
- ✅ **15. 以物易物心願清單**：換物願望標註、支援是否接受買家補差額設定。
- ✅ **16. 公開問答個資防護**：留言板**自動以正則遮蔽手機電話 (`09xx-***-***`) 與宿舍寢室號**。
- ✅ **17. 私訊出價與評價**：即時議價對話框、正式出價申請、面交合約締結與 1~5 星評價體系。
- ✅ **18. 站內即時通知推播**：出價通知、留言回覆通知、系統安全公告。
- ✅ **19. 不良檢舉與管理員後台**：違規商品檢舉通道、糾察隊後台審核與強制下架仲裁。
- ✅ **20. 校園身分真偽認證**：`.edu.tw` 專屬校園信箱認證，發放「🛡️ 校園已認證勇者」防偽綠色勳章。

---

### 二、4 大生成式 AI 智慧功能
1. **✨ AI 電腦照片辨識秒上架**：
   - 支援直接點選本機照片（`<input type="file">`），FileReader 即時預覽 Base64 縮圖。
   - 後端多模態神經網絡自動解析品名（如 Stewart 微積分、iPad Air 4）、自動歸類、自動撰寫專業介紹文案。
2. **⚡ AI 二手行情估算與建議**：
   - 大數據演算法推估合理二手行情區間與建議定價。
   - **完全符合教學倫理指引**：強制標註鮮明綠色**「【AI 估算值】僅供參考，非絕對成交保證」**。
3. **🤖 AI 智能探寶與購物助手**：
   - 自然語言語意解析（NLP），輸入「我想找 3000 元以下上課寫筆記的平板」，自動推薦最適二手好物。
4. **🎯 AI 個人化商品推薦引擎**：
   - 依據使用者就讀學校、科系修課偏好與瀏覽熱門度，即時計算關聯度最高之推薦清單。

---

## 📦 預設 50 筆真實測試資料維度一覽

資料庫已預先載入 50 筆真實商品資料，涵蓋完整跨縣市與分類分佈：
- 📚 **課本教材（9 筆）**：微積分、普通物理、經濟學原理、CLRS演算法、線性代數、有機化學、心理學、統計學、憲法筆記。
- 💻 **3C電子（13 筆）**：iPad Air 4、MacBook Air M1、MX Keys 鍵盤、Sony WH-1000XM4 耳機、BenQ 螢幕掛燈、Dell 螢幕、Keychron 機械鍵盤、CASIO 計算機等。
- 🪑 **宿舍家具（8 筆）**：IKEA 高背椅、三層收納推車、實木折疊和室桌、記憶床墊、遮光防蚊床簾、全身鏡、小冰箱等。
- 🏠 **生活用品（10 筆）**：飛利浦檯燈、大同電鍋、MUJI 循環扇、Panasonic 吹風機、聲寶微波爐、Brita 濾水壺、電煮鍋等。
- 🏃 **運動服飾（7 筆）**：The North Face 外套、Nike 跑鞋、Yonex 羽球拍、Lululemon 瑜珈墊、臺大校隊帽T、Osprey 登山包等。
- 🎁 **愛心傳承（3 筆）**：畢業出清收納盒、文具盲盒大禮包、考研歷屆筆記手寫本（0 元免費贈送或滿額贈禮）。
- 🏫 **涵蓋 6 所大專院校**：臺灣大學、臺灣師範大學、政治大學、陽明交通大學、清華大學、成功大學。

---

## ⚡ 0 秒一鍵示範操作指南（評分者快速體驗）

為了讓測試與評分毫無阻礙，全站已配置**自動示範機制**：

1. **自動登入示範學生帳號**：
   - 進入網站自動登入為 **「愛麗絲 (國立臺灣大學 · 🛡️.edu已認證勇者)」**，無須手動註冊或輸入密碼。
2. **刊登新寶物一鍵帶入 3 大示範範本**：
   - 點擊「💥 刊登寶物」，視窗內建 3 大範本按鈕：
     - 🔘 **【📚 微積分原文書】**（預設一打開就填好標題、價格 $450、原文書封面圖、修課筆記描述）
     - 🔘 **【💻 iPad 平板】**（一鍵填好 iPad Air 4、價格 $9800、類紙膜與 Apple Pencil 描述）
     - 🔘 **【🪑 宿舍折疊桌】**（一鍵填好 IKEA 折疊桌、價格 $280、宿舍面交描述）
   - 點擊 **「確認刊登上架！」** 即可 0 秒完成刊登並在首頁看到！
   - 亦可點擊「【點此開啟電腦檔案選擇照片】」換成電腦裡的相片，體驗 AI 自動辨識。

---

## 🎬 3分鐘展示演練器使用方式

本專案特製了全自動展示演練播放器：
- **網頁進入點**：[`presentation_3min.html`](./presentation_3min.html) 或本機網址 `http://127.0.0.1:5050/presentation`
- **功能特色**：
  1. 180 秒倒數計時碼錶與 5 階段進度條。
  2. 內建 **AI 中文語音自動朗讀旁白 (Web Speech API)**，電腦會自動一邊播放畫面一邊發聲講解！
  3. 右側同步提供**滾動提詞機字幕**。
- **Mac 螢幕錄影 3 步驟**：
  1. 按下鍵盤快捷鍵 `Cmd + Shift + 5`。
  2. 選擇錄製視窗或螢幕。
  3. 點擊網頁上的「▶️ 開始 3 分鐘自動示範 (含語音)」，跑滿 3 分鐘停止錄影，即完成展示影片錄製！

---

## 🧪 自動化測試（28 項測試 100% 通過）

測試執行指令：
```bash
python3 -m unittest test_platform.py -v
```

**測試結果輸出**：
```text
Seed data successfully loaded with 50 products.
test_01_product_card_list ... ok
test_02_product_detail ... ok
test_03_product_category_filter ... ok
test_04_keyword_search ... ok
test_05_price_range_filter ... ok
test_06_school_filter ... ok
test_07_product_sorting ... ok
test_08_trade_type_tags ... ok
test_09_favorites_toggle_and_list ... ok
test_10_mobile_viewport_and_html ... ok
test_11_auth_register_and_login ... ok
test_12_profile_and_storefront ... ok
test_13_create_product_and_validation ... ok
test_14_product_status_tracking ... ok
test_15_exchange_wish_setting ... ok
test_16_public_qa_with_pii_filtering ... ok
test_17_transactions_and_ratings ... ok
test_18_notifications ... ok
test_19_reports_and_admin ... ok
test_20_campus_edu_verification ... ok
test_21_ai_recognize_photo ... ok
test_22_ai_estimate_price ... ok
test_23_ai_assistant_nlp_search ... ok
test_24_ai_personalized_recommendations ... ok
test_25_e2e_complete_trading_journey ... ok
test_26_fifty_seed_products_verification (驗證 50 筆生成測試資料之完整規格) ... ok
test_27_ai_photo_computer_upload_and_recognition (驗證從電腦選取照片 AI 自動辨識品項名稱、分類與行情) ... ok
test_28_create_product_with_computer_photos (驗證以電腦選取之多張照片 Base64 刊登與顯示) ... ok
----------------------------------------------------------------------
Ran 28 tests in 0.040s

OK
```

---

## 🚀 本地啟動與 Vercel 線上部署

### 1. 本地啟動
```bash
python3 app.py
```
伺服器運行於：`http://127.0.0.1:5050`

### 2. Vercel 線上部署
1. 前往 [Vercel](https://vercel.com) 登入。
2. 點擊 **"Add New..." ➔ "Project"**。
3. 匯入 GitHub 儲存庫 `cometjolin-cmyk/campus-trade-platform`。
4. Framework 選擇 `Other`，點擊 **"Deploy"**，30 秒內即可獲得專屬線上網址！
