# HTML見出し抽出API

指定されたURLリストから`<h1>`、`<h2>`、`<h3>`タグを階層構造で一括抽出するFastAPI アプリケーションです。

## 機能

- 複数URLの一括処理
- h1、h2、h3タグの抽出
- **階層構造の表現**: h3タグがどのh2タグの下に属しているかを明確に表示
- 個別エラーハンドリング（一部のURLでエラーが発生しても他のURLは正常に処理）
- 統計情報の提供
- キャッシュバスティング機能
- 詳細なログ出力

## インストール

```bash
pip install -r requirements.txt
```

## 使用方法

### サーバー起動

```bash
python main.py
```

サーバーは `http://localhost:8000` で起動します。

### API仕様

#### エンドポイント: `POST /extract-headings`

複数のURLから見出しタグを階層構造で抽出します。

**リクエスト例:**
```json
{
  "urls": [
    "https://example.com/page1",
    "https://example.com/page2"
  ]
}
```

**レスポンス例:**
```json
{
  "results": {
    "https://example.com/page1": {
      "h1_tags": ["メインタイトル"],
      "sections": [
        {
          "h2_title": "セクション1のタイトル",
          "h3_tags": ["サブセクション1-1", "サブセクション1-2"]
        },
        {
          "h2_title": "セクション2のタイトル", 
          "h3_tags": ["サブセクション2-1"]
        },
        {
          "h2_title": "セクション3のタイトル",
          "h3_tags": []
        }
      ],
      "orphan_h3_tags": [],
      "total_h1": 1,
      "total_h2": 3,
      "total_h3": 3
    },
    "https://example.com/page2": {
      "error": "HTTPリクエストエラー: 404 Not Found"
    }
  },
  "total_processed": 2,
  "total_success": 1,
  "total_errors": 1
}
```

#### レスポンス構造の説明

- **`h1_tags`**: ページ内のすべてのh1タグのテキスト
- **`sections`**: h2タグとその下に属するh3タグの階層構造
  - `h2_title`: h2タグのテキスト
  - `h3_tags`: そのh2の下に属するh3タグのリスト
- **`orphan_h3_tags`**: h2タグの前に出現する孤立したh3タグ
- **統計情報**: 各タグの総数
- **エラー情報**: 個別URLでエラーが発生した場合の詳細

### その他のエンドポイント

- `GET /`: API情報
- `GET /health`: ヘルスチェック
- `GET /docs`: Swagger UI（API仕様書）

## 特徴

### 階層構造の表現
従来の単純なリスト形式ではなく、h3タグがどのh2タグの下に属しているかを明確に表現します。

### エラーハンドリング
- 個別URLでエラーが発生しても、他のURLの処理は継続
- 詳細なエラーメッセージを提供
- HTTPエラー、タイムアウト、パースエラーなどに対応

### キャッシュ対策
- キャッシュバスティングパラメータの自動追加
- 適切なHTTPヘッダーの設定
- 最新のコンテンツを確実に取得

## 開発

### テスト実行
```bash
python test_api.py
```

### デバッグ
```bash
python debug_headings.py
```

## 技術仕様

- **フレームワーク**: FastAPI
- **HTMLパーサー**: BeautifulSoup4
- **HTTPクライアント**: Requests
- **バリデーション**: Pydantic
- **ログ**: Python標準ログ

## GCPデプロイ手順

### 前提条件
1. Google Cloud Platform アカウント
2. Google Cloud SDK (gcloud) のインストール
3. プロジェクトの作成と課金の有効化

### デプロイ手順

#### 1. プロジェクトIDの設定
[`deploy.sh`](deploy.sh:4)の`PROJECT_ID`を実際のGCPプロジェクトIDに変更：
```bash
PROJECT_ID="your-actual-gcp-project-id"
```

#### 2. gcloudの認証
```bash
gcloud auth login
gcloud auth configure-docker
```

#### 3. デプロイ実行
```bash
# Linuxの場合
chmod +x deploy.sh
./deploy.sh

# Windowsの場合
bash deploy.sh
```

#### 4. 手動デプロイ（オプション）
```bash
# プロジェクト設定
gcloud config set project your-project-id

# APIの有効化
gcloud services enable cloudbuild.googleapis.com run.googleapis.com

# ビルド・デプロイ
gcloud builds submit --config cloudbuild.yaml
```

### Difyからの呼び出し

デプロイ後、DifyのHTTPリクエストノードで以下のように設定：

**エンドポイント**: `https://your-service-url/extract-headings`
**メソッド**: POST
**ヘッダー**: `Content-Type: application/json`
**ボディ**:
```json
{
  "urls": ["{{input_url}}"]
}
```

**レスポンス例**:
```json
{
  "results": {
    "https://example.com/": {
      "h1_tags": ["メインタイトル"],
      "sections": [
        {
          "h2_title": "セクション1",
          "h3_tags": ["サブセクション1-1"]
        }
      ],
      "total_h1": 1,
      "total_h2": 1,
      "total_h3": 1
    }
  },
  "total_processed": 1,
  "total_success": 1,
  "total_errors": 0
}
```

### 料金について
- Cloud Run: リクエスト数とCPU/メモリ使用量に基づく従量課金
- 無料枠: 月200万リクエストまで無料
- 推定コスト: 月1000リクエスト程度なら無料枠内

## ライセンス

MIT License