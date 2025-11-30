# push_system_mvp

FastAPI-based real-time push notification MVP.

Features
- User registration + login (JWT)
- Create and persist messages
- Real-time delivery via WebSocket + Redis pub/sub

Run locally (recommended: use Docker Compose):

```powershell
cd C:\Users\homet\OneDrive\桌面\Programing\SideProject\push_system_mvp
docker-compose up --build
```

App will be available at http://localhost:8000 and WebSocket endpoint at ws://localhost:8000/ws?token=<jwt>

======== 檔案架構 ========

push_system_mvp
app/
- __init__.py            # 標記 app 是 Python package，可選初始化程式碼
- main.py                # FastAPI 啟動入口，初始化路由、WebSocket、DB連線
- config.py              # 系統配置 (DB連線、Redis設定、JWT密鑰等)
- models/
__init__.py        # 標記 models 是 package
user.py            # 定義使用者 ORM 模型 (User table)
message.py         # 定義推播訊息 ORM 模型 (Message table)
│
│   ├── schemas/
│   │   ├── __init__.py        # 標記 schemas 是 package
│   │   ├── user.py            # 使用者 API 請求/回應格式 (Pydantic schema)
│   │   └── message.py         # 推播訊息 API 請求/回應格式
│
│   ├── crud/
│   │   ├── __init__.py        # 標記 crud 是 package
│   │   ├── user.py            # 封裝使用者資料庫操作 (CRUD)
│   │   └── message.py         # 封裝訊息資料庫操作 (CRUD)
│
│   ├── api/
│   │   ├── __init__.py        # 標記 api 是 package
│   │   ├── auth.py            # 登入 / 註冊 API
│   │   └── message.py         # 發送/查詢推播訊息 API
│
│   ├── services/
│   │   ├── __init__.py        # 標記 services 是 package
│   │   ├── websocket_manager.py  # 管理 WebSocket 連線、線上用戶
│   │   └── push_service.py       # 處理推播邏輯、群發訊息
│
│   └── utils/
│       ├── __init__.py        # 標記 utils 是 package
│       ├── security.py        # JWT、密碼雜湊等安全工具
│       └── logger.py          # 日誌工具
│
├── tests/
│   ├── test_auth.py           # 測試登入/註冊功能
│   └── test_message.py        # 測試推播訊息功能
│
├── requirements.txt           # Python 套件清單
├── Dockerfile                 # 容器化服務的定義
├── docker-compose.yml         # 多容器啟動配置 (FastAPI + Redis + DB)
└── README.md                  # 專案說明文件

======== 流程簡述 ========
使用者登入 → 後端驗證 JWT → 回傳 token
使用者透過 WebSocket 連線 → 後端 websocket_manager 記錄連線
發送推播訊息 → push_service 處理邏輯 → 儲存資料庫 → 廣播到所有線上用戶
前端接收訊息 → 顯示通知或更新列表
Redis 支援跨實例廣播（MVP階段可單機即可）

[ 前端 Web / Browser ]
        │
        │ HTTP API 請求 (登入 / 註冊 / 發送訊息)
        │
        ▼
[ FastAPI 後端 ]
  ├─ /auth           ---> JWT 認證 (登入/註冊)
  ├─ /message        ---> 發送推播、查詢歷史
  ├─ services/
  │     ├─ push_service.py         ---> 處理訊息、群發邏輯
  │     └─ websocket_manager.py   ---> WebSocket 連線管理
  └─ crud/                          ---> 資料庫操作
        │
        ▼
[ 資料庫 (PostgreSQL / MySQL) ]
  ├─ users
  └─ messages
        │
        ▼
[ Redis (快取 / Pub-Sub) ]
  ├─ 保存線上用戶連線資訊
  └─ 協助即時廣播訊息到多個後端實例
        │
        ▼
[ 前端 Web / Browser ]

  └─ WebSocket 接收即時推播




