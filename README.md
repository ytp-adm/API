# SEO見出し抽出API - Google Cloud Run版

複数のURLから`<h1>`、`<h2>`、`<h3>`タグを階層構造で一括抽出するFastAPIアプリケーションです。Google Cloud Runにデプロイされ、Difyワークフローから呼び出すことができます。

## 🚀 本番環境

- **API URL**: https://seo-fastapi-449500499475.asia-northeast1.run.app
- **プロジェクト**: dify-seo-api-2025
- **リージョン**: asia-northeast1
- **認証**: Google Cloud IDトークン + APIキー

## 📋 機能

- ✅ 複数URLの一括処理（並列処理）
- ✅ h1、h2、h3タグの抽出
- ✅ **階層構造の表現**: h3タグがどのh2タグの下に属しているかを明確に表示
- ✅ 個別エラーハンドリング（一部のURLでエラーが発生しても他のURLは正常に処理）
- ✅ APIキー認証によるセキュアなアクセス
- ✅ 詳細なログ出力とエラー情報
- ✅ キャッシュバスティング機能

## 🔧 ローカル開発

### インストール
```bash
pip install -r requirements.txt
```

### サーバー起動
```bash
python main.py
```

サーバーは `http://localhost:8000` で起動します。

## 📡 API仕様

### 認証
すべてのAPIエンドポイント（`/`と`/health`を除く）には以下の認証が必要です：

```http
Authorization: Bearer [Google Cloud IDトークン]
X-API-Key: dify-seo-api-key-2025
```

### エンドポイント

#### `POST /extract-headings`
複数のURLから見出しタグを階層構造で抽出します。

**リクエスト例:**
```json
{
  "urls": [
    "https://example.com",
    "https://another-site.com"
  ]
}
```

**レスポンス例:**
```json
{
  "processing_time_seconds": 2.34,
  "results": [
    {
      "url": "https://example.com",
      "status": "success",
      "headings": {
        "h1": ["メインタイトル"],
        "h2_sections": [
          {
            "h2_text": "セクション1のタイトル",
            "h3_tags": ["サブセクション1-1", "サブセクション1-2"]
          },
          {
            "h2_text": "セクション2のタイトル", 
            "h3_tags": ["サブセクション2-1"]
          }
        ]
      }
    },
    {
      "url": "https://another-site.com",
      "status": "error",
      "error": "HTTPエラー: 404"
    }
  ]
}
```

#### その他のエンドポイント
- `GET /`: API情報（認証不要）
- `GET /health`: ヘルスチェック（認証不要）
- `GET /docs`: Swagger UI（認証不要）

## 🔐 認証設定

### Google Cloud IDトークンの取得

```bash
# サービスアカウントで認証
gcloud auth activate-service-account --key-file=dify-service-account-key.json

# IDトークンを取得
gcloud auth print-identity-token --audiences=https://seo-fastapi-449500499475.asia-northeast1.run.app
```

## 🔗 Dify統合

詳細な統合ガイドは [`DIFY_INTEGRATION.md`](DIFY_INTEGRATION.md) を参照してください。

### 基本設定

**HTTPリクエストノード設定:**
- **URL**: `https://seo-fastapi-449500499475.asia-northeast1.run.app/extract-headings`
- **Method**: `POST`
- **Headers**:
  ```json
  {
    "Authorization": "Bearer [IDトークン]",
    "X-API-Key": "dify-seo-api-key-2025",
    "Content-Type": "application/json"
  }
  ```
- **Body**:
  ```json
  {
    "urls": ["{{input_url}}"]
  }
  ```

## 🏗️ プロジェクト構造

```
SEO_FAST_API/
├── main.py                    # メインAPIアプリケーション
├── requirements.txt           # Python依存関係
├── Dockerfile                # Dockerコンテナ設定
├── cloudbuild.yaml           # Cloud Build設定
├── deploy.sh                 # デプロイスクリプト
├── README.md                 # このファイル
├── DIFY_INTEGRATION.md       # Dify統合ガイド
├── .gitignore               # Git除外設定
├── .dockerignore            # Docker除外設定
└── dify-service-account-key.json  # サービスアカウントキー（非公開）
```

## 🛠️ 技術スタック

- **フレームワーク**: FastAPI
- **HTMLパーサー**: BeautifulSoup4
- **HTTPクライアント**: Requests
- **バリデーション**: Pydantic
- **コンテナ**: Docker
- **デプロイ**: Google Cloud Run
- **CI/CD**: Google Cloud Build
- **レジストリ**: Google Artifact Registry

## 🚀 デプロイメント

### 自動デプロイ（推奨）
```bash
gcloud builds submit --config cloudbuild.yaml .
```

### 手動デプロイ
```bash
# プロジェクト設定
gcloud config set project dify-seo-api-2025

# APIの有効化
gcloud services enable cloudbuild.googleapis.com run.googleapis.com artifactregistry.googleapis.com

# ビルド・デプロイ
gcloud builds submit --config cloudbuild.yaml
```

## 🔍 トラブルシューティング

### よくある問題

1. **403 Forbiddenエラー**
   - Google Cloud IDトークンが必要です
   - 組織ポリシーによりパブリックアクセスが制限されています

2. **401 Unauthorizedエラー**
   - IDトークンの期限切れまたは無効
   - APIキーが正しく設定されているか確認

3. **APIキーエラー**
   - `X-API-Key: dify-seo-api-key-2025` が正しく設定されているか確認

## 💰 料金

- **Cloud Run**: リクエスト数とCPU/メモリ使用量に基づく従量課金
- **無料枠**: 月200万リクエストまで無料
- **推定コスト**: 月1000リクエスト程度なら無料枠内

## 🔒 セキュリティ

- Google Cloud IDトークンによる認証
- APIキーによる追加セキュリティ層
- サービスアカウントベースの権限管理
- 組織ポリシーに準拠したアクセス制御

## 📄 ライセンス

MIT License

---

**最終更新**: 2025年7月3日  
**APIバージョン**: v1.0  
**Cloud Runサービス**: seo-fastapi (asia-northeast1)