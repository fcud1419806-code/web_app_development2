import sqlite3
import os

# 資料庫檔案路徑，假設從專案根目錄執行 app.py
DB_PATH = os.path.join('instance', 'database.db')

def get_db_connection():
    """取得 SQLite 資料庫連線，並設定 row_factory 讓結果以 dict 形式呈現"""
    # 確保 instance 資料夾存在
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

class NoteModel:
    @staticmethod
    def create_note(title, review, rating):
        """新增一筆筆記"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO notes (title, review, rating) VALUES (?, ?, ?)',
            (title, review, rating)
        )
        conn.commit()
        note_id = cursor.lastrowid
        conn.close()
        return note_id

    @staticmethod
    def get_all_notes():
        """取得所有筆記（依時間新到舊排序）"""
        conn = get_db_connection()
        notes = conn.execute('SELECT * FROM notes ORDER BY created_at DESC').fetchall()
        conn.close()
        return [dict(note) for note in notes]

    @staticmethod
    def get_note_by_id(note_id):
        """根據 ID 取得單筆筆記"""
        conn = get_db_connection()
        note = conn.execute('SELECT * FROM notes WHERE id = ?', (note_id,)).fetchone()
        conn.close()
        return dict(note) if note else None

    @staticmethod
    def update_note(note_id, title, review, rating):
        """更新特定筆記"""
        conn = get_db_connection()
        conn.execute(
            'UPDATE notes SET title = ?, review = ?, rating = ? WHERE id = ?',
            (title, review, rating, note_id)
        )
        conn.commit()
        conn.close()
        return True

    @staticmethod
    def delete_note(note_id):
        """刪除特定筆記"""
        conn = get_db_connection()
        conn.execute('DELETE FROM notes WHERE id = ?', (note_id,))
        conn.commit()
        conn.close()
        return True

    @staticmethod
    def search_notes(keyword):
        """根據書名或心得進行關鍵字搜尋"""
        conn = get_db_connection()
        search_query = f"%{keyword}%"
        notes = conn.execute(
            'SELECT * FROM notes WHERE title LIKE ? OR review LIKE ? ORDER BY created_at DESC',
            (search_query, search_query)
        ).fetchall()
        conn.close()
        return [dict(note) for note in notes]
