import sqlite3
import os
import shutil
import hashlib
import json
import seed_data

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_db_path():
    # 當運行於 Vercel Serverless 環境時，使用唯一具備寫入權限的 /tmp/ 目錄
    if os.environ.get("VERCEL") or os.environ.get("AWS_LAMBDA_FUNCTION_NAME"):
        tmp_db = "/tmp/campus_trade.db"
        if not os.path.exists(tmp_db) or os.path.getsize(tmp_db) == 0:
            # 優先嘗試從各處複製已存在的 campus_trade.db (92KB)
            possible_srcs = [
                os.path.join(BASE_DIR, "campus_trade.db"),
                os.path.join(os.path.dirname(BASE_DIR), "campus_trade.db"),
                os.path.join(BASE_DIR, "api", "campus_trade.db"),
                os.path.join(os.getcwd(), "campus_trade.db")
            ]
            for src in possible_srcs:
                if os.path.exists(src) and os.path.getsize(src) > 0:
                    try:
                        shutil.copy2(src, tmp_db)
                        break
                    except Exception as e:
                        print(f"Copying DB exception: {e}")
        return tmp_db
    return os.path.join(BASE_DIR, "campus_trade.db")

DB_FILE = get_db_path()

def get_db():
    target_path = get_db_path()
    conn = sqlite3.connect(target_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    
    # 確保資料庫結構與基礎表格存在
    _init_db_conn(conn)
    
    # 檢查是否有商品資料，若無商品資料立即自動寫入 50 筆種子資料！
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM products")
    if cursor.fetchone()[0] == 0:
        seed_data.insert_seed_data_on_conn(conn)
        
    return conn

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def _init_db_conn(conn):
    cursor = conn.cursor()


    # 1. Users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        nickname TEXT NOT NULL,
        school TEXT NOT NULL,
        department TEXT DEFAULT '',
        avatar_url TEXT DEFAULT '',
        is_edu_verified INTEGER DEFAULT 0,
        is_admin INTEGER DEFAULT 0,
        rating REAL DEFAULT 5.0,
        rating_count INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # 2. Products table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        category TEXT NOT NULL,
        condition TEXT NOT NULL,
        price INTEGER NOT NULL DEFAULT 0,
        original_price INTEGER DEFAULT 0,
        trade_types TEXT NOT NULL, -- JSON string e.g. ["sell", "exchange", "gift"]
        exchange_wish TEXT DEFAULT '',
        allow_price_diff INTEGER DEFAULT 1,
        school TEXT NOT NULL,
        city TEXT NOT NULL,
        meetup_location TEXT DEFAULT '',
        status TEXT NOT NULL DEFAULT 'active', -- 'active', 'reserved', 'completed', 'delisted'
        images TEXT NOT NULL, -- JSON array of image URLs
        views INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # 3. Favorites table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS favorites (
        user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        product_id INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (user_id, product_id)
    )
    """)

    # 4. QA Messages table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS qa_messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
        user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        question TEXT NOT NULL,
        answer TEXT DEFAULT '',
        answered_at TIMESTAMP,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # 5. Chats table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
        buyer_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        seller_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(product_id, buyer_id)
    )
    """)

    # 6. Chat Messages table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chat_messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chat_id INTEGER NOT NULL REFERENCES chats(id) ON DELETE CASCADE,
        sender_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        message_type TEXT DEFAULT 'text', -- 'text', 'offer', 'offer_accepted', 'offer_rejected', 'offer_counter', 'meetup_contract'
        content TEXT NOT NULL,
        offer_price INTEGER DEFAULT NULL,
        exchange_product_id INTEGER DEFAULT NULL,
        meetup_details TEXT DEFAULT '',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # 7. Transactions history table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
        buyer_id INTEGER NOT NULL REFERENCES users(id),
        seller_id INTEGER NOT NULL REFERENCES users(id),
        trade_type TEXT NOT NULL, -- 'buy', 'exchange', 'gift'
        final_price INTEGER DEFAULT 0,
        meetup_location TEXT DEFAULT '',
        buyer_rating INTEGER DEFAULT NULL,
        buyer_review TEXT DEFAULT '',
        seller_rating INTEGER DEFAULT NULL,
        seller_review TEXT DEFAULT '',
        status TEXT DEFAULT 'completed',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # 8. Notifications table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        type TEXT NOT NULL, -- 'price_drop', 'offer', 'qa', 'trade_status', 'system'
        link TEXT DEFAULT '',
        is_read INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # 9. Reports & Admin moderation table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        reporter_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        target_type TEXT NOT NULL, -- 'product', 'user'
        target_id INTEGER NOT NULL,
        reason TEXT NOT NULL,
        status TEXT DEFAULT 'pending', -- 'pending', 'resolved_valid', 'resolved_dismissed'
        admin_notes TEXT DEFAULT '',
        resolved_by INTEGER REFERENCES users(id),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        resolved_at TIMESTAMP
    )
    """)

    conn.commit()

def init_db():
    target_path = get_db_path()
    conn = sqlite3.connect(target_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    _init_db_conn(conn)
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database schema successfully initialized.")
