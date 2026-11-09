import unittest
import json
import os
import sys

# Ensure import from current directory
sys.path.insert(0, os.path.dirname(__file__))

from app import app, mask_pii
from database import init_db, get_db
from seed_data import seed_database

class CampusTradePlatformTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Initialize and seed database with test data
        seed_database()

    def setUp(self):
        self.app = app
        self.client = self.app.test_client()
        self.app.config["TESTING"] = True

    # -------------------------------------------------------------
    # 入門功能測試 (Features 1 - 10)
    # -------------------------------------------------------------
    def test_01_product_card_list(self):
        """Feature 1: 商品卡片列表 - 顯示照片、名稱、價格及所屬學校"""
        response = self.client.get("/api/products")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("products", data)
        self.assertGreater(len(data["products"]), 0)
        p = data["products"][0]
        self.assertTrue(len(p["title"]) > 0)
        self.assertIsInstance(p["price"], int)
        self.assertTrue(len(p["school"]) > 0)
        self.assertIsInstance(p["images"], list)
        self.assertGreater(len(p["images"]), 0)

    def test_02_product_detail(self):
        """Feature 2: 商品詳細頁 - 查看描述、新舊程度、交易方式與賣家資料"""
        response = self.client.get("/api/products/1")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data["success"])
        p = data["product"]
        self.assertEqual(p["id"], 1)
        self.assertTrue(len(p["description"]) > 0)
        self.assertTrue(len(p["condition"]) > 0)
        self.assertIn("trade_types", p)
        self.assertTrue(len(p["seller_name"]) > 0)
        self.assertIn("seller_rating", p)

    def test_03_product_category_filter(self):
        """Feature 3: 商品分類篩選 - 課本、電子產品、家具、生活用品等"""
        response = self.client.get("/api/products?category=課本教材")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        for p in data["products"]:
            self.assertEqual(p["category"], "課本教材")

        response_3c = self.client.get("/api/products?category=3C電子")
        self.assertEqual(response_3c.status_code, 200)
        data_3c = json.loads(response_3c.data)
        for p in data_3c["products"]:
            self.assertEqual(p["category"], "3C電子")

    def test_04_keyword_search(self):
        """Feature 4: 關鍵字搜尋 - 搜尋名稱及描述，無結果時正常回傳空陣列"""
        # Keyword match
        response = self.client.get("/api/products?keyword=微積分")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertGreaterEqual(len(data["products"]), 1)
        self.assertTrue(any("微積分" in p["title"] for p in data["products"]))
        for p in data["products"]:
            self.assertTrue("微積分" in p["title"] or "微積分" in p["description"])

        # No results match
        empty_res = self.client.get("/api/products?keyword=完全不存在之稀奇商品999")
        self.assertEqual(empty_res.status_code, 200)
        empty_data = json.loads(empty_res.data)
        self.assertEqual(len(empty_data["products"]), 0)

    def test_05_price_range_filter(self):
        """Feature 5: 價格範圍篩選 - 輸入最低及最高價格"""
        response = self.client.get("/api/products?min_price=100&max_price=1000")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        for p in data["products"]:
            self.assertGreaterEqual(p["price"], 100)
            self.assertLessEqual(p["price"], 1000)

    def test_06_school_filter(self):
        """Feature 6: 學校與地區篩選 - 依學校篩選商品"""
        response = self.client.get("/api/products?school=國立臺灣大學")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        for p in data["products"]:
            self.assertEqual(p["school"], "國立臺灣大學")

    def test_07_product_sorting(self):
        """Feature 7: 商品排序 - 依最新上架、價格由低到高或由高到低"""
        # Price ascending
        res_asc = self.client.get("/api/products?sort_by=price_asc")
        data_asc = json.loads(res_asc.data)
        prices_asc = [p["price"] for p in data_asc["products"]]
        self.assertEqual(prices_asc, sorted(prices_asc))

        # Price descending
        res_desc = self.client.get("/api/products?sort_by=price_desc")
        data_desc = json.loads(res_desc.data)
        prices_desc = [p["price"] for p in data_desc["products"]]
        self.assertEqual(prices_desc, sorted(prices_desc, reverse=True))

    def test_08_trade_type_tags(self):
        """Feature 8: 交易方式標籤 - 買賣、交換或贈送支援多重標記"""
        res_gift = self.client.get("/api/products?trade_type=gift")
        data_gift = json.loads(res_gift.data)
        for p in data_gift["products"]:
            self.assertIn("gift", p["trade_types"])

        res_exchange = self.client.get("/api/products?trade_type=exchange")
        data_exchange = json.loads(res_exchange.data)
        for p in data_exchange["products"]:
            self.assertIn("exchange", p["trade_types"])

    def test_09_favorites_toggle_and_list(self):
        """Feature 9: 收藏清單 - 新增與取消收藏，跨裝置同步"""
        # Login as Bob
        self.client.post("/api/auth/login", json={"email": "bob@ntnu.edu.tw", "password": "password123"})

        # Toggle favorite product 2
        res_add = self.client.post("/api/favorites/toggle", json={"product_id": 2})
        data_add = json.loads(res_add.data)
        self.assertTrue(data_add["success"])
        self.assertTrue(data_add["is_favorited"])

        # Check in list
        res_list = self.client.get("/api/favorites")
        data_list = json.loads(res_list.data)
        fav_ids = [p["id"] for p in data_list["favorites"]]
        self.assertIn(2, fav_ids)

        # Toggle again to remove
        res_remove = self.client.post("/api/favorites/toggle", json={"product_id": 2})
        data_remove = json.loads(res_remove.data)
        self.assertFalse(data_remove["is_favorited"])

    def test_10_mobile_viewport_and_html(self):
        """Feature 10: 手機版介面 - 支援 RWD 視口與適配結構"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        html = response.data.decode("utf-8")
        self.assertIn('name="viewport"', html)
        self.assertIn("width=device-width", html)
        self.assertIn("校園二手寶", html)

    # -------------------------------------------------------------
    # 中階與進階功能測試 (Features 11 - 20)
    # -------------------------------------------------------------
    def test_11_auth_register_and_login(self):
        """Feature 11: 會員註冊與登入 - 以電子郵件註冊，提供登入、登出"""
        test_email = "test_student@ntu.edu.tw"
        # Register with .edu.tw
        reg_res = self.client.post("/api/auth/register", json={
            "email": test_email,
            "password": "mypassword123",
            "nickname": "新進學生",
            "school": "國立臺灣大學",
            "department": "物理學系"
        })
        self.assertEqual(reg_res.status_code, 200)
        reg_data = json.loads(reg_res.data)
        self.assertTrue(reg_data["success"])
        self.assertEqual(reg_data["user"]["is_edu_verified"], 1)

        # Logout
        self.client.post("/api/auth/logout")

        # Login
        login_res = self.client.post("/api/auth/login", json={
            "email": test_email,
            "password": "mypassword123"
        })
        self.assertEqual(login_res.status_code, 200)
        login_data = json.loads(login_res.data)
        self.assertTrue(login_data["success"])

    def test_12_profile_and_storefront(self):
        """Feature 12: 個人檔案與賣場 - 管理暱稱、學校、展示在售物品"""
        self.client.post("/api/auth/login", json={"email": "alice@ntu.edu.tw", "password": "password123"})
        res = self.client.get("/api/auth/me")
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data["logged_in"])
        self.assertEqual(data["user"]["nickname"], "愛麗絲")
        self.assertEqual(data["user"]["school"], "國立臺灣大學")

    def test_13_create_product_and_validation(self):
        """Feature 13: 商品上架與必填欄位檢查"""
        self.client.post("/api/auth/login", json={"email": "alice@ntu.edu.tw", "password": "password123"})
        
        # Missing title should fail
        fail_res = self.client.post("/api/products", json={"title": "", "price": 100})
        self.assertEqual(fail_res.status_code, 400)

        # Successful listing
        success_res = self.client.post("/api/products", json={
            "title": "單晶片微電腦實作教材 (含 Arduino 開發板)",
            "description": "大三實驗課使用完畢，晶片與線材皆齊全，功能正常。",
            "category": "3C電子",
            "condition": "9成新",
            "price": 450,
            "original_price": 1200,
            "trade_types": ["sell", "exchange"],
            "exchange_wish": "可換 Raspberry Pi 相關配件",
            "meetup_location": "資工系德田館大廳"
        })
        self.assertEqual(success_res.status_code, 200)
        data = json.loads(success_res.data)
        self.assertTrue(data["success"])
        self.assertIn("product_id", data)

    def test_14_product_status_tracking(self):
        """Feature 14: 商品管理與狀態追蹤 - 上架中、預約中、交易完成"""
        self.client.post("/api/auth/login", json={"email": "alice@ntu.edu.tw", "password": "password123"})
        
        # Change status of product 1 to 'reserved'
        res = self.client.post("/api/products/1/status", json={"status": "reserved"})
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data["success"])

        # Verify status in detail API
        detail = json.loads(self.client.get("/api/products/1").data)
        self.assertEqual(detail["product"]["status"], "reserved")

        # Revert back to active
        self.client.post("/api/products/1/status", json={"status": "active"})

    def test_15_exchange_wish_setting(self):
        """Feature 15: 交換意願設定 - 填寫希望交換物品及是否補差價"""
        detail = json.loads(self.client.get("/api/products/1").data)
        p = detail["product"]
        self.assertIn("exchange", p["trade_types"])
        self.assertTrue(len(p["exchange_wish"]) > 0)
        self.assertEqual(p["allow_price_diff"], 1)

    def test_16_public_qa_with_pii_filtering(self):
        """Feature 16: 商品公開問答與個資安全防護過濾 (屏蔽電話號碼與地址)"""
        # Test mask_pii directly
        masked_phone = mask_pii("有興趣，請加我手機 0912-345-678 聯絡")
        self.assertNotIn("0912-345-678", masked_phone)
        self.assertIn("0912-***-***", masked_phone)

        # Post Q&A through endpoint
        self.client.post("/api/auth/login", json={"email": "bob@ntnu.edu.tw", "password": "password123"})
        res = self.client.post("/api/products/1/qa", json={
            "question": "可以約今天嗎？我住在女一舍301室，電話0988776655"
        })
        self.assertEqual(res.status_code, 200)

        # Verify masked result in product Q&A list
        p_data = json.loads(self.client.get("/api/products/1").data)
        qa = p_data["product"]["qa_list"][-1]
        self.assertNotIn("0988776655", qa["question"])
        self.assertIn("0988-***-***", qa["question"])

    def test_17_transactions_and_ratings(self):
        """Feature 17: 交易紀錄查看與評價制度"""
        self.client.post("/api/auth/login", json={"email": "alice@ntu.edu.tw", "password": "password123"})
        res = self.client.get("/api/transactions")
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertGreaterEqual(len(data["transactions"]), 1)
        tx = data["transactions"][0]
        self.assertIn("buyer_rating", tx)
        self.assertIn("seller_rating", tx)

    def test_18_notifications(self):
        """Feature 18: 站內通知 - 提醒新出價、降價與狀態，可標記已讀"""
        self.client.post("/api/auth/login", json={"email": "alice@ntu.edu.tw", "password": "password123"})
        res = self.client.get("/api/notifications")
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertIn("notifications", data)
        self.assertIn("unread_count", data)

        # Mark all read
        res_read = self.client.post("/api/notifications/read_all")
        self.assertEqual(res_read.status_code, 200)
        res_after = self.client.get("/api/notifications")
        self.assertEqual(json.loads(res_after.data)["unread_count"], 0)

    def test_19_reports_and_admin(self):
        """Feature 19: 檢舉與管理員後台 - 管理商品檢舉並處理爭議"""
        # User Bob submits a report
        self.client.post("/api/auth/login", json={"email": "bob@ntnu.edu.tw", "password": "password123"})
        rep_res = self.client.post("/api/reports", json={
            "target_type": "product",
            "target_id": 8,
            "reason": "商品疑似有電線接觸不良問題，申請管理員審查"
        })
        self.assertEqual(rep_res.status_code, 200)

        # Admin login
        self.client.post("/api/auth/login", json={"email": "admin@campus.edu.tw", "password": "password123"})
        admin_res = self.client.get("/api/admin/reports")
        self.assertEqual(admin_res.status_code, 200)
        reports = json.loads(admin_res.data)["reports"]
        self.assertGreater(len(reports), 0)

        # Resolve report with delist action
        latest_report_id = reports[0]["id"]
        resolve_res = self.client.post(f"/api/admin/reports/{latest_report_id}/resolve", json={
            "action": "dismiss",
            "notes": "經確認商品已由原廠檢測正常，駁回檢舉"
        })
        self.assertEqual(resolve_res.status_code, 200)

    def test_20_campus_edu_verification(self):
        """Feature 20: 校園身分驗證 - 驗證學校信箱 (.edu.tw)"""
        # Login Charlie (initially gmail / unverified)
        self.client.post("/api/auth/login", json={"email": "charlie@gmail.com", "password": "password123"})
        
        # Invalid email (not .edu.tw)
        fail_res = self.client.post("/api/auth/verify_edu", json={"edu_email": "charlie@yahoo.com"})
        self.assertEqual(fail_res.status_code, 400)

        # Valid .edu.tw email
        succ_res = self.client.post("/api/auth/verify_edu", json={"edu_email": "charlie@nycu.edu.tw"})
        self.assertEqual(succ_res.status_code, 200)
        self.assertTrue(json.loads(succ_res.data)["success"])

    # -------------------------------------------------------------
    # 4 大 AI 智慧功能測試
    # -------------------------------------------------------------
    def test_21_ai_recognize_photo(self):
        """AI Feature 1: AI 拍照自動上架 - 上傳照片自動辨識商品類型與產生介紹"""
        res = self.client.post("/api/ai/recognize_photo", json={"sample_type": "calculus_book"})
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data["success"])
        item = data["recognized"]
        self.assertIn("Calculus", item["title"])
        self.assertEqual(item["category"], "課本教材")
        self.assertIn("ISBN", item["description"])
        self.assertGreater(item["suggested_price"], 0)

    def test_22_ai_estimate_price(self):
        """AI Feature 2: AI 二手商品價格建議 - 估算合理售價區間 (標記估算值)"""
        res = self.client.post("/api/ai/estimate_price", json={
            "category": "3C電子",
            "condition": "9成新",
            "original_price": 10000,
            "usage_years": 1.5
        })
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data["success"])
        self.assertIn("price_range", data)
        self.assertIn("估算值", data["disclaimer"])
        self.assertGreater(data["estimated_price"], 0)

    def test_23_ai_assistant_nlp_search(self):
        """AI Feature 3: AI 購物問答助手 - 用自然語言描述需求，AI 協助搜尋與篩選"""
        res = self.client.post("/api/ai/assistant", json={
            "prompt": "想找 3000 元以下上課寫筆記的二手平板或 3C 配件"
        })
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data["success"])
        self.assertEqual(data["analysis"]["category"], "3C電子")
        self.assertEqual(data["analysis"]["max_budget"], 3000)
        self.assertIn("recommendations", data)

    def test_24_ai_personalized_recommendations(self):
        """AI Feature 4: AI 個人化商品推薦 - 根據學校與熱門度推薦相關商品"""
        res = self.client.get("/api/ai/recommendations")
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertIn("recommendations", data)
        self.assertGreaterEqual(len(data["recommendations"]), 1)

    # -------------------------------------------------------------
    # 端到端整合流程測試 (E2E Complete User Journey)
    # -------------------------------------------------------------
    def test_25_e2e_complete_trading_journey(self):
        """E2E 整合測試：從 AI 拍照上架 ➔ 搜尋瀏覽 ➔ 私訊出價 ➔ 接受預約 ➔ 完成交易與互評"""
        # Step 1: Alice logs in and lists an item
        self.client.post("/api/auth/login", json={"email": "alice@ntu.edu.tw", "password": "password123"})
        ai_scan = self.client.post("/api/ai/recognize_photo", json={"sample_type": "ipad"})
        scan_data = json.loads(ai_scan.data)["recognized"]

        post_res = self.client.post("/api/products", json={
            "title": scan_data["title"],
            "description": scan_data["description"],
            "category": scan_data["category"],
            "condition": scan_data["condition"],
            "price": scan_data["suggested_price"],
            "original_price": scan_data["original_price"],
            "trade_types": ["sell"],
            "meetup_location": "台大第一活動中心小福廣場",
            "images": [scan_data["image"]]
        })
        new_prod_id = json.loads(post_res.data)["product_id"]

        # Step 2: Bob logs in and searches for the item
        self.client.post("/api/auth/login", json={"email": "bob@ntnu.edu.tw", "password": "password123"})
        search_res = self.client.get(f"/api/products?keyword=iPad")
        search_items = json.loads(search_res.data)["products"]
        self.assertTrue(any(p["id"] == new_prod_id for p in search_items))

        # Step 3: Bob starts a chat with Alice
        chat_start = self.client.post("/api/chats/start", json={"product_id": new_prod_id})
        chat_id = json.loads(chat_start.data)["chat_id"]

        # Step 4: Bob makes a counter-offer
        self.client.post(f"/api/chats/{chat_id}/send", json={
            "message_type": "offer",
            "content": "學姊好！如果今天在台大面交，6500 元可以嗎？",
            "offer_price": 6500
        })

        # Step 5: Alice logs in and accepts the offer
        self.client.post("/api/auth/login", json={"email": "alice@ntu.edu.tw", "password": "password123"})
        self.client.post(f"/api/chats/{chat_id}/send", json={
            "message_type": "offer_accepted",
            "content": "沒問題，以 NT$ 6500 成交！",
            "offer_price": 6500
        })

        # Verify product is now reserved
        prod_detail = json.loads(self.client.get(f"/api/products/{new_prod_id}").data)["product"]
        self.assertEqual(prod_detail["status"], "reserved")

        # Step 6: Alice completes transaction with Bob
        comp_res = self.client.post("/api/transactions/complete", json={
            "product_id": new_prod_id,
            "buyer_id": 3, # Bob's ID
            "final_price": 6500,
            "trade_type": "buy",
            "meetup_location": "台大第一活動中心小福廣場"
        })
        self.assertTrue(json.loads(comp_res.data)["success"])

        # Verify product status is now completed
        prod_final = json.loads(self.client.get(f"/api/products/{new_prod_id}").data)["product"]
        self.assertEqual(prod_final["status"], "completed")

        # Step 7: Bob reviews the transaction
        self.client.post("/api/auth/login", json={"email": "bob@ntnu.edu.tw", "password": "password123"})
        tx_list = json.loads(self.client.get("/api/transactions").data)["transactions"]
        latest_tx_id = tx_list[0]["id"]

        rev_res = self.client.post(f"/api/transactions/{latest_tx_id}/review", json={
            "rating": 5,
            "review": "商品保存極佳，賣家親切守時，極力推薦！"
        })
        self.assertTrue(json.loads(rev_res.data)["success"])

    # -------------------------------------------------------------
    # 50 筆生成測試資料與電腦照片 AI 辨識完整驗證
    # -------------------------------------------------------------
    def test_26_fifty_seed_products_verification(self):
        """驗證 50 筆生成測試資料之完整規格 (數量、分類多樣性、價格區間、交易方式)"""
        # Re-seed to get clean 50 products state
        seed_database()
        
        res = self.client.get("/api/products")
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        products = data["products"]
        
        # 1. 驗證商品總數恰為 50 筆
        self.assertEqual(len(products), 50, f"預期有 50 筆商品，實際為 {len(products)} 筆")
        
        # 2. 驗證各大分類皆有豐富涵蓋
        categories = set(p["category"] for p in products)
        expected_cats = {"課本教材", "3C電子", "宿舍家具", "生活用品", "運動服飾"}
        self.assertTrue(expected_cats.issubset(categories), f"分類缺少: {expected_cats - categories}")
        
        # 3. 驗證大專院校涵蓋多元校園
        schools = set(p["school"] for p in products)
        self.assertIn("國立臺灣大學", schools)
        self.assertIn("國立臺灣師範大學", schools)
        self.assertIn("國立成功大學", schools)
        self.assertIn("國立清華大學", schools)
        self.assertIn("國立陽明交通大學", schools)
        self.assertIn("國立政治大學", schools)
        
        # 4. 驗證交易標籤包含買賣、交換、免費贈送
        trade_types_all = set()
        for p in products:
            for t in p["trade_types"]:
                trade_types_all.add(t)
        self.assertIn("sell", trade_types_all)
        self.assertIn("exchange", trade_types_all)
        self.assertIn("gift", trade_types_all)
        
        # 5. 驗證價格分佈 (包含 NT$0 免費贈送與高價 3C)
        prices = [p["price"] for p in products]
        self.assertIn(0, prices, "應包含 NT$ 0 免費贈送品項")
        self.assertTrue(any(price >= 5000 for price in prices), "應包含高價值 3C 品項")
        
        # 6. 驗證每筆資料之必填欄位完整性
        for p in products:
            self.assertTrue(p["id"] > 0)
            self.assertTrue(len(p["title"]) > 0)
            self.assertTrue(len(p["description"]) > 0)
            self.assertTrue(len(p["condition"]) > 0)
            self.assertTrue(len(p["school"]) > 0)
            self.assertTrue(len(p["city"]) > 0)
            self.assertIsInstance(p["images"], list)
            self.assertGreater(len(p["images"]), 0)

    def test_27_ai_photo_computer_upload_and_recognition(self):
        """驗證從電腦選取照片 (Base64 + 本機檔名)，AI 自動辨識品項名稱、分類與建議行情"""
        # 模擬本機電腦圖片 Base64
        mock_image_base64 = "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEASABIAAD/2wBDAP//////////////////////////////////////////////////////////////////////////////////////wgALCAABAAEBAREA/8QAFBABAAAAAAAAAAAAAAAAAAAAAP/aAAgBAQABPxA="

        # 情境 A: 使用者從電腦選取微積分課本照片
        res_calc = self.client.post("/api/ai/recognize_photo", json={
            "filename": "Calculus_Stewart_8th.jpg",
            "image_data": mock_image_base64
        })
        self.assertEqual(res_calc.status_code, 200)
        data_calc = json.loads(res_calc.data)["recognized"]
        self.assertIn("Calculus", data_calc["title"])
        self.assertEqual(data_calc["category"], "課本教材")
        self.assertEqual(data_calc["image"], mock_image_base64, "應保留使用者電腦上傳之原圖")

        # 情境 B: 使用者從電腦選取 iPad 照片
        res_ipad = self.client.post("/api/ai/recognize_photo", json={
            "filename": "my_apple_ipad_photo.png",
            "image_data": mock_image_base64
        })
        self.assertEqual(res_ipad.status_code, 200)
        data_ipad = json.loads(res_ipad.data)["recognized"]
        self.assertIn("iPad", data_ipad["title"])
        self.assertEqual(data_ipad["category"], "3C電子")
        self.assertGreater(data_ipad["suggested_price"], 3000)

        # 情境 C: 使用者從電腦選取 IKEA 人體工學椅照片
        res_chair = self.client.post("/api/ai/recognize_photo", json={
            "filename": "IKEA_desk_chair.jpeg",
            "image_data": mock_image_base64
        })
        self.assertEqual(res_chair.status_code, 200)
        data_chair = json.loads(res_chair.data)["recognized"]
        self.assertIn("IKEA", data_chair["title"])
        self.assertEqual(data_chair["category"], "宿舍家具")

        # 情境 D: 使用者從電腦選取任一相片 (自動提取品名特徵)
        res_generic = self.client.post("/api/ai/recognize_photo", json={
            "filename": "IMG_20261102_1430.jpg",
            "image_data": mock_image_base64
        })
        self.assertEqual(res_generic.status_code, 200)
        data_generic = json.loads(res_generic.data)["recognized"]
        self.assertTrue(len(data_generic["title"]) > 0)
        self.assertEqual(data_generic["image"], mock_image_base64)

    def test_28_create_product_with_computer_photos(self):
        """驗證直接以電腦選取之多張照片 (Base64) 進行刊登與顯示"""
        self.client.post("/api/auth/login", json={"email": "alice@ntu.edu.tw", "password": "password123"})
        
        local_img1 = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
        local_img2 = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="

        res = self.client.post("/api/products", json={
            "title": "電腦相片實測：Logitech 羅技無線滑鼠 (含本機上傳圖片)",
            "description": "這是直接從電腦選取相片上傳刊登的測試商品！",
            "category": "3C電子",
            "condition": "9成新",
            "price": 490,
            "original_price": 990,
            "trade_types": ["sell"],
            "meetup_location": "台大公館捷運站出口",
            "images": [local_img1, local_img2]
        })
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        prod_id = data["product_id"]

        # 檢視商品詳細資料，確認多張本機照片正確儲存
        detail_res = self.client.get(f"/api/products/{prod_id}")
        prod = json.loads(detail_res.data)["product"]
        self.assertEqual(len(prod["images"]), 2)
        self.assertEqual(prod["images"][0], local_img1)
        self.assertEqual(prod["images"][1], local_img2)

if __name__ == "__main__":
    unittest.main()
