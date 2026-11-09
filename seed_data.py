import json
from database import get_db, init_db, hash_password

def seed_database():
    init_db()
    conn = get_db()
    cursor = conn.cursor()

    # Clear existing data
    cursor.execute("DELETE FROM reports")
    cursor.execute("DELETE FROM notifications")
    cursor.execute("DELETE FROM transactions")
    cursor.execute("DELETE FROM chat_messages")
    cursor.execute("DELETE FROM chats")
    cursor.execute("DELETE FROM qa_messages")
    cursor.execute("DELETE FROM favorites")
    cursor.execute("DELETE FROM products")
    cursor.execute("DELETE FROM users")
    try:
        cursor.execute("DELETE FROM sqlite_sequence")
    except Exception:
        pass

    # 1. Seed Users
    users_data = [
        # 1. Admin
        ("admin@campus.edu.tw", hash_password("password123"), "系統管理員", "國立臺灣大學", "資訊工程學系", "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=150&q=80", 1, 1, 5.0, 50),
        # 2. Alice (NTU)
        ("alice@ntu.edu.tw", hash_password("password123"), "愛麗絲", "國立臺灣大學", "資訊工程學系", "https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&w=150&q=80", 1, 0, 4.9, 18),
        # 3. Bob (NTNU)
        ("bob@ntnu.edu.tw", hash_password("password123"), "鮑伯", "國立臺灣師範大學", "英語學系", "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=150&q=80", 1, 0, 4.8, 12),
        # 4. Charlie (NYCU - unverified initially for verification testing)
        ("charlie@gmail.com", hash_password("password123"), "查理", "國立陽明交通大學", "電機工程學系", "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&w=150&q=80", 0, 0, 4.5, 3),
        # 5. Diana (NCKU)
        ("diana@ncku.edu.tw", hash_password("password123"), "黛安娜", "國立成功大學", "建築學系", "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?auto=format&fit=crop&w=150&q=80", 1, 0, 5.0, 25),
        # 6. Evan (NTHU)
        ("evan@nthu.edu.tw", hash_password("password123"), "艾文", "國立清華大學", "動力機械工程學系", "https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?auto=format&fit=crop&w=150&q=80", 1, 0, 4.7, 8),
        # 7. Fiona (NCCU)
        ("fiona@nccu.edu.tw", hash_password("password123"), "費歐娜", "國立政治大學", "國際經營與貿易學系", "https://images.unsplash.com/photo-1517841905240-472988babdf9?auto=format&fit=crop&w=150&q=80", 1, 0, 4.9, 15),
    ]

    cursor.executemany("""
    INSERT INTO users (email, password_hash, nickname, school, department, avatar_url, is_edu_verified, is_admin, rating, rating_count)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, users_data)

    cursor.execute("SELECT id, email FROM users")
    email_map = {row["email"]: row["id"] for row in cursor.fetchall()}
    user_ids = {
        "admin": email_map["admin@campus.edu.tw"],
        "alice": email_map["alice@ntu.edu.tw"],
        "bob": email_map["bob@ntnu.edu.tw"],
        "charlie": email_map["charlie@gmail.com"],
        "diana": email_map["diana@ncku.edu.tw"],
        "evan": email_map["evan@nthu.edu.tw"],
        "fiona": email_map["fiona@nccu.edu.tw"]
    }

    # 2. Seed 50 Products
    products_data = [
        # Product 1: Textbook (Exchange / Sell)
        (
            user_ids["alice"],
            "Stewart Calculus: Early Transcendentals 微積分第 8 版 (原文書)",
            "台大資工必修課本，內含期中考重點標籤，無破損、無缺頁，前三章有鉛筆筆記。非常適合大一新生準備微積分課程！",
            "課本教材",
            "9成新",
            350,
            1250,
            json.dumps(["sell", "exchange"]),
            "希望交換：Halliday 普通物理學 (第10版) 或 補差價 NT$ 100",
            1,
            "國立臺灣大學",
            "台北市",
            "總圖書館正門門口",
            "active",
            json.dumps([
                "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?auto=format&fit=crop&w=600&q=80",
                "https://images.unsplash.com/photo-1497633762265-9d179a990aa6?auto=format&fit=crop&w=600&q=80"
            ]),
            128
        ),
        # Product 2: Free Gift (Lamp)
        (
            user_ids["alice"],
            "飛利浦 LED 護眼金屬檯燈 (大四畢業免費贈送新生)",
            "因為即將畢業搬離宿舍，將這台功能完全正常的檯燈免費贈送給需要的大一新生！光線柔和不閃爍，附原廠變壓器。",
            "生活用品",
            "8成新",
            0,
            980,
            json.dumps(["gift"]),
            "免費愛心傳承，以台大新生優先",
            0,
            "國立臺灣大學",
            "台北市",
            "大一女宿舍前廣場",
            "active",
            json.dumps([
                "https://images.unsplash.com/photo-1534353436294-0dbd4bdac845?auto=format&fit=crop&w=600&q=80"
            ]),
            86
        ),
        # Product 3: Electronics (iPad)
        (
            user_ids["bob"],
            "Apple iPad Air 4 (64GB 太空灰 WiFi 版，附原廠磁吸保護套)",
            "上課做 GoodNotes 筆記專用機，無撞傷敲痕，電池健康度 91%。功能完全正常，附原廠外盒與保護套，支援 Apple Pencil 2。",
            "3C電子",
            "9成新",
            8800,
            18900,
            json.dumps(["sell"]),
            "",
            1,
            "國立臺灣師範大學",
            "台北市",
            "師大校本部正門",
            "active",
            json.dumps([
                "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?auto=format&fit=crop&w=600&q=80"
            ]),
            245
        ),
        # Product 4: Furniture (IKEA Chair - Reserved)
        (
            user_ids["alice"],
            "IKEA 人體工學高背辦公椅 (透氣網布 / 氣壓升降正常)",
            "宿舍讀書必備人體工學椅，透氣不悶熱，腰靠支撐良好，因更換新椅子故廉讓。需自備推車或機車面交。",
            "宿舍家具",
            "8成新",
            650,
            1990,
            json.dumps(["sell", "exchange"]),
            "可換立扇或除濕盒",
            1,
            "國立臺灣大學",
            "台北市",
            "第一活動中心 (小福廣場)",
            "reserved",
            json.dumps([
                "https://images.unsplash.com/photo-1580481077195-c328a37db71a?auto=format&fit=crop&w=600&q=80"
            ]),
            310
        ),
        # Product 5: Electronics (Keyboard)
        (
            user_ids["diana"],
            "Logitech 羅技 MX Keys 智能無線背光鍵盤 (Mac/Win 雙系統)",
            "極致靜音剪刀腳手感，支援三台裝置一秒切換。手感極佳，外觀如新，附 Type-C 充電線與原廠接收器。",
            "3C電子",
            "9成新",
            1650,
            3490,
            json.dumps(["sell"]),
            "",
            1,
            "國立成功大學",
            "台南市",
            "成大光復校區中正堂門口",
            "active",
            json.dumps([
                "https://images.unsplash.com/photo-1587829741301-dc798b83add3?auto=format&fit=crop&w=600&q=80"
            ]),
            95
        ),
        # Product 6: Textbook (Algorithms)
        (
            user_ids["alice"],
            "Introduction to Algorithms (CLRS 3rd Edition 原文書)",
            "經典演算法聖經本（白皮厚本），資訊系考研必備，乾淨無塗鴉，書角有微翻摺痕跡，整體保存極佳。",
            "課本教材",
            "9成新",
            550,
            1800,
            json.dumps(["sell", "exchange"]),
            "想換：作業系統 Operating System Concepts (恐龍本)",
            1,
            "國立臺灣大學",
            "台北市",
            "總圖書館正門門口",
            "active",
            json.dumps([
                "https://images.unsplash.com/photo-1532012164546-f432f2e3ddb5?auto=format&fit=crop&w=600&q=80"
            ]),
            180
        ),
        # Product 7: Clothing
        (
            user_ids["bob"],
            "The North Face 防水連帽衝鋒防風外套 (深藍 男版 M)",
            "防風保暖騎機車通勤非常適合，下雨天防潑水，只穿過幾次，無髒污破損，已專業送洗乾淨。",
            "運動服飾",
            "9成新",
            1200,
            4500,
            json.dumps(["sell", "exchange"]),
            "可換 L 號其他大牌外套",
            1,
            "國立臺灣師範大學",
            "台北市",
            "師大公館校區大門",
            "active",
            json.dumps([
                "https://images.unsplash.com/photo-1548883354-7622d03aca27?auto=format&fit=crop&w=600&q=80"
            ]),
            72
        ),
        # Product 8: Daily item (Hair Dryer)
        (
            user_ids["diana"],
            "Panasonic 國際牌速乾大風量負離子吹風機 (粉金限定色)",
            "風量強大速乾，女生吹頭髮不費力。宿舍插座 110V 適用，功能正常良好。",
            "生活用品",
            "8成新",
            280,
            890,
            json.dumps(["sell", "gift"]),
            "清空房間，可小議",
            1,
            "國立成功大學",
            "台南市",
            "勝九舍管理員室前",
            "active",
            json.dumps([
                "https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?auto=format&fit=crop&w=600&q=80"
            ]),
            54
        ),
        # Product 9: Halliday Physics
        (
            user_ids["evan"],
            "Halliday & Resnick Fundamentals of Physics (普通物理學 第10版 原文書)",
            "清大工學院大一必修教材，涵蓋力學、電磁學完整習題，內頁乾淨無破損，附公式速查表。",
            "課本教材",
            "9成新",
            420,
            1350,
            json.dumps(["sell", "exchange"]),
            "想換：工程數學 Advanced Engineering Mathematics",
            1,
            "國立清華大學",
            "新竹市",
            "清大小吃部前廣場",
            "active",
            json.dumps(["https://images.unsplash.com/photo-1532012164546-f432f2e3ddb5?auto=format&fit=crop&w=600&q=80"]),
            92
        ),
        # Product 10: Mankiw Economics
        (
            user_ids["fiona"],
            "Mankiw Principles of Economics (經濟學原理 第9版 原文書)",
            "政大商學院大一必備聖經本，個體與總體經濟學圖表標記清晰，內頁乾淨，修完課廉讓給學弟妹。",
            "課本教材",
            "9成新",
            460,
            1400,
            json.dumps(["sell", "exchange"]),
            "可換初級會計學原文書",
            1,
            "國立政治大學",
            "台北市",
            "政大商學院大樓一樓",
            "active",
            json.dumps(["https://images.unsplash.com/photo-1497633762265-9d179a990aa6?auto=format&fit=crop&w=600&q=80"]),
            115
        ),
        # Product 11: Apple Pencil 2
        (
            user_ids["charlie"],
            "Apple Pencil 2代 (磁吸無線充電 / 筆尖磨損輕微 / 附矽膠握筆套)",
            "陽明交大電資做筆記繪圖專用，磁吸吸附充電良好，壓力感應無延遲，功能完全正常。",
            "3C電子",
            "9成新",
            2300,
            4390,
            json.dumps(["sell"]),
            "",
            1,
            "國立陽明交通大學",
            "新竹市",
            "光復校區浩然圖書館大門",
            "active",
            json.dumps(["https://images.unsplash.com/photo-1585336261026-4074ee969e54?auto=format&fit=crop&w=600&q=80"]),
            160
        ),
        # Product 12: Sony WH-1000XM4
        (
            user_ids["bob"],
            "Sony WH-1000XM4 頂級無線藍牙降噪耳罩耳機 (尊絕黑)",
            "圖書館讀書無敵隔音神器，降噪深邃安靜。耳罩皮質保養良好無脫皮，附原廠便攜收納盒與飛機轉接頭。",
            "3C電子",
            "9成新",
            4600,
            9900,
            json.dumps(["sell", "exchange"]),
            "想換 iPad 9 或可補差價交易",
            1,
            "國立臺灣師範大學",
            "台北市",
            "師大誠大樓大廳",
            "active",
            json.dumps(["https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=600&q=80"]),
            310
        ),
        # Product 13: BenQ ScreenBar
        (
            user_ids["alice"],
            "BenQ WiT ScreenBar 螢幕智能掛燈 (自動調光 / 護眼無反光)",
            "宿舍狹小桌面必備，掛在螢幕上完全不佔桌面空間，專利非對稱光學設計，照亮桌面不照螢幕。",
            "3C電子",
            "9成新",
            1850,
            2990,
            json.dumps(["sell"]),
            "",
            1,
            "國立臺灣大學",
            "台北市",
            "台大長興街 BOT 宿舍前",
            "active",
            json.dumps(["https://images.unsplash.com/photo-1517055729445-fa7d27394b48?auto=format&fit=crop&w=600&q=80"]),
            142
        ),
        # Product 14: Dell Monitor
        (
            user_ids["evan"],
            "Dell 24吋 IPS 旋轉護眼外接螢幕 (高低升降 / 附 HDMI 與電源線)",
            "寫程式必備垂直旋轉螢幕，色彩精準，IPS 廣視角無色偏，防眩光霧面螢幕，外觀九成新。",
            "3C電子",
            "9成新",
            2100,
            4990,
            json.dumps(["sell"]),
            "",
            1,
            "國立清華大學",
            "新竹市",
            "清大旺宏館大廳",
            "active",
            json.dumps(["https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?auto=format&fit=crop&w=600&q=80"]),
            220
        ),
        # Product 15: Tatung Rice Cooker
        (
            user_ids["diana"],
            "大同 6人份全不鏽鋼經典電鍋 (經典紅 / 宿舍料理必備神物)",
            "全機身與內鍋皆為 304 不鏽鋼，煮飯、燉湯、熱便當一鍋搞定，加熱元件正常附原廠量杯與飯匙。",
            "生活用品",
            "8成新",
            1200,
            2880,
            json.dumps(["sell"]),
            "",
            1,
            "國立成功大學",
            "台南市",
            "成大勝六舍門口",
            "active",
            json.dumps(["https://images.unsplash.com/photo-1556911220-e15b29be8c8f?auto=format&fit=crop&w=600&q=80"]),
            185
        ),
        # Product 16: MUJI Fan
        (
            user_ids["fiona"],
            "無印良品 MUJI 空氣循環風扇 (超低噪音 / 節能低功耗 / 宿舍對流)",
            "大風量極度安靜，夏天冷氣房必備對流循環扇，扇葉無積塵已深度清潔，風速三段可調。",
            "生活用品",
            "9成新",
            750,
            1590,
            json.dumps(["sell", "exchange"]),
            "可換多功能陶瓷電煮鍋",
            1,
            "國立政治大學",
            "台北市",
            "政大安九福利社前",
            "active",
            json.dumps(["https://images.unsplash.com/photo-1585338107529-13afc5f02586?auto=format&fit=crop&w=600&q=80"]),
            104
        ),
        # Product 17: IKEA Trolley
        (
            user_ids["alice"],
            "IKEA RÅSKOG 三層附輪多功能收納推車 (純白款 / 附抽屜隔板)",
            "宿舍床邊與書桌旁超好用推車，輪子滑順無卡頓，三層置物大容量，放保養品、文具、零食超整齊。",
            "宿舍家具",
            "9成新",
            450,
            899,
            json.dumps(["sell"]),
            "",
            1,
            "國立臺灣大學",
            "台北市",
            "水源 BOT 男宿大廳",
            "active",
            json.dumps(["https://images.unsplash.com/photo-1586023492125-27b2c045efd7?auto=format&fit=crop&w=600&q=80"]),
            135
        ),
        # Product 18: Folding Desk
        (
            user_ids["bob"],
            "實木折疊和室多功能矮桌 (免組裝 / 宿舍租屋床邊省空間)",
            "床邊讀書追劇好幫手，桌腳摺疊收納僅厚 5 公分，木紋質感佳，四邊圓角防磕碰，廉讓學弟妹。",
            "宿舍家具",
            "9成新",
            360,
            790,
            json.dumps(["sell", "gift"]),
            "若家庭清寒新生可免費贈送！",
            1,
            "國立臺灣師範大學",
            "台北市",
            "師大學一舍廣場",
            "active",
            json.dumps(["https://images.unsplash.com/photo-1518455027359-f3f8164ba6bd?auto=format&fit=crop&w=600&q=80"]),
            88
        ),
        # Product 19: Memory Foam Mattress
        (
            user_ids["diana"],
            "加厚慢回彈記憶床墊 (單人加大 90x188cm / 附透氣可拆洗布套)",
            "成大外宿租屋使用一年，支撐性極佳不塌陷，布套已高溫熱水清洗烘乾，附防塵束口收納袋。",
            "宿舍家具",
            "8成新",
            850,
            2480,
            json.dumps(["sell"]),
            "",
            1,
            "國立成功大學",
            "台南市",
            "成大光復校區門口",
            "active",
            json.dumps(["https://images.unsplash.com/photo-1631049307264-da0ec9d70304?auto=format&fit=crop&w=600&q=80"]),
            176
        ),
        # Product 20: Dorm Bed Curtain
        (
            user_ids["fiona"],
            "宿舍全遮光防蚊透氣床簾 (四面全罩式 / 隱私必備 / 雙軌滑輪)",
            "政大莊舍高架床使用，全遮光布料隔絕走道燈光，夏天防蚊透氣，安裝簡易拆卸方便。",
            "宿舍家具",
            "9成新",
            290,
            680,
            json.dumps(["sell", "exchange"]),
            "可換衣架或文具組",
            1,
            "國立政治大學",
            "台北市",
            "政大山下麥當勞門口",
            "active",
            json.dumps(["https://images.unsplash.com/photo-1513694203232-719a280e022f?auto=format&fit=crop&w=600&q=80"]),
            95
        ),
        # Product 21: Nike Running Shoes
        (
            user_ids["evan"],
            "Nike Air Zoom Pegasus 專業慢跑鞋 (US 9.5 / 全新未落地 / 經典黑白)",
            "尺寸買錯未落地穿過，氣墊飽滿彈性極佳，透氣網布鞋面，含原裝鞋盒與吊牌。",
            "運動服飾",
            "9成新",
            1350,
            3500,
            json.dumps(["sell"]),
            "",
            1,
            "國立清華大學",
            "新竹市",
            "清大南大校區門口",
            "active",
            json.dumps(["https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=600&q=80"]),
            140
        ),
        # Product 22: Badminton Racket
        (
            user_ids["bob"],
            "Yonex 超輕全碳纖維羽毛球拍組 (含拍袋 / 已穿 BG65 24磅線)",
            "體育課與校內盃比賽專用，拍框無敲傷掉漆，手感輕盈揮拍速度快，加送兩顆全新練習羽球。",
            "運動服飾",
            "9成新",
            680,
            1680,
            json.dumps(["sell", "exchange"]),
            "想換桌球拍組",
            1,
            "國立臺灣師範大學",
            "台北市",
            "師大體育館前",
            "active",
            json.dumps(["https://images.unsplash.com/photo-1626224583764-f87db24ac4ea?auto=format&fit=crop&w=600&q=80"]),
            110
        ),
        # Product 23: Yoga Mat
        (
            user_ids["alice"],
            "Lululemon 5mm 雙面防滑加厚瑜珈墊 (附原廠便攜背帶 / 櫻花粉)",
            "天然橡膠材質抓地力絕佳，流汗不打滑，緩震保護手腕關節，已使用酒精擦拭消毒。",
            "運動服飾",
            "9成新",
            980,
            2480,
            json.dumps(["sell"]),
            "",
            1,
            "國立臺灣大學",
            "台北市",
            "台大綜合體育館 (新體)",
            "active",
            json.dumps(["https://images.unsplash.com/photo-1601925260368-ae2f83cf8b7f?auto=format&fit=crop&w=600&q=80"]),
            84
        ),
        # Product 24: Free Drawer Box
        (
            user_ids["charlie"],
            "大四畢業出清四層透明收納抽屜盒 (完全免費自取 / 助攻新生)",
            "大四畢業生出清宿舍，四層抽屜滑順無破損，裝文具、化妝品或充電線超好用，完全免費贈送！",
            "生活用品",
            "8成新",
            0,
            490,
            json.dumps(["gift"]),
            "免費贈送給需要的新生學弟妹",
            0,
            "國立陽明交通大學",
            "新竹市",
            "交大十三舍前空地",
            "active",
            json.dumps(["https://images.unsplash.com/photo-1595428774223-ef52624120d2?auto=format&fit=crop&w=600&q=80"]),
            195
        ),
        # Product 25: Free Stationery
        (
            user_ids["diana"],
            "全新文具盲盒大禮包 (含橫線筆記本、斑馬雙頭螢光筆、立可帶五入)",
            "之前團購買太多用不完，包含兩本全新厚筆記本、日本螢光筆組及全新立可帶替芯，免費送給認真讀書的同學。",
            "生活用品",
            "幾乎全新",
            0,
            380,
            json.dumps(["gift"]),
            "純免費愛心贈送，期中考加油！",
            0,
            "國立成功大學",
            "台南市",
            "成大總圖書館門口",
            "active",
            json.dumps(["https://images.unsplash.com/photo-1583485088034-697b5bc54ccd?auto=format&fit=crop&w=600&q=80"]),
            165
        ),
        # Product 26: Free Exam Notes
        (
            user_ids["alice"],
            "研究所考研筆記與資工歷屆考古題解析手寫本 (免費贈送學弟妹)",
            "順利正取台大資工所，整理出的計算機組織、資料結構與演算法重點筆記手寫掃描裝訂本，傳承給有志考研的同學！",
            "課本教材",
            "9成新",
            0,
            1200,
            json.dumps(["gift"]),
            "純心意傳承，希望學弟妹金榜題名",
            0,
            "國立臺灣大學",
            "台北市",
            "德田館 (資工系館) 大廳",
            "active",
            json.dumps(["https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?auto=format&fit=crop&w=600&q=80"]),
            420
        ),
        # Product 27: Strang Linear Algebra
        (
            user_ids["evan"],
            "Strang 線性代數導論 Introduction to Linear Algebra (第5版 原文書)",
            "MIT 公開課指定教材，線性代數聖經本，圖解矩陣空間深刻易懂，頁面無塗鴉，書皮完整。",
            "課本教材",
            "9成新",
            480,
            1450,
            json.dumps(["sell", "exchange"]),
            "想換離散數學原文書",
            1,
            "國立清華大學",
            "新竹市",
            "清大資電館大廳",
            "active",
            json.dumps(["https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?auto=format&fit=crop&w=600&q=80"]),
            130
        ),
        # Product 28: Wade Organic Chemistry
        (
            user_ids["diana"],
            "Wade 有機化學 Organic Chemistry (第9版 上下冊精裝合售)",
            "化學系、化工系必修經典，反應機構機轉圖解詳盡，包含期中立體化學重點劃記，附解答手冊。",
            "課本教材",
            "9成新",
            680,
            2200,
            json.dumps(["sell"]),
            "",
            1,
            "國立成功大學",
            "台南市",
            "成大理學教學大樓門口",
            "active",
            json.dumps(["https://images.unsplash.com/photo-1532012164546-f432f2e3ddb5?auto=format&fit=crop&w=600&q=80"]),
            118
        ),
        # Product 29: Psychology Textbook
        (
            user_ids["bob"],
            "Atkinson & Hilgard 心理學導論 (中文第4版 / 附期末重點講義整理)",
            "通識課熱門教材，彩色列印圖文並茂，涵蓋認知、發展與社會心理學，考前必備神書。",
            "課本教材",
            "9成新",
            390,
            950,
            json.dumps(["sell", "exchange"]),
            "可換教育心理學教材",
            1,
            "國立臺灣師範大學",
            "台北市",
            "師大教育學院大樓前",
            "active",
            json.dumps(["https://images.unsplash.com/photo-1497633762265-9d179a990aa6?auto=format&fit=crop&w=600&q=80"]),
            78
        ),
        # Product 30: Business Statistics
        (
            user_ids["fiona"],
            "統計學：商業與經濟的應用 Statistics for Business (第13版 原文書)",
            "商學院統計學指定教材，包含迴歸分析、假說檢定章節完整筆記，光碟未拆封。",
            "課本教材",
            "9成新",
            450,
            1350,
            json.dumps(["sell", "exchange"]),
            "想換投資學原文書",
            1,
            "國立政治大學",
            "台北市",
            "政大逸仙樓大廳",
            "active",
            json.dumps(["https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?auto=format&fit=crop&w=600&q=80"]),
            96
        ),
        # Product 31: Constitution Notes
        (
            user_ids["fiona"],
            "憲法與政府體制爭點筆記 (司律國考與大二必修適用 / 體系表齊全)",
            "公法名師體系綱要整理，大法官釋字與憲判字完整整理，適合法學院修課與準備國考者。",
            "課本教材",
            "幾乎全新",
            280,
            650,
            json.dumps(["sell"]),
            "",
            1,
            "國立政治大學",
            "台北市",
            "政大法學院館門口",
            "active",
            json.dumps(["https://images.unsplash.com/photo-1589829545856-d10d557cf95f?auto=format&fit=crop&w=600&q=80"]),
            65
        ),
        # Product 32: Keychron K2
        (
            user_ids["alice"],
            "Keychron K2 RGB 無線機械鍵盤 (茶軸熱插拔 / Mac與Win專用鍵帽皆齊全)",
            "75% 緊湊配置省桌面空間，茶軸微段落感打字安靜不擾室友，藍牙與 Type-C 雙模切換自如。",
            "3C電子",
            "9成新",
            1580,
            2890,
            json.dumps(["sell", "exchange"]),
            "想換 Logitech 靜音滑鼠",
            1,
            "國立臺灣大學",
            "台北市",
            "台大小福廣場",
            "active",
            json.dumps(["https://images.unsplash.com/photo-1587829741301-dc798b83add3?auto=format&fit=crop&w=600&q=80"]),
            210
        ),
        # Product 33: Logitech G Pro Mouse
        (
            user_ids["charlie"],
            "Logitech G Pro X Superlight 超輕量無線電競滑鼠 (黑色 / 僅63克)",
            "電競社訓練專用，HERO 25K 感應器定位極準，電池續航力長達 70 小時，微動開關點擊清脆無連點。",
            "3C電子",
            "9成新",
            2400,
            4490,
            json.dumps(["sell"]),
            "",
            1,
            "國立陽明交通大學",
            "新竹市",
            "交大活動中心大廳",
            "active",
            json.dumps(["https://images.unsplash.com/photo-1615663245857-ac93bb7c39e7?auto=format&fit=crop&w=600&q=80"]),
            185
        ),
        # Product 34: WD External HDD
        (
            user_ids["evan"],
            "WD My Passport 2TB USB 3.0 隨身防震外接硬碟 (黑 / 附防震保護包)",
            "備份報告、期末專題與照片必備，讀寫速度穩定無壞軌，原廠 USB 3.0 傳輸線齊全。",
            "3C電子",
            "9成新",
            1150,
            2390,
            json.dumps(["sell"]),
            "",
            1,
            "國立清華大學",
            "新竹市",
            "清大工程一館門口",
            "active",
            json.dumps(["https://images.unsplash.com/photo-1597872200969-2b65d56bd16b?auto=format&fit=crop&w=600&q=80"]),
            98
        ),
        # Product 35: Anker GaN Charger
        (
            user_ids["bob"],
            "Anker 65W GaN 氮化鎵三孔迷你快速充電器 (2C1A / 可同時充筆電與手機)",
            "體積小巧摺疊插腳，支援 PD 3.0 與 QC 快充，出門上課只要帶一顆，不必帶笨重筆電充電器。",
            "3C電子",
            "9成新",
            690,
            1490,
            json.dumps(["sell", "exchange"]),
            "可換 10000mAh 行動電源",
            1,
            "國立臺灣師範大學",
            "台北市",
            "師大和平校區正門",
            "active",
            json.dumps(["https://images.unsplash.com/photo-1583863788434-e58a36330cf0?auto=format&fit=crop&w=600&q=80"]),
            145
        ),
        # Product 36: Wacom Tablet
        (
            user_ids["diana"],
            "Wacom One 13.3吋 專業液晶感壓繪圖螢幕 (附感壓筆與替換筆芯組)",
            "設計系專題繪圖神機，直覺在螢幕上作畫，免充電感壓筆，支援 Mac/Windows，外觀無刮痕良好。",
            "3C電子",
            "9成新",
            5500,
            12500,
            json.dumps(["sell"]),
            "",
            1,
            "國立成功大學",
            "台南市",
            "成大建築系館一樓大廳",
            "active",
            json.dumps(["https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?auto=format&fit=crop&w=600&q=80"]),
            275
        ),
        # Product 37: CASIO Calculator
        (
            user_ids["charlie"],
            "CASIO fx-991ES PLUS 二代太陽能雙電源工程型計算機 (考研與國考考選部合格核准款)",
            "理工科微積分、工數、電路學必備計算機，自然教科書顯示格式，太陽能與電池雙重電力，無摔落功能完整。",
            "3C電子",
            "9成新",
            380,
            750,
            json.dumps(["sell", "exchange"]),
            "可換多功能尺規組",
            1,
            "國立陽明交通大學",
            "新竹市",
            "交大工程四館中庭",
            "active",
            json.dumps(["https://images.unsplash.com/photo-1587145820266-a5951ee6f620?auto=format&fit=crop&w=600&q=80"]),
            160
        ),
        # Product 38: Laptop Stand
        (
            user_ids["alice"],
            "全鋁合金多角度可折疊筆記型電腦散熱支架 (穩固防晃 / 六檔高度調節)",
            "拯救頸椎宿舍神器，鏤空底座輔助通風散熱，附收納絨布袋，適用 11-17 吋各廠牌筆電。",
            "3C電子",
            "9成新",
            290,
            590,
            json.dumps(["sell", "gift"]),
            "買其他 3C 物品可免費隨機附贈！",
            1,
            "國立臺灣大學",
            "台北市",
            "台大總圖地下室自習室前",
            "active",
            json.dumps(["https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?auto=format&fit=crop&w=600&q=80"]),
            110
        ),
        # Product 39: Tiger Thermos
        (
            user_ids["fiona"],
            "虎牌 TIGER 不鏽鋼超輕量彈蓋保溫隨行杯 (500ml / 珍珠白限定款)",
            "單手一鍵彈蓋開鎖，上課開會喝水超優雅，保溫保冷長達 12 小時，杯口無污垢異味，清潔乾淨。",
            "生活用品",
            "9成新",
            420,
            1190,
            json.dumps(["sell"]),
            "",
            1,
            "國立政治大學",
            "台北市",
            "政大麥側門口",
            "active",
            json.dumps(["https://images.unsplash.com/photo-1517256064527-09c73fc73e38?auto=format&fit=crop&w=600&q=80"]),
            75
        ),
        # Product 40: Sampo Microwave
        (
            user_ids["evan"],
            "聲寶 SAMPO 20L 微電腦微波爐 (機械旋鈕五段火力 / 宿舍宵夜神器)",
            "解凍、熱便當、煮泡麵超快，轉盤運轉順暢，定時鐘聲清脆，外觀與內部皆已使用小蘇打深層清潔。",
            "生活用品",
            "8成新",
            950,
            2490,
            json.dumps(["sell"]),
            "",
            1,
            "國立清華大學",
            "新竹市",
            "清大清齋交誼廳",
            "active",
            json.dumps(["https://images.unsplash.com/photo-1585659722983-3a675dabf23d?auto=format&fit=crop&w=600&q=80"]),
            190
        ),
        # Product 41: Philips Sonicare
        (
            user_ids["bob"],
            "飛利浦 Sonicare 智能音波震動電動牙刷 (含2入原廠全新未拆刷頭 / 附充電底座)",
            "音波震動每分鐘 31000 次，深層潔淨牙齦，機身防水功能正常，電池續航力充一次可用兩週。",
            "生活用品",
            "9成新",
            780,
            1980,
            json.dumps(["sell"]),
            "",
            1,
            "國立臺灣師範大學",
            "台北市",
            "師大夜市水準書局門口",
            "active",
            json.dumps(["https://images.unsplash.com/photo-1559591937-e62fb330bc1f?auto=format&fit=crop&w=600&q=80"]),
            68
        ),
        # Product 42: Brita Water Pitcher
        (
            user_ids["alice"],
            "Brita 德國原裝濾水壺 3.5L (含3入全新未拆 Maxtra+ 全效濾芯)",
            "宿舍飲水機安心過濾必備，免開蓋注水設計，電子式濾芯更換顯示器正常，壺身乾淨無水垢。",
            "生活用品",
            "9成新",
            650,
            1450,
            json.dumps(["sell", "exchange"]),
            "可換不鏽鋼快煮壺",
            1,
            "國立臺灣大學",
            "台北市",
            "台大辛亥路後門校門",
            "active",
            json.dumps(["https://images.unsplash.com/photo-1548839140-29a749e1bc4e?auto=format&fit=crop&w=600&q=80"]),
            130
        ),
        # Product 43: Electric Cooker
        (
            user_ids["diana"],
            "多功能美型雙層陶瓷電煮鍋 (附不鏽鋼蒸籠 / 宿舍無油煙料理首選)",
            "陶瓷不沾內膽清洗超容易，雙檔火力調節，煮火鍋、下水餃、蒸包子一機搞定，防乾燒斷電安全保護。",
            "生活用品",
            "9成新",
            380,
            890,
            json.dumps(["sell", "exchange"]),
            "想換小型吹風機",
            1,
            "國立成功大學",
            "台南市",
            "成大育樂街口 7-11",
            "active",
            json.dumps(["https://images.unsplash.com/photo-1556911220-e15b29be8c8f?auto=format&fit=crop&w=600&q=80"]),
            112
        ),
        # Product 44: Dehumidifier Boxes
        (
            user_ids["charlie"],
            "克潮靈 宿舍除濕吸濕盒組 (超值10入量販組 / 全新未拆封包裝)",
            "新竹雨季與潮濕氣候必備，衣櫃與書桌防霉必用，多買了一整箱用不完，便宜出清給同學。",
            "生活用品",
            "幾乎全新",
            190,
            450,
            json.dumps(["sell", "gift"]),
            "購買其他物品可免費贈送兩盒！",
            1,
            "國立陽明交通大學",
            "新竹市",
            "交大竹軒女舍大門",
            "active",
            json.dumps(["https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?auto=format&fit=crop&w=600&q=80"]),
            82
        ),
        # Product 45: Full Length Mirror
        (
            user_ids["fiona"],
            "簡約立式旋轉全身穿衣鏡 (後附三層實木置物衣帽掛架 / 佔地小)",
            "外宿租屋穿搭必備，高清晰度鏡面無變形，底部可 360 度旋轉，背後能掛包包和大衣，穩固不晃。",
            "宿舍家具",
            "9成新",
            550,
            1280,
            json.dumps(["sell"]),
            "",
            1,
            "國立政治大學",
            "台北市",
            "政大山下一舍管理室",
            "active",
            json.dumps(["https://images.unsplash.com/photo-1618221195710-dd6b41faaea6?auto=format&fit=crop&w=600&q=80"]),
            145
        ),
        # Product 46: Coat Rack
        (
            user_ids["bob"],
            "實木多功能宿舍門後衣帽架 (無痕掛勾免釘牆壁 / 8掛勾款)",
            "掛在宿舍房門後完全免打孔，掛外套、帽子、書包超順手，實木掛勾質感圓潤不刮傷衣物。",
            "宿舍家具",
            "9成新",
            180,
            390,
            json.dumps(["sell", "gift"]),
            "可免費贈送給新生",
            1,
            "國立臺灣師範大學",
            "台北市",
            "師大本部文學院穿堂",
            "active",
            json.dumps(["https://images.unsplash.com/photo-1586023492125-27b2c045efd7?auto=format&fit=crop&w=600&q=80"]),
            58
        ),
        # Product 47: Dorm Mini Fridge
        (
            user_ids["charlie"],
            "雙層超靜音小型宿舍冰箱 (45L 一級能效 / 環保省電 / 附冷凍製冰盒)",
            "放飲料、冰淇淋、優格超讚，運轉分貝極低睡眠不干擾，一級能效電費極省，已完全除霜消毒乾淨。",
            "宿舍家具",
            "8成新",
            1800,
            4990,
            json.dumps(["sell"]),
            "",
            1,
            "國立陽明交通大學",
            "新竹市",
            "交大七舍門口",
            "active",
            json.dumps(["https://images.unsplash.com/photo-1571175443880-49e1d25b2bc5?auto=format&fit=crop&w=600&q=80"]),
            330
        ),
        # Product 48: NTU Hoodie
        (
            user_ids["alice"],
            "台大校隊限定版連帽運動長袖衛衣 (經典麻花灰 L號 / 加厚刷毛保暖款)",
            "台大校園紀念正品，胸前精緻立體刺繡，內裡刷毛柔軟親膚，冬天在校園騎腳踏車超防風保暖。",
            "運動服飾",
            "9成新",
            580,
            1350,
            json.dumps(["sell", "exchange"]),
            "想換 XL 號或其他大學校隊帽T",
            1,
            "國立臺灣大學",
            "台北市",
            "台大鹿鳴廣場",
            "active",
            json.dumps(["https://images.unsplash.com/photo-1556905055-8f358a7a47b2?auto=format&fit=crop&w=600&q=80"]),
            195
        ),
        # Product 49: Osprey Backpack
        (
            user_ids["evan"],
            "Osprey Daylite 20L 輕量多功能戶外登山後背包 (軍綠色 / 附防雨罩)",
            "通風透氣背板流汗不悶熱，人體工學肩帶減壓舒適，內有筆電隔層，日常上課或週末健行郊遊皆宜。",
            "運動服飾",
            "9成新",
            1200,
            2680,
            json.dumps(["sell", "exchange"]),
            "可換 North Face 斜背包",
            1,
            "國立清華大學",
            "新竹市",
            "清大成功湖畔步道口",
            "active",
            json.dumps(["https://images.unsplash.com/photo-1553062407-98eeb64c6a62?auto=format&fit=crop&w=600&q=80"]),
            160
        ),
        # Product 50: Grip Strength Trainer
        (
            user_ids["bob"],
            "專業可調節計數握力器 (10-60kg 無級阻力調節 / 附手指力量伸展圈)",
            "讀書疲憊或坐著聽講時鍛鍊手腕握力，機械計數器自動記錄次數，防滑握把舒適不磨手，維持健康體態。",
            "運動服飾",
            "幾乎全新",
            150,
            350,
            json.dumps(["sell", "gift"]),
            "新生面交買書可直接贈送！",
            1,
            "國立臺灣師範大學",
            "台北市",
            "師大圖書館校區日光大道",
            "active",
            json.dumps(["https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=600&q=80"]),
            90
        ),
    ]

    cursor.executemany("""
    INSERT INTO products (user_id, title, description, category, condition, price, original_price, trade_types, exchange_wish, allow_price_diff, school, city, meetup_location, status, images, views)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, products_data)

    # 3. Seed Favorites
    cursor.execute("INSERT INTO favorites (user_id, product_id) VALUES (3, 1), (4, 3), (2, 5), (5, 9), (6, 12), (7, 15)")

    # 4. Seed QA Messages
    cursor.execute("""
    INSERT INTO qa_messages (product_id, user_id, question, answer, answered_at)
    VALUES 
    (1, 3, '學姊好！請問這本是上學期用的嗎？隨書光碟還在嗎？', '在的，隨書附的光碟以及期中考重點整理 PDF 會一併提供！', CURRENT_TIMESTAMP),
    (3, 4, '請問可以接受分期面交嗎？還是只能一次付清？', '建議面交當面網銀轉帳或現金點清喔！', CURRENT_TIMESTAMP),
    (9, 2, '請問這本普物第10版跟第9版章節差很多嗎？', '習題題號有重新編排，如果是清大或台大修課建議用第10版對應作業喔！', CURRENT_TIMESTAMP)
    """)

    # 5. Seed Chat & Negotiation (Between Bob buyer and Alice seller for Calculus book)
    cursor.execute("""
    INSERT INTO chats (product_id, buyer_id, seller_id)
    VALUES (1, 3, 2)
    """)
    chat_id = cursor.lastrowid

    cursor.execute("""
    INSERT INTO chat_messages (chat_id, sender_id, message_type, content, offer_price, meetup_details)
    VALUES 
    (?, 3, 'text', '學姊好！如果今天中午在台大總圖面交，300 元願意割愛嗎？', NULL, ''),
    (?, 3, 'offer', '買家提出出價：NT$ 300', 300, ''),
    (?, 2, 'offer_accepted', '賣家已接受出價 NT$ 300！已鎖定商品為預約中。', 300, ''),
    (?, 2, 'meetup_contract', '已確認面交約定：今天 12:30 在台大總圖書館大門口見！', 300, '{"location": "台大總圖書館大門口", "time": "今天 12:30"}')
    """, (chat_id, chat_id, chat_id, chat_id))

    # 6. Seed Completed Transaction & Reviews
    cursor.execute("""
    INSERT INTO transactions (product_id, buyer_id, seller_id, trade_type, final_price, meetup_location, buyer_rating, buyer_review, seller_rating, seller_review, status)
    VALUES (
        1, 3, 2, 'buy', 300, '總圖書館正門門口', 5, '學姊人超級好，微積分書況很棒，還親切傳授考試技巧！', 5, '買家準時守信用，交易非常順利！', 'completed'
    )
    """)

    # 7. Seed Notifications
    cursor.execute("""
    INSERT INTO notifications (user_id, title, content, type, link)
    VALUES 
    (2, '買家提出了出價！', '鮑伯 對您的「微積分第 8 版」提出了 NT$ 300 的出價申請。', 'offer', '/chat/1'),
    (3, '賣家已接受您的出價', '愛麗絲 已同意以 NT$ 300 與您面交「微積分第 8 版」。', 'trade_status', '/chat/1'),
    (4, '願望清單降價提醒', '您收藏的「iPad Air 4」目前已降價至 NT$ 8,800，符合您的預算！', 'price_drop', '/product/3')
    """)

    # 8. Seed Reports
    cursor.execute("""
    INSERT INTO reports (reporter_id, target_type, target_id, reason, status, admin_notes)
    VALUES (
        3, 'product', 8, '商品疑似有電線接觸不良問題，申請管理員審查', 'pending', ''
    )
    """)

    conn.commit()
    conn.close()
    print("Seed data successfully loaded with 50 products.")

if __name__ == "__main__":
    seed_database()
