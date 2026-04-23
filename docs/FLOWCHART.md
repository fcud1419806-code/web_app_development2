# 流程圖文件 - 讀書筆記系統

本文件根據產品需求文件 (PRD) 與系統架構文件 (ARCHITECTURE) 定義讀書筆記系統的使用者流程與系統互動流程。

## 1. 使用者流程圖 (User Flow)

此流程圖展示使用者在系統中的操作路徑，涵蓋首頁瀏覽、新增筆記、查看細節與搜尋等主要功能。

```mermaid
flowchart LR
    Start([使用者開啟網頁]) --> Home[首頁 - 筆記列表]
    Home --> Action{要執行什麼操作？}
    
    Action -->|點擊新增| CreatePage[新增筆記頁面]
    CreatePage --> FillForm[填寫書名、心得與評分]
    FillForm --> SubmitCreate([送出表單])
    SubmitCreate --> Home
    
    Action -->|點擊特定筆記| DetailPage[筆記詳細頁面]
    DetailPage --> EditAction{要編輯嗎？}
    EditAction -->|否| BackHome([返回首頁])
    BackHome --> Home
    EditAction -->|是| EditPage[編輯筆記頁面]
    EditPage --> UpdateForm[修改心得與評分]
    UpdateForm --> SubmitUpdate([儲存修改])
    SubmitUpdate --> DetailPage
    
    Action -->|輸入關鍵字搜尋| Search[執行搜尋]
    Search --> SearchResult[顯示搜尋結果列表]
    SearchResult --> Home
```

---

## 2. 系統序列圖 (Sequence Diagram)

此序列圖描述使用者執行「新增筆記」時，系統各元件之間的完整資料傳遞流程。

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Route as Flask Route (note_routes.py)
    participant Model as Model (note_model.py)
    participant DB as SQLite (database.db)
    
    User->>Browser: 填寫新增筆記表單並點擊「送出」
    Browser->>Route: POST /notes/create (包含表單資料)
    
    Route->>Model: 呼叫 create_note(title, review, rating)
    Model->>DB: 執行 SQL: INSERT INTO notes...
    DB-->>Model: 回傳執行成功狀態
    Model-->>Route: 建立成功
    
    Route-->>Browser: HTTP 302 重導向 (Redirect to /)
    Browser->>Route: GET / (請求首頁)
    Route->>Model: 呼叫 get_all_notes()
    Model->>DB: 執行 SQL: SELECT * FROM notes...
    DB-->>Model: 回傳筆記資料陣列
    Model-->>Route: 回傳筆記清單
    Route-->>Browser: 渲染 index.html (包含最新筆記)
```

---

## 3. 功能清單對照表

以下整理主要功能所對應的 URL 路徑、HTTP 方法與負責的頁面/動作。

| 功能描述 | HTTP 方法 | URL 路徑 | 負責的模板 / 動作說明 |
| :--- | :--- | :--- | :--- |
| **首頁 / 筆記列表** | GET | `/` 或 `/notes` | `index.html` (顯示所有筆記) |
| **顯示新增頁面** | GET | `/notes/create` | `create.html` (顯示新增表單) |
| **處理新增資料** | POST | `/notes/create` | 處理表單後重導向至 `/` |
| **查看筆記細節** | GET | `/notes/<id>` | `detail.html` (顯示特定筆記) |
| **顯示編輯頁面** | GET | `/notes/<id>/edit` | `edit.html` (顯示編輯表單，可與 create.html 共用) |
| **處理編輯資料** | POST | `/notes/<id>/edit` | 處理修改後重導向至 `/notes/<id>` |
| **刪除筆記** | POST | `/notes/<id>/delete` | 處理刪除後重導向至 `/` |
| **搜尋筆記** | GET | `/search` | 根據 `?q=關鍵字` 渲染 `index.html` 的搜尋結果 |
