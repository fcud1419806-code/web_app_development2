from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.note_model import NoteModel

# 建立名為 note_bp 的 Blueprint
note_bp = Blueprint('note', __name__)

@note_bp.route('/')
def index():
    """
    處理首頁與筆記列表：
    - 呼叫 NoteModel.get_all_notes()
    - 渲染 index.html
    """
    pass

@note_bp.route('/search')
def search():
    """
    處理搜尋請求：
    - 取得 GET 參數 'q'
    - 呼叫 NoteModel.search_notes(keyword)
    - 渲染 index.html 並帶入搜尋結果
    """
    pass

@note_bp.route('/notes/create', methods=['GET', 'POST'])
def create_note():
    """
    處理新增筆記：
    - GET: 渲染 create.html
    - POST: 接收表單資料，呼叫 NoteModel.create_note，並重導向至首頁
    """
    pass

@note_bp.route('/notes/<int:note_id>')
def view_note(note_id):
    """
    處理檢視單筆筆記細節：
    - 根據 note_id 呼叫 NoteModel.get_note_by_id
    - 若找到則渲染 detail.html，否則回傳 404
    """
    pass

@note_bp.route('/notes/<int:note_id>/edit', methods=['GET', 'POST'])
def edit_note(note_id):
    """
    處理編輯筆記：
    - GET: 根據 note_id 取得筆記，並渲染 edit.html 預填資料
    - POST: 接收表單資料，呼叫 NoteModel.update_note，並重導向至詳情頁
    """
    pass

@note_bp.route('/notes/<int:note_id>/delete', methods=['POST'])
def delete_note(note_id):
    """
    處理刪除筆記：
    - 接收 POST 請求，呼叫 NoteModel.delete_note
    - 刪除後重導向至首頁
    """
    pass
