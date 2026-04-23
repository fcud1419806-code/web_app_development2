-- 讀書筆記系統 - 資料表建立語法
-- 執行方式：sqlite3 instance/database.db < database/schema.sql

-- 如果資料表已經存在則不建立
CREATE TABLE IF NOT EXISTS notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    review TEXT,
    rating INTEGER CHECK(rating >= 1 AND rating <= 5),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
