# 全國大學生二手物品交換與買賣平台 (Campus Trade Platform)
> **Vibe Coding 進階功能與大作業成果整套交付**  
> 專題定位：實用型・校園電商・AI 應用

---

## 🌟 專題成果總覽

本專案依據教育部與大專院校 Vibe Coding 課程規格，完整實作兩份教學文件中的所有要求：
- ✅ **10 項入門功能（編號 1 至 10）**：商品卡片列表、商品詳細頁、5大分類、關鍵字搜尋、價格篩選、學校/地區篩選、3種排序、買賣/交換/贈送標籤、收藏清單、RWD 手機版介面。
- ✅ **10 項中階功能（編號 11 至 20）**：會員註冊登入、個人檔案賣場、商品上架照片驗證、商品狀態追蹤（上架中/預約中/已完成/已下架）、以物易物交換意向與補差價、商品公開問答（含自動屏蔽手機與地址敏感個資）、交易歷史紀錄、站內通知推播、檢舉與管理員後台仲裁、學校 `.edu.tw` 信箱認證機制。
- ✅ **4 大 AI 智慧功能**：
  1. **AI 拍照自動上架**：拍攝或上傳課本/3C照片，AI 自動辨識書名、ISBN、分類與狀況，一鍵生成商品介紹。
  2. **AI 二手商品價格建議**：依據年份、原價、品況與歷史成交大數據，計算合理售價區間（清楚標記「估算值」）。
  3. **AI 自然語言購物問答助手**：輸入「找 3000 元以下上課筆記平板」，AI 自動解析語意、品類與預算並推薦商品。
  4. **AI 個人化商品推薦**：依據就讀學校、科系與瀏覽熱門度進行個人化關聯推薦。
- ✅ **全套自動化測試套件（UnitTest / E2E）**：25 項全自動測試，覆蓋所有 API 與真實端到端交易旅程。

---

## 🚀 快速啟動與操作方式

### 1. 啟動伺服器
請於終端機執行下列指令啟動 Flask 網站伺服器：
```bash
cd /Users/comet/.gemini/antigravity/scratch/campus_trade_platform
python3 app.py
```
啟動後於瀏覽器開啟：`http://127.0.0.1:5050` (避開 macOS 預設 5000 AirPlay 佔用)

### 2. 測試帳號清單（預設密碼均為 `password123`）
| 身分 | 電子郵件 | 學校 / 學系 | 角色權限與測試重點 |
| :--- | :--- | :--- | :--- |
| **管理員** | `admin@campus.edu.tw` | 國立臺灣大學 資訊工程學系 | 管理員權限，可進入後台審查檢舉案件並執行下架處置 |
| **一般學生** | `alice@ntu.edu.tw` | 國立臺灣大學 資訊工程學系 | 已通過 `.edu.tw` 驗證，刊登微積分課本與檯燈贈送之賣家 |
| **一般學生** | `bob@ntnu.edu.tw` | 國立臺灣師範大學 英語學系 | 已通過驗證，刊登 iPad Air 4 與外套之賣家 |
| **待驗證學生** | `charlie@gmail.com` | 國立陽明交通大學 電機工程學系 | 測試「校園身分信箱驗證」流程 |
| **一般學生** | `diana@ncku.edu.tw` | 國立成功大學 建築學系 | 已通過驗證，刊登 Logitech 鍵盤之賣家 |

---

## 🧪 執行自動化測試

本專案內建完整的自動化測試套件，預先以測試資料對 24 項功能及 E2E 完整交易流程進行驗證：
```bash
cd /Users/comet/.gemini/antigravity/scratch/campus_trade_platform
python3 test_platform.py -v
```

**測試結果概況**：
```text
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

Ran 25 tests in 0.033s - OK
```

---

## 📄 繳交成果檔案清單
1. [`PRD.md`](./PRD.md)：產品定位、目標使用者、核心流程、選做功能與驗收條件。
2. [`UIUX.md`](./UIUX.md)：導覽架構圖、主要畫面、使用流程、字體色彩規範、邊界狀態。
3. [`app.py`](./app.py)：整合前端現代化 UI/UX Pro Max 介面與後端 API 完整系統。
4. [`test_platform.py`](./test_platform.py)：自動化單元測試與端到端測試程式。
5. [`seed_data.py`](./seed_data.py)：預載校園真實測試資料庫。
