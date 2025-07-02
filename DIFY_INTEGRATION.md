# Dify統合ガイド - SEO見出し抽出API

## 概要
このAPIは複数のURLから`<h1>`、`<h2>`、`<h3>`タグを階層構造で一括抽出するFastAPIサービスです。Google Cloud Runにデプロイされ、Difyワークフローから呼び出すことができます。

## API情報
- **URL**: `https://seo-fastapi-449500499475.asia-northeast1.run.app`
- **エンドポイント**: `/extract-headings`
- **メソッド**: POST
- **認証**: Google Cloud IDトークン + APIキー

## 認証方法

### 1. Google Cloud IDトークンの取得
```bash
# サービスアカウントキーで認証
gcloud auth activate-service-account --key-file=dify-service-account-key.json

# IDトークンを取得
gcloud auth print-identity-token --audiences=https://seo-fastapi-449500499475.asia-northeast1.run.app
```

### 2. 必要なヘッダー
```
Authorization: Bearer [IDトークン]
X-API-Key: dify-seo-api-key-2025
Content-Type: application/json
```

## Difyでの設定方法

### HTTPリクエストノードの設定

1. **基本設定**
   - URL: `https://seo-fastapi-449500499475.asia-northeast1.run.app/extract-headings`
   - Method: `POST`

2. **ヘッダー設定**
   ```json
   {
     "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6Ijg4MjUwM2E1ZmQ1NmU5ZjczNGRmYmE1YzUwZDdiZjQ4ZGIyODRhZTkiLCJ0eXAiOiJKV1QifQ...",
     "X-API-Key": "dify-seo-api-key-2025",
     "Content-Type": "application/json"
   }
   ```

3. **リクエストボディ**
   ```json
   {
     "urls": [
       "https://example.com",
       "https://another-site.com"
     ]
   }
   ```

## レスポンス形式

### 成功レスポンス (200 OK)
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
            "h2_text": "セクション1",
            "h3_tags": ["サブセクション1-1", "サブセクション1-2"]
          },
          {
            "h2_text": "セクション2", 
            "h3_tags": ["サブセクション2-1"]
          }
        ]
      }
    }
  ]
}
```

### エラーレスポンス
```json
{
  "url": "https://invalid-url.com",
  "status": "error",
  "error": "HTTPエラー: 404"
}
```

## 使用例

### 1. 単一URLの処理
```json
{
  "urls": ["https://example.com"]
}
```

### 2. 複数URLの一括処理
```json
{
  "urls": [
    "https://site1.com",
    "https://site2.com", 
    "https://site3.com"
  ]
}
```

## エラーハンドリング

### 認証エラー
- **401 Unauthorized**: IDトークンが無効または期限切れ
- **403 Forbidden**: APIキーが無効

### APIエラー
- **422 Unprocessable Entity**: リクエストボディの形式が不正
- **500 Internal Server Error**: サーバー内部エラー

## 制限事項

1. **IDトークンの有効期限**: 約1時間（定期的な更新が必要）
2. **同時処理**: 複数URLを並列処理（個別にエラーハンドリング）
3. **タイムアウト**: 各URLのリクエストタイムアウトは10秒

## トラブルシューティング

### よくある問題

1. **403 Forbiddenエラー**
   - 組織ポリシーによりパブリックアクセスが制限されています
   - 必ずGoogle Cloud IDトークンを使用してください

2. **401 Unauthorizedエラー**
   - IDトークンの期限切れまたは無効
   - 新しいIDトークンを取得してください

3. **APIキーエラー**
   - X-API-Keyヘッダーが正しく設定されているか確認
   - 値: `dify-seo-api-key-2025`

## セキュリティ

- APIキーは環境変数として管理することを推奨
- IDトークンは定期的に更新
- サービスアカウントキーは安全に保管

## サポート

問題が発生した場合は、以下を確認してください：
1. IDトークンの有効性
2. APIキーの正確性
3. リクエスト形式の妥当性
4. ネットワーク接続

---

**最終更新**: 2025年7月3日
**APIバージョン**: v1.0
**Cloud Runサービス**: seo-fastapi (asia-northeast1)