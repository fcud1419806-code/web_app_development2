# 路由與頁面設計文件 - 讀書筆記系統

本文件根據產品需求文件 (PRD) 與資料庫設計 (DB_DESIGN) 規劃了讀書筆記系統的所有 HTTP 路由與 Jinja2 模板對應關係。

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| 首頁 / 筆記列表 | GET | `/` | `index.html` | 顯示所有最新筆記 |
| 搜尋筆記 | GET | `/search` | `index.html` | 根據關鍵字顯示搜尋結果（重複利用首頁模板） |
| 新增筆記頁面 | GET | `/notes/create` | `create.html` | 顯示新增筆記的表單 |
| 建立筆記 | POST | `/notes/create` | — | 接收表單資料，存入 DB 後重導向至首頁 |
| 筆記詳情 | GET | `/notes/<id>` | `detail.html` | 顯示特定筆記的完整內容與評分 |
| 編輯筆記頁面 | GET | `/notes/<id>/edit` | `edit.html` | 顯示編輯特定筆記的表單 |
| 更新筆記 | POST | `/notes/<id>/edit` | — | 接收表單資料，更新 DB 後重導向至詳情頁 |
| 刪除筆記 | POST | `/notes/<id>/delete` | — | 從 DB 刪除筆記，完成後重導向至首頁 |

---

## 2. 路由詳細說明

### 2.1 首頁 / 筆記列表 (`GET /`)
- **輸入**：無
- **處理邏輯**：呼叫 `NoteModel.get_all_notes()` 取得所有筆記。
- **輸出**：渲染 `index.html`，傳遞 `notes` 變數。

### 2.2 搜尋筆記 (`GET /search`)
- **輸入**：URL 參數 `?q=關鍵字`
- **處理邏輯**：取得參數 `q`，若有值則呼叫 `NoteModel.search_notes(keyword)`，否則呼叫 `get_all_notes()`。
- **輸出**：渲染 `index.html`，傳遞 `notes` 與 `search_query` 變數。

### 2.3 新增筆記頁面 (`GET /notes/create`)
- **輸入**：無
- **處理邏輯**：無特殊邏輯。
- **輸出**：渲染 `create.html`。

### 2.4 建立筆記 (`POST /notes/create`)
- **輸入**：表單欄位 `title` (必填), `review`, `rating`
- **處理邏輯**：
  - 驗證 `title` 是否存在。若無，可能返回錯誤訊息。
  - 呼叫 `NoteModel.create_note(title, review, rating)`。
- **輸出**：重導向至 `/`。
- **錯誤處理**：如果必填欄位缺失，重新渲染 `create.html` 並顯示錯誤訊息。

### 2.5 筆記詳情 (`GET /notes/<id>`)
- **輸入**：URL 路徑參數 `id`
- **處理邏輯**：呼叫 `NoteModel.get_note_by_id(id)`。
- **輸出**：若找到，渲染 `detail.html`，傳遞 `note` 變數。
- **錯誤處理**：若找不到該筆記，返回 404 畫面或重導向至首頁並帶錯誤訊息。

### 2.6 編輯筆記頁面 (`GET /notes/<id>/edit`)
- **輸入**：URL 路徑參數 `id`
- **處理邏輯**：呼叫 `NoteModel.get_note_by_id(id)` 取出原始資料。
- **輸出**：渲染 `edit.html`，傳遞 `note` 變數以預填表單。

### 2.7 更新筆記 (`POST /notes/<id>/edit`)
- **輸入**：URL 路徑參數 `id`，表單欄位 `title`, `review`, `rating`
- **處理邏輯**：呼叫 `NoteModel.update_note(id, title, review, rating)`。
- **輸出**：重導向至 `/notes/<id>`。

### 2.8 刪除筆記 (`POST /notes/<id>/delete`)
- **輸入**：URL 路徑參數 `id`
- **處理邏輯**：呼叫 `NoteModel.delete_note(id)`。
- **輸出**：重導向至 `/`。

---

## 3. Jinja2 模板清單

所有的模板檔案將放置於 `app/templates/` 目錄下。

| 檔案名稱 | 繼承對象 | 用途 |
| :--- | :--- | :--- |
| `base.html` | (無) | 全站共用佈局，包含 HTML 骨架、Navbar、Footer 與 CSS 引入 |
| `index.html` | `base.html` | 首頁與搜尋結果頁，顯示筆記列表清單 |
| `create.html` | `base.html` | 新增筆記的表單頁面 |
| `detail.html` | `base.html` | 單筆筆記的完整內容展示頁，包含編輯與刪除按鈕 |
| `edit.html` | `base.html` | 編輯筆記的表單頁面（內容與 create.html 相似但會預填資料） |
